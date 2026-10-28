import uuid
from decimal import Decimal
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.dependencies import require_admin, require_permission, get_current_customer
from app.repositories.db import get_db
from app.repositories import booking_repository, audit_repository
from app.models.user import User
from app.models.provider import Provider
from app.models.customer import Customer, BookingWarranty
from app.models.booking import Booking, BookingStatus, PaymentStatus
from app.models.payment import BookingPayment
from app.services.booking.otp_service import generate_secure_otp, get_active_otp, verify_and_consume_otp
from app.schemas.booking import (
    BookingCreateRequest,
    BookingStatusUpdateRequest,
    ProviderReassignRequest,
    BookingDetailResponse,
    PaymentRecordResponse,
    PaymentVerifyRequest,
    PaymentRejectRequest,
)

router = APIRouter(prefix="/admin/bookings", tags=["Admin Booking Operations"])
payments_admin_router = APIRouter(prefix="/admin/payments", tags=["Admin Payment Review Operations"])

VALID_TRANSITIONS = {
    BookingStatus.REQUESTED: [BookingStatus.ASSIGNED, BookingStatus.ACCEPTED, BookingStatus.CANCELLED, BookingStatus.REJECTED, BookingStatus.EXPIRED],
    BookingStatus.ASSIGNED: [BookingStatus.ACCEPTED, BookingStatus.CANCELLED, BookingStatus.REJECTED, BookingStatus.EXPIRED],
    BookingStatus.ACCEPTED: [BookingStatus.ON_THE_WAY, BookingStatus.CANCELLED],
    BookingStatus.ON_THE_WAY: [BookingStatus.ARRIVED, BookingStatus.CANCELLED],
    BookingStatus.ARRIVED: [BookingStatus.STARTED, BookingStatus.CANCELLED],
    BookingStatus.STARTED: [BookingStatus.COMPLETED, BookingStatus.PAID, BookingStatus.CANCELLED],
    BookingStatus.COMPLETED: [BookingStatus.PAID],
    BookingStatus.PAID: [],
    BookingStatus.CANCELLED: [],
    BookingStatus.REJECTED: [],
    BookingStatus.EXPIRED: []
}

def get_allowed_next(status_val):
    for k in VALID_TRANSITIONS:
        if k.value.lower() == str(status_val).lower():
            return [st.value for st in VALID_TRANSITIONS[k]]
    return []

def safe_timeline(raw_timeline):
    if isinstance(raw_timeline, list):
        return raw_timeline
    if isinstance(raw_timeline, dict):
        return [raw_timeline]
    return []

def format_warranty(w):
    if not w:
        return None
    now_utc = datetime.now(timezone.utc)
    exp = w.expires_at
    if exp and exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)
    is_valid = w.is_active and (exp > now_utc if exp else True)
    return {
        "id": str(w.id),
        "service_name": w.service_name,
        "issued_at": w.issued_at.isoformat() if w.issued_at else None,
        "expires_at": w.expires_at.isoformat() if w.expires_at else None,
        "is_active": w.is_active,
        "is_valid": is_valid,
        "claim_status": w.claim_status or "None",
        "claim_description": w.claim_description,
        "claim_submitted_at": w.claim_submitted_at.isoformat() if w.claim_submitted_at else None,
        "claim_resolved_at": w.claim_resolved_at.isoformat() if w.claim_resolved_at else None,
        "claim_notes": w.claim_notes,
    }

def clean_admin_photos(photos):
    if not photos:
        return []
    res = []
    for p in photos:
        if isinstance(p, str):
            if p.startswith("/static/"):
                res.append(f"https://smartserve-api-de3f.onrender.com{p}")
            elif p.startswith("data:image"):
                if len(p) <= 120000:
                    res.append(p)
                else:
                    res.append("https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=600&q=80")
            else:
                res.append(p)
    return res

def _serialize_admin_booking(b: Booking) -> BookingDetailResponse:
    c_name = b.customer.full_name if b.customer else "Customer"
    c_phone = b.customer.phone if (b.customer and b.customer.phone) else "+91 98765 43210"
    p_name = b.provider.full_name if b.provider else None
    s_name = b.service.name if b.service else "Home Service"
    allowed_next = get_allowed_next(b.status)

    return BookingDetailResponse(
        id=str(b.id),
        customer_id=str(b.customer_id),
        customer_name=c_name,
        customer_phone=c_phone,
        provider_id=str(b.provider_id) if b.provider_id else None,
        provider_name=p_name,
        service_id=str(b.service_id),
        service_name=s_name,
        status=b.status.value if hasattr(b.status, 'value') else str(b.status),
        payment_method=b.payment_method or "COD",
        payment_status=b.payment_status.value if hasattr(b.payment_status, 'value') else str(b.payment_status),
        scheduled_time=b.scheduled_time.isoformat() if b.scheduled_time else "",
        address=b.address or "",
        total_price=float(b.total_price or 0.0),
        otp_code=b.otp_code,
        start_otp=b.start_otp,
        completion_otp=b.completion_otp,
        timeline=safe_timeline(b.timeline),
        allowed_next_statuses=allowed_next,
        emergency_flag=b.emergency_flag,
        cancellation_reason=b.cancellation_reason,
        customer_notes=b.customer_notes,
        before_photos=clean_admin_photos(b.before_photos),
        after_photos=clean_admin_photos(b.after_photos),
        warranty=format_warranty(b.warranty),
        created_at=b.created_at.isoformat() if b.created_at else ""
    )

@router.get("/", response_model=List[BookingDetailResponse])
def list_admin_bookings(
    status_filter: Optional[str] = None,
    emergency_only: Optional[bool] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Retrieve filterable bookings list for admin operations with fast eager loading."""
    from sqlalchemy.orm import joinedload
    from sqlalchemy import desc
    query = (
        db.query(Booking)
        .options(
            joinedload(Booking.customer),
            joinedload(Booking.provider),
            joinedload(Booking.service),
            joinedload(Booking.warranty),
        )
    )
    if status_filter:
        query = query.filter(Booking.status == status_filter)
    bookings = query.order_by(desc(Booking.created_at)).offset(skip).limit(limit).all()
    
    res = []
    for b in bookings:
        if emergency_only and not b.emergency_flag:
            continue

        matches_search = True
        if search:
            s_lower = search.lower()
            c_name = b.customer.full_name.lower() if b.customer else ""
            p_name = b.provider.full_name.lower() if b.provider else ""
            srv_name = b.service.name.lower() if b.service else ""
            matches_search = (s_lower in c_name or s_lower in p_name or s_lower in srv_name or s_lower in str(b.id))

        if matches_search:
            res.append(_serialize_admin_booking(b))

    return res


# =========================================================================
# ADMIN COD PAYMENT REVIEW QUEUE & AUDIT TRAIL ENDPOINTS
# =========================================================================

def _serialize_payment_record(p: BookingPayment) -> PaymentRecordResponse:
    b = p.booking
    c = p.customer or (b.customer if b else None)
    prov = p.provider or (b.provider if b else None)
    srv = b.service if b else None

    c_name = c.full_name if c else "Customer"
    c_phone = c.phone if c and c.phone else "+91 98765 43210"
    prov_name = prov.full_name if prov else None
    srv_name = srv.name if srv else "Home Service"
    ref_code = b.booking_reference if b else f"BK-{str(p.booking_id)[:8].upper()}"

    return PaymentRecordResponse(
        id=str(p.id),
        booking_id=str(p.booking_id),
        booking_reference=ref_code,
        customer_id=str(p.customer_id),
        customer_name=c_name,
        customer_phone=c_phone,
        provider_id=str(p.provider_id) if p.provider_id else None,
        provider_name=prov_name,
        service_id=str(b.service_id) if b else None,
        service_name=srv_name,
        payment_method=p.payment_method or "COD",
        agreed_amount=float(p.agreed_amount or 0.0),
        reported_amount=float(p.reported_amount) if p.reported_amount is not None else None,
        status=p.status,
        discrepancy_flag=bool(p.discrepancy_flag),
        discrepancy_amount=float(p.discrepancy_amount or 0.0),
        collected_at=p.collected_at.isoformat() if p.collected_at else None,
        collection_notes=p.collection_notes,
        reviewed_by_id=str(p.reviewed_by_id) if p.reviewed_by_id else None,
        reviewed_by_name=p.reviewed_by_name,
        reviewed_at=p.reviewed_at.isoformat() if p.reviewed_at else None,
        rejection_reason=p.rejection_reason,
        created_at=p.created_at.isoformat() if p.created_at else "",
        updated_at=p.updated_at.isoformat() if p.updated_at else "",
    )


@router.get("/payments/review", response_model=List[PaymentRecordResponse])
@payments_admin_router.get("/", response_model=List[PaymentRecordResponse])
@payments_admin_router.get("/review", response_model=List[PaymentRecordResponse])
def list_cod_payments_for_review(
    status_filter: Optional[str] = None,
    discrepancy_only: Optional[bool] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    List COD payment records for Admin Payment Review.
    Enforces Admin authorization and allows filtering by status and discrepancy flag.
    """
    query = db.query(BookingPayment).join(Booking, BookingPayment.booking_id == Booking.id)

    if status_filter and status_filter.strip().lower() != "all":
        norm_st = status_filter.strip().lower()
        if norm_st in ["collection_reported", "collection reported"]:
            query = query.filter(func.lower(BookingPayment.status) == "collection reported")
        elif norm_st in ["pending"]:
            query = query.filter(func.lower(BookingPayment.status) == "pending")
        elif norm_st in ["paid"]:
            query = query.filter(func.lower(BookingPayment.status) == "paid")
        elif norm_st in ["rejected"]:
            query = query.filter(func.lower(BookingPayment.status) == "rejected")
        else:
            query = query.filter(func.lower(BookingPayment.status) == norm_st)

    if discrepancy_only:
        query = query.filter(BookingPayment.discrepancy_flag == True)

    payments = query.order_by(BookingPayment.created_at.desc()).offset(skip).limit(limit).all()

    res = []
    for p in payments:
        b = p.booking
        c = p.customer or (b.customer if b else None)
        prov = p.provider or (b.provider if b else None)
        srv = b.service if b else None

        c_name = c.full_name if c else "Customer"
        prov_name = prov.full_name if prov else None
        srv_name = srv.name if srv else "Home Service"
        ref_code = b.booking_reference if b else f"BK-{str(p.booking_id)[:8].upper()}"

        if search:
            s_low = search.lower()
            matches = (
                s_low in ref_code.lower()
                or s_low in c_name.lower()
                or (prov_name and s_low in prov_name.lower())
                or (srv_name and s_low in srv_name.lower())
                or s_low in str(p.booking_id).lower()
            )
            if not matches:
                continue

        res.append(_serialize_payment_record(p))
    return res


@router.post("/payments/{payment_id}/verify", response_model=PaymentRecordResponse)
@payments_admin_router.post("/{payment_id}/verify", response_model=PaymentRecordResponse)
def verify_payment_collection_by_id(
    payment_id: str,
    req: Optional[PaymentVerifyRequest] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Admin endpoint to verify a reported cash collection."""
    from app.core.websockets import broadcast_realtime

    try:
        p_uuid = uuid.UUID(payment_id)
        payment = db.query(BookingPayment).filter(BookingPayment.id == p_uuid).first()
    except ValueError:
        payment = None

    if not payment:
        # Fallback by booking_id
        try:
            b_uuid = uuid.UUID(payment_id)
            payment = db.query(BookingPayment).filter(BookingPayment.booking_id == b_uuid).order_by(BookingPayment.created_at.desc()).first()
        except ValueError:
            b_match = db.query(Booking).filter(Booking.booking_reference == payment_id).first()
            if b_match:
                payment = db.query(BookingPayment).filter(BookingPayment.booking_id == b_match.id).order_by(BookingPayment.created_at.desc()).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment record not found")

    booking = payment.booking or db.query(Booking).filter(Booking.id == payment.booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Associated booking not found")

    now_utc = datetime.now(timezone.utc)
    admin_name = getattr(admin, "full_name", None) or getattr(admin, "email", "Admin")

    payment.status = "Paid"
    payment.reviewed_by_id = admin.id
    payment.reviewed_by_name = admin_name
    payment.reviewed_at = now_utc
    payment.updated_at = now_utc
    db.add(payment)

    booking.payment_status = "Paid"

    # Append audit event to booking timeline
    audit_event = {
        "event": "Admin Verified Cash Collection",
        "actor": admin_name,
        "role": admin.role,
        "agreed_amount": float(payment.agreed_amount),
        "verified_amount": float(payment.reported_amount or payment.agreed_amount),
        "notes": req.notes if req and req.notes else "Admin verified cash collection",
        "timestamp": now_utc.isoformat(),
    }
    tl = list(booking.timeline or [])
    tl.append(audit_event)
    booking.timeline = tl

    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(booking, "timeline")

    audit_repository.create_audit_log(
        db, actor_id=admin.id, actor_email=admin.email, actor_role=admin.role,
        action=f"Verified COD Payment for Booking {booking.booking_reference}",
        target_resource=str(payment.id),
        metadata_json={
            "booking_id": str(booking.id),
            "agreed_amount": float(payment.agreed_amount),
            "reported_amount": float(payment.reported_amount or payment.agreed_amount),
            "discrepancy_flag": payment.discrepancy_flag,
        }
    )

    db.commit()
    db.refresh(payment)
    db.refresh(booking)

    # Automated Notification Trigger: Payment Verified
    try:
        from app.services.notification import notify_booking_event
        notify_booking_event(
            db,
            booking,
            "payment.verified",
            extra_context={
                "payment_id": str(payment.id),
                "notes": req.notes if req and req.notes else "Admin verified cash collection",
            },
        )
    except Exception as exc:
        pass

    # Broadcast notification across channels
    cust_id = str(booking.customer_id) if booking.customer_id else None
    channels = ["dashboard", "bookings", "admin", f"booking_{booking.id}", f"admin_booking_{booking.id}"]
    if cust_id:
        channels.extend([f"customer_{cust_id}", f"user_{cust_id}"])
    if booking.provider_id:
        channels.extend([f"provider_{booking.provider_id}", f"user_{booking.provider_id}"])

    broadcast_realtime(channels, {
        "type": "PAYMENT_VERIFIED",
        "event": "payment.verified",
        "event_type": "payment.verified",
        "booking_id": str(booking.id),
        "payment_id": str(payment.id),
        "payment_status": "Paid",
        "reviewed_by": admin_name,
        "timestamp": now_utc.isoformat(),
    })

    return _serialize_payment_record(payment)


@router.post("/{booking_id}/verify-payment", response_model=PaymentRecordResponse)
def verify_payment_collection_by_booking(
    booking_id: str,
    req: Optional[PaymentVerifyRequest] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Admin shortcut to verify payment by booking reference or ID."""
    return verify_payment_collection_by_id(payment_id=booking_id, req=req, db=db, admin=admin)


@router.post("/payments/{payment_id}/reject", response_model=PaymentRecordResponse)
@payments_admin_router.post("/{payment_id}/reject", response_model=PaymentRecordResponse)
def reject_payment_collection_by_id(
    payment_id: str,
    req: PaymentRejectRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Admin endpoint to reject a reported cash collection with mandatory reason."""
    from app.core.websockets import broadcast_realtime

    if not req.reason or not req.reason.strip():
        raise HTTPException(status_code=400, detail="Rejection reason is required")

    try:
        p_uuid = uuid.UUID(payment_id)
        payment = db.query(BookingPayment).filter(BookingPayment.id == p_uuid).first()
    except ValueError:
        payment = None

    if not payment:
        # Fallback by booking_id
        try:
            b_uuid = uuid.UUID(payment_id)
            payment = db.query(BookingPayment).filter(BookingPayment.booking_id == b_uuid).order_by(BookingPayment.created_at.desc()).first()
        except ValueError:
            b_match = db.query(Booking).filter(Booking.booking_reference == payment_id).first()
            if b_match:
                payment = db.query(BookingPayment).filter(BookingPayment.booking_id == b_match.id).order_by(BookingPayment.created_at.desc()).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment record not found")

    booking = payment.booking or db.query(Booking).filter(Booking.id == payment.booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Associated booking not found")

    now_utc = datetime.now(timezone.utc)
    admin_name = getattr(admin, "full_name", None) or getattr(admin, "email", "Admin")

    payment.status = "Rejected"
    payment.rejection_reason = req.reason.strip()
    payment.reviewed_by_id = admin.id
    payment.reviewed_by_name = admin_name
    payment.reviewed_at = now_utc
    payment.updated_at = now_utc
    db.add(payment)

    booking.payment_status = "Rejected"

    # Append audit event to booking timeline
    audit_event = {
        "event": "Admin Rejected Cash Collection Report",
        "actor": admin_name,
        "role": admin.role,
        "reason": req.reason.strip(),
        "timestamp": now_utc.isoformat(),
    }
    tl = list(booking.timeline or [])
    tl.append(audit_event)
    booking.timeline = tl

    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(booking, "timeline")

    audit_repository.create_audit_log(
        db, actor_id=admin.id, actor_email=admin.email, actor_role=admin.role,
        action=f"Rejected COD Payment for Booking {booking.booking_reference}: {req.reason.strip()}",
        target_resource=str(payment.id),
        metadata_json={
            "booking_id": str(booking.id),
            "reason": req.reason.strip(),
        }
    )

    db.commit()
    db.refresh(payment)
    db.refresh(booking)

    # Automated Notification Trigger: Payment Rejected
    try:
        from app.services.notification import notify_booking_event
        notify_booking_event(
            db,
            booking,
            "payment.rejected",
            extra_context={
                "payment_id": str(payment.id),
                "notes": req.reason.strip(),
            },
        )
    except Exception as exc:
        pass

    # Broadcast notification across channels
    cust_id = str(booking.customer_id) if booking.customer_id else None
    channels = ["dashboard", "bookings", "admin", f"booking_{booking.id}", f"admin_booking_{booking.id}"]
    if cust_id:
        channels.extend([f"customer_{cust_id}", f"user_{cust_id}"])
    if booking.provider_id:
        channels.extend([f"provider_{booking.provider_id}", f"user_{booking.provider_id}"])

    broadcast_realtime(channels, {
        "type": "PAYMENT_REJECTED",
        "event": "payment.rejected",
        "event_type": "payment.rejected",
        "booking_id": str(booking.id),
        "payment_id": str(payment.id),
        "payment_status": "Rejected",
        "reason": req.reason.strip(),
        "reviewed_by": admin_name,
        "timestamp": now_utc.isoformat(),
    })

    return _serialize_payment_record(payment)


@router.post("/{booking_id}/reject-payment", response_model=PaymentRecordResponse)
def reject_payment_collection_by_booking(
    booking_id: str,
    req: PaymentRejectRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Admin shortcut to reject payment by booking reference or ID."""
    return reject_payment_collection_by_id(payment_id=booking_id, req=req, db=db, admin=admin)


@router.get("/{booking_id}/payments", response_model=List[PaymentRecordResponse])
def get_booking_payments(
    booking_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Retrieve full payment collection history and audit trail for a booking."""
    booking = None
    try:
        b_uuid = uuid.UUID(booking_id)
        booking = db.query(Booking).filter(Booking.id == b_uuid).first()
    except ValueError:
        booking = db.query(Booking).filter(Booking.booking_reference == booking_id).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    payments = (
        db.query(BookingPayment)
        .filter(BookingPayment.booking_id == booking.id)
        .order_by(BookingPayment.created_at.desc())
        .all()
    )
    return [_serialize_payment_record(p) for p in payments]


@router.get("/{booking_id}", response_model=BookingDetailResponse)
def get_admin_booking_detail(
    booking_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Retrieve detailed operational booking info by ID with eager loading."""
    try:
        b_uuid = uuid.UUID(booking_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid booking ID format")

    from sqlalchemy.orm import joinedload
    b = (
        db.query(Booking)
        .options(
            joinedload(Booking.customer),
            joinedload(Booking.provider),
            joinedload(Booking.service),
            joinedload(Booking.warranty),
        )
        .filter(Booking.id == b_uuid)
        .first()
    )
    if not b:
        raise HTTPException(status_code=404, detail="Booking not found")

    return _serialize_admin_booking(b)



@router.post("/", response_model=BookingDetailResponse, status_code=status.HTTP_201_CREATED)
def create_admin_booking(
    req: BookingCreateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("bookings:manage"))
):
    """Create a new booking directly from Admin console (Emergency dispatch / phone booking)."""
    try:
        c_uuid = uuid.UUID(req.customer_id)
        s_uuid = uuid.UUID(req.service_id)
        p_uuid = uuid.UUID(req.provider_id) if req.provider_id else None
        raw_sched = req.scheduled_time.replace("Z", "+00:00")
        sched_dt = datetime.fromisoformat(raw_sched)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID or datetime format")

    booking = booking_repository.create_booking(
        db,
        customer_id=c_uuid,
        service_id=s_uuid,
        scheduled_time=sched_dt,
        address=req.address,
        total_price=req.total_price,
        provider_id=p_uuid,
        emergency_flag=req.emergency_flag
    )

    audit_repository.create_audit_log(
        db, actor_id=admin.id, actor_email=admin.email, actor_role=admin.role,
        action=f"Created Admin Booking #{booking.id}", target_resource=str(booking.id)
    )

    try:
        from app.services.kafka import kafka_producer, KafkaTopics, KafkaEvent
        booking_event = KafkaEvent(
            event_type=KafkaTopics.BOOKING_CREATED,
            booking_id=str(booking.id),
            sender_id=str(admin.id),
            receiver_id=str(booking.provider_id) if booking.provider_id else None,
            payload={
                "booking_id": str(booking.id),
                "booking_reference": getattr(booking, "booking_reference", str(booking.id)[:8]),
                "customer_id": str(booking.customer_id),
                "provider_id": str(booking.provider_id) if booking.provider_id else None,
                "service_id": str(booking.service_id),
                "status": booking.status.value if hasattr(booking.status, "value") else str(booking.status),
                "address": booking.address,
                "total_price": float(booking.total_price),
                "emergency_flag": booking.emergency_flag,
                "created_at": booking.created_at.isoformat() if hasattr(booking.created_at, "isoformat") else str(booking.created_at),
            }
        )
        kafka_producer.publish_event(KafkaTopics.BOOKING_CREATED, booking_event)
    except Exception as exc:
        print(f"[Admin Booking Kafka Error] {exc}")

    return _serialize_admin_booking(booking)


@router.patch("/{booking_id}/status", response_model=BookingDetailResponse)
def transition_booking_status(
    booking_id: str,
    req: BookingStatusUpdateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("bookings:manage"))
):
    """Validate & execute backend booking state transition."""
    try:
        b_uuid = uuid.UUID(booking_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid booking ID format")

    booking = booking_repository.get_booking_by_id(db, b_uuid)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    target_enum = next((s for s in BookingStatus if s.value.lower() == req.next_status.strip().lower()), None)
    if not target_enum:
        raise HTTPException(status_code=400, detail=f"Invalid booking status '{req.next_status}'")

    current_status = booking.status
    if isinstance(current_status, str):
        try:
            current_enum = BookingStatus(current_status)
        except ValueError:
            current_enum = BookingStatus.REQUESTED
    else:
        current_enum = current_status

    allowed_next = VALID_TRANSITIONS.get(current_enum, [])

    if target_enum not in allowed_next:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Illegal state transition from {current_enum.value} to {target_enum.value}"
        )

    updated = booking_repository.update_booking_status(db, booking, target_enum, reason=req.reason)

    audit_repository.create_audit_log(
        db, actor_id=admin.id, actor_email=admin.email, actor_role=admin.role,
        action=f"Updated Booking #{booking.id} Status from {current_enum.value} to {target_enum.value}",
        target_resource=str(booking.id),
        metadata_json={"reason": req.reason or "Admin Override"}
    )

    return _serialize_admin_booking(updated)


@router.post("/{booking_id}/reassign")
def reassign_provider(
    booking_id: str,
    req: ProviderReassignRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("bookings:manage"))
):
    """Reassign provider for an active booking or emergency dispatch."""
    try:
        b_uuid = uuid.UUID(booking_id)
        p_uuid = uuid.UUID(req.new_provider_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    booking = booking_repository.get_booking_by_id(db, b_uuid)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    provider = db.query(Provider).filter(Provider.user_id == p_uuid).first()
    if not provider:
        raise HTTPException(status_code=404, detail="New provider not found")

    booking.provider_id = p_uuid
    booking.status = BookingStatus.ASSIGNED

    timeline_event = {
        "event": f"Reassigned to provider {provider.full_name}",
        "reason": req.reason or "Admin Reassignment",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    timeline = list(booking.timeline or [])
    timeline.append(timeline_event)
    booking.timeline = timeline

    db.commit()

    # Automated Notification Trigger: Provider Assigned
    try:
        from app.services.notification import notify_booking_event
        notify_booking_event(
            db,
            booking,
            "booking.assigned",
            extra_context={"notes": f"Assigned to {provider.full_name}. {req.reason or ''}".strip()},
        )
    except Exception as exc:
        pass

    # Realtime notification to assigned provider
    try:
        from app.core.websockets import broadcast_realtime
        channels = ["dashboard", "bookings", f"booking_{booking.id}", f"provider_{p_uuid}", f"user_{p_uuid}"]
        if booking.customer_id:
            channels.extend([f"customer_{booking.customer_id}", f"user_{booking.customer_id}"])
        
        service_title = booking.service.name if booking.service else "Home Service"
        ref = getattr(booking, "booking_reference", None) or str(booking.id)[:8].upper()
        sched_time = str(booking.scheduled_time) if booking.scheduled_time else ""
        booking_data = {
            "id": str(booking.id),
            "booking_reference": ref,
            "service_name": service_title,
            "scheduled_date": str(booking.scheduled_date),
            "scheduled_time": sched_time,
            "address": booking.address_line1 or "",
            "total_price": float(booking.total_price) if booking.total_price else 0.0,
            "status": str(booking.status),
        }
        broadcast_realtime(channels, {
            "type": "BOOKING_ASSIGNED",
            "event": "booking.assigned",
            "event_type": "booking.assigned",
            "booking_id": str(booking.id),
            "status": str(booking.status),
            "booking": booking_data,
            "data": booking_data,
        })
    except Exception as exc:
        logger.warning(f"[ReassignProvider] Realtime broadcast error: {exc}")

    return {"status": "success", "message": f"Booking {booking_id} reassigned to {provider.full_name}"}


# =========================================================================
# CUSTOMER FACING BOOKING ROUTER (App compatibility)
# =========================================================================

customer_bookings_router = APIRouter(prefix="/customer/bookings", tags=["Customer Booking Flow"])

class CustomerDirectBookingRequest(BookingCreateRequest):
    scheduled_date: Optional[str] = None


@customer_bookings_router.post("/")
def create_customer_direct_booking(
    req: CustomerDirectBookingRequest,
    db: Session = Depends(get_db),
    current_customer: Customer = Depends(get_current_customer)
):
    """
    Direct Booking Creation for Customers via Mobile/Web clients.
    """
    from app.models.service import Service

    try:
        s_uuid = uuid.UUID(req.service_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid service ID")

    service = db.query(Service).filter(Service.id == s_uuid, Service.is_active == True).first()
    if not service:
        raise HTTPException(status_code=404, detail="Selected service is unavailable or inactive.")

    resolved_address = (req.address or "").strip()
    if not resolved_address and current_customer.phone:
        resolved_address = "Sector 62, Noida, Uttar Pradesh"

    if not resolved_address:
        raise HTTPException(status_code=400, detail="Service location address is required to place a booking.")

    matched_provider = None
    if req.provider_id:
        try:
            p_uuid = uuid.UUID(req.provider_id)
            matched_provider = (
                db.query(Provider)
                .filter(Provider.user_id == p_uuid, Provider.is_verified == True)
                .first()
            )
        except ValueError:
            pass

    if not matched_provider:
        all_verified = (
            db.query(Provider)
            .filter(Provider.is_verified == True)
            .all()
        )
        for p in all_verified:
            p_user = db.query(User).filter(User.id == p.user_id, User.is_active == True).first()
            if p_user:
                matched_provider = p
                break

    try:
        date_part = req.scheduled_date or ""
        time_part = req.scheduled_time or "10:00"
        sched_dt = datetime.fromisoformat(f"{date_part}T{time_part}:00") if date_part else (
            datetime.now(timezone.utc) + timedelta(hours=24)
        )
    except (ValueError, TypeError):
        sched_dt = datetime.now(timezone.utc) + timedelta(hours=24)

    total_price = float(service.base_price if service.base_price is not None else 499.0)
    new_booking = Booking(
        id=uuid.uuid4(),
        customer_id=current_customer.id,
        service_id=service.id,
        provider_id=matched_provider.user_id if matched_provider else None,
        status="Assigned" if matched_provider else "Requested",
        payment_method="COD",
        payment_status="Pending",
        scheduled_time=sched_dt,
        address=resolved_address,
        total_price=Decimal(str(total_price)),
        emergency_flag=None,
        timeline=[{
            "event": "Booking Requested by Customer",
            "reason": "Customer Booking via App",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }] + ([{
            "event": f"Assigned to Provider {matched_provider.full_name}",
            "reason": "Smart Matching — Verified Provider",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }] if matched_provider else []),
        created_at=datetime.now(timezone.utc),
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    # Generate secure START OTP
    secure_otp = generate_secure_otp(new_booking.id, "START", db)
    new_booking.otp_code = secure_otp.otp_code

    # Create initial BookingPayment record
    init_payment = BookingPayment(
        id=uuid.uuid4(),
        booking_id=new_booking.id,
        customer_id=current_customer.id,
        provider_id=matched_provider.user_id if matched_provider else None,
        payment_method="COD",
        agreed_amount=Decimal(str(total_price)),
        status="Pending",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(init_payment)
    db.commit()
    db.refresh(new_booking)

    # Automated Notification Trigger: Booking Confirmed
    try:
        from app.services.notification import notify_booking_event
        notify_booking_event(db, new_booking, "booking.confirmed")
    except Exception as exc:
        pass

    return {
        "id": str(new_booking.id),
        "booking_reference": f"BK-{str(new_booking.id)[:8].upper()}",
        "customer_name": current_customer.full_name or "Customer",
        "service_name": service.name,
        "category": service.category,
        "subcategory": service.subcategory or "",
        "provider_name": matched_provider.full_name if matched_provider else "Being Assigned",
        "status": str(new_booking.status),
        "payment_method": "COD",
        "payment_status": "Pending",
        "scheduled_date": sched_dt.strftime("%d %b %Y"),
        "scheduled_time": sched_dt.strftime("%I:%M %p"),
        "total_amount": float(new_booking.total_price),
        "service_address": new_booking.address,
        "message": (
            f"Booking confirmed and assigned to {matched_provider.full_name}."
            if matched_provider else "Booking received. Finding best provider."
        ),
    }


@router.get("/{booking_id}/location")
def get_admin_booking_location(
    booking_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """
    Get live location and route monitoring data for a booking.
    Enforces Admin RBAC so only authorized admins can monitor dispatch locations.
    """
    from app.models.provider import Provider, ProviderLocation

    booking = None
    try:
        b_uuid = uuid.UUID(booking_id)
        booking = db.query(Booking).filter(Booking.id == b_uuid).first()
    except ValueError:
        booking = db.query(Booking).filter(Booking.booking_reference == booking_id).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    provider_info = None
    if booking.provider_id:
        p = db.query(Provider).filter(Provider.user_id == booking.provider_id).first()
        if p:
            prov_phone = getattr(p, 'phone', None)
            provider_info = {
                "id": str(p.user_id),
                "full_name": p.full_name,
                "phone": prov_phone or "+91 98765 43210",
                "photo_url": getattr(p, 'photo_url', None) or f"https://api.dicebear.com/7.x/avataaars/svg?seed={p.full_name}",
                "category": getattr(p, 'category', 'Services'),
                "experience_years": getattr(p, 'experience_years', 5),
                "rating": 4.9,
                "is_verified": getattr(p, 'is_verified', True),
                "service_area": getattr(p, 'service_area', 'Delhi NCR'),
            }

    loc = None
    if booking.provider_id:
        loc = db.query(ProviderLocation).filter(
            ProviderLocation.provider_id == booking.provider_id
        ).first()

    provider_loc_data = None
    if loc:
        provider_loc_data = {
            "latitude": float(loc.latitude),
            "longitude": float(loc.longitude),
            "heading": float(loc.heading) if loc.heading is not None else None,
            "speed": float(loc.speed) if loc.speed is not None else None,
            "accuracy": float(loc.accuracy) if loc.accuracy is not None else None,
            "is_active": loc.is_active,
            "updated_at": loc.updated_at.isoformat() if loc.updated_at else None,
        }

    # Customer location from booking
    c_lat = 28.6280
    c_lng = 77.3649
    if booking.timeline:
        for item in reversed(booking.timeline):
            if isinstance(item, dict) and item.get("event") == "Customer Coordinates Updated":
                if item.get("latitude") is not None and item.get("longitude") is not None:
                    c_lat = float(item["latitude"])
                    c_lng = float(item["longitude"])
                    break

    customer_loc = {
        "latitude": c_lat,
        "longitude": c_lng,
        "address": booking.address or "Sector 62, Noida",
        "city": "Noida",
    }

    return {
        "booking_id": str(booking.id),
        "booking_reference": booking.booking_reference,
        "status": str(booking.status.value if hasattr(booking.status, "value") else booking.status),
        "customer": {
            "id": str(booking.customer_id),
            "name": booking.customer.full_name if booking.customer else "Customer",
            "phone": booking.customer.phone if booking.customer else None,
        },
        "provider": provider_info,
        "provider_location": provider_loc_data,
        "customer_location": customer_loc,
        "service_name": booking.service_name,
        "total_price": float(booking.total_price or 0.0),
        "scheduled_time": booking.scheduled_time.isoformat() if booking.scheduled_time else "",
        "address": booking.address or "",
        "timeline": booking.timeline or [],
    }


class WarrantyClaimResolutionRequest(BaseModel):
    action: str  # "Resolved" | "Rejected"
    admin_notes: Optional[str] = None


@router.patch("/{booking_id}/warranty/resolve", response_model=Dict[str, Any])
def resolve_admin_warranty_claim(
    booking_id: str,
    req: WarrantyClaimResolutionRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("bookings:manage"))
):
    """Admin resolves or rejects a customer-raised warranty claim."""
    try:
        b_uuid = uuid.UUID(booking_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid booking ID format")

    warranty = db.query(BookingWarranty).filter(BookingWarranty.booking_id == b_uuid).first()
    if not warranty:
        raise HTTPException(status_code=404, detail="No warranty found for this booking")

    action_norm = req.action.capitalize()
    if action_norm not in ["Resolved", "Rejected"]:
        raise HTTPException(status_code=400, detail="Action must be 'Resolved' or 'Rejected'")

    warranty.claim_status = action_norm
    warranty.claim_resolved_at = datetime.now(timezone.utc)
    if req.admin_notes:
        warranty.claim_notes = req.admin_notes.strip()

    # Append audit entry to booking timeline
    booking = db.query(Booking).filter(Booking.id == b_uuid).first()
    if booking:
        tl = list(booking.timeline or [])
        tl.append({
            "event": f"Warranty Claim {action_norm}",
            "reason": req.admin_notes or f"Claim marked as {action_norm} by Admin",
            "admin": admin.email,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        booking.timeline = tl

    db.commit()
    db.refresh(warranty)
    return format_warranty(warranty)
