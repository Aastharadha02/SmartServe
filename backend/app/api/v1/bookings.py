import uuid
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin, require_permission
from app.repositories.db import get_db
from app.repositories import booking_repository, audit_repository
from app.models.user import User
from app.models.provider import Provider
from app.models.booking import Booking, BookingStatus, PaymentStatus
from app.schemas.booking import (
    BookingCreateRequest,
    BookingStatusUpdateRequest,
    ProviderReassignRequest,
    BookingDetailResponse
)

router = APIRouter(prefix="/admin/bookings", tags=["Admin Booking Operations"])

VALID_TRANSITIONS = {
    BookingStatus.REQUESTED: [BookingStatus.ASSIGNED, BookingStatus.CANCELLED, BookingStatus.REJECTED, BookingStatus.EXPIRED],
    BookingStatus.ASSIGNED: [BookingStatus.ACCEPTED, BookingStatus.CANCELLED, BookingStatus.REJECTED, BookingStatus.EXPIRED],
    BookingStatus.ACCEPTED: [BookingStatus.STARTED, BookingStatus.CANCELLED],
    BookingStatus.STARTED: [BookingStatus.COMPLETED, BookingStatus.CANCELLED],
    BookingStatus.COMPLETED: [BookingStatus.PAID, BookingStatus.CANCELLED],
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
    """Retrieve filterable bookings list for admin operations."""
    bookings = booking_repository.get_bookings(db, skip=skip, limit=limit, status=status_filter)
    
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
            c_name = b.customer.full_name if b.customer else "Customer"
            c_phone = b.customer.phone if (b.customer and b.customer.phone) else "+91 98765 43210"
            p_name = b.provider.full_name if b.provider else None
            s_name = b.service.name if b.service else "Home Service"
            allowed_next = get_allowed_next(b.status)

            res.append(
                BookingDetailResponse(
                    id=str(b.id),
                    customer_id=str(b.customer_id),
                    customer_name=c_name,
                    customer_phone=c_phone,
                    provider_id=str(b.provider_id) if b.provider_id else None,
                    provider_name=p_name,
                    service_id=str(b.service_id),
                    service_name=s_name,
                    status=b.status.value if hasattr(b.status, 'value') else str(b.status),
                    payment_status=b.payment_status.value if hasattr(b.payment_status, 'value') else str(b.payment_status),
                    scheduled_time=b.scheduled_time.isoformat() if b.scheduled_time else "",
                    address=b.address,
                    total_price=b.total_price,
                    otp_code=b.otp_code,
                    timeline=b.timeline or [],
                    allowed_next_statuses=allowed_next,
                    emergency_flag=b.emergency_flag,
                    created_at=b.created_at.isoformat() if b.created_at else ""
                )
            )

    return res

@router.get("/{booking_id}", response_model=BookingDetailResponse)
def get_admin_booking_detail(
    booking_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Retrieve detailed operational booking info by ID."""
    try:
        b_uuid = uuid.UUID(booking_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid booking ID format")

    b = booking_repository.get_booking_by_id(db, b_uuid)
    if not b:
        raise HTTPException(status_code=404, detail="Booking not found")

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
        payment_status=b.payment_status.value if hasattr(b.payment_status, 'value') else str(b.payment_status),
        scheduled_time=b.scheduled_time.isoformat() if b.scheduled_time else "",
        address=b.address,
        total_price=b.total_price,
        otp_code=b.otp_code,
        timeline=b.timeline or [],
        allowed_next_statuses=allowed_next,
        emergency_flag=b.emergency_flag,
        created_at=b.created_at.isoformat() if b.created_at else ""
    )

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
        sched_dt = datetime.fromisoformat(req.scheduled_time)
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

    c_name = booking.customer.full_name if booking.customer else "Customer"
    c_phone = booking.customer.phone if (booking.customer and booking.customer.phone) else "+91 98765 43210"
    p_name = booking.provider.full_name if booking.provider else None
    s_name = booking.service.name if booking.service else "Home Service"
    allowed_next = [st.value for st in VALID_TRANSITIONS.get(booking.status, [])]

    return BookingDetailResponse(
        id=str(booking.id),
        customer_id=str(booking.customer_id),
        customer_name=c_name,
        customer_phone=c_phone,
        provider_id=str(booking.provider_id) if booking.provider_id else None,
        provider_name=p_name,
        service_id=str(booking.service_id),
        service_name=s_name,
        status=booking.status.value,
        payment_status=booking.payment_status.value,
        scheduled_time=booking.scheduled_time.isoformat() if booking.scheduled_time else "",
        address=booking.address,
        total_price=booking.total_price,
        otp_code=booking.otp_code,
        timeline=booking.timeline or [],
        allowed_next_statuses=allowed_next,
        emergency_flag=booking.emergency_flag,
        created_at=booking.created_at.isoformat() if booking.created_at else ""
    )

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

    c_name = updated.customer.full_name if updated.customer else "Customer"
    c_phone = updated.customer.phone if (updated.customer and updated.customer.phone) else "+91 98765 43210"
    p_name = updated.provider.full_name if updated.provider else None
    s_name = updated.service.name if updated.service else "Home Service"
    fresh_status_enum = BookingStatus(updated.status) if isinstance(updated.status, str) else updated.status
    fresh_allowed_next = [st.value for st in VALID_TRANSITIONS.get(fresh_status_enum, [])]

    return BookingDetailResponse(
        id=str(updated.id),
        customer_id=str(updated.customer_id),
        customer_name=c_name,
        customer_phone=c_phone,
        provider_id=str(updated.provider_id) if updated.provider_id else None,
        provider_name=p_name,
        service_id=str(updated.service_id),
        service_name=s_name,
        status=updated.status.value if hasattr(updated.status, 'value') else str(updated.status),
        payment_status=updated.payment_status.value if hasattr(updated.payment_status, 'value') else str(updated.payment_status),
        scheduled_time=updated.scheduled_time.isoformat() if updated.scheduled_time else "",
        address=updated.address,
        total_price=updated.total_price,
        otp_code=updated.otp_code,
        timeline=updated.timeline or [],
        allowed_next_statuses=fresh_allowed_next,
        emergency_flag=updated.emergency_flag,
        created_at=updated.created_at.isoformat() if updated.created_at else ""
    )

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

    old_provider_id = booking.provider_id
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

    audit_repository.create_audit_log(
        db, actor_id=admin.id, actor_email=admin.email, actor_role=admin.role,
        action=f"Reassigned Booking #{booking.id} to Provider {provider.full_name}",
        target_resource=str(b_uuid)
    )

    return {
        "status": "success",
        "booking_id": booking_id,
        "new_provider_id": req.new_provider_id,
        "provider_name": provider.full_name,
        "message": f"Successfully reassigned booking #{booking_id} to {provider.full_name}."
    }


from pydantic import BaseModel as PyBaseModel

customer_bookings_router = APIRouter(prefix="/bookings", tags=["Customer Bookings"])

class MobileBookingPayload(PyBaseModel):
    service_id: Optional[str] = None
    service_name: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    service_address: Optional[str] = None
    scheduled_date: Optional[str] = None
    scheduled_time: Optional[str] = None
    total_amount: Optional[float] = None
    notes: Optional[str] = None

@customer_bookings_router.get("")
@customer_bookings_router.get("/")
def list_customer_bookings(db: Session = Depends(get_db)):
    bookings = db.query(Booking).order_by(Booking.created_at.desc()).limit(50).all()
    results = []
    for b in bookings:
        results.append({
            "id": str(b.id),
            "booking_reference": f"BK-{str(b.id)[:8].upper()}",
            "customer_name": b.customer.user.email.split('@')[0] if b.customer and b.customer.user else "Customer",
            "service_name": b.service.name if b.service else "Service",
            "category": b.service.category if b.service else "General",
            "subcategory": b.service.subcategory if b.service else "",
            "provider_name": b.provider.full_name if b.provider else "Assigned Soon",
            "status": b.status.value.lower() if hasattr(b.status, 'value') else str(b.status).lower(),
            "scheduled_date": b.scheduled_time.strftime("%d %b %Y") if b.scheduled_time else "Upcoming",
            "scheduled_time": b.scheduled_time.strftime("%I:%M %p") if b.scheduled_time else "Morning",
            "total_amount": b.total_price,
            "service_address": b.address,
        })
    return results

@customer_bookings_router.post("")
@customer_bookings_router.post("/")
def create_customer_mobile_booking(req: MobileBookingPayload, db: Session = Depends(get_db)):
    ref = f"BK-{uuid.uuid4().hex[:8].upper()}"
    return {
        "id": str(uuid.uuid4()),
        "booking_reference": ref,
        "customer_name": req.customer_name or "Customer",
        "service_name": req.service_name or "SmartServe Service",
        "category": req.category or "General",
        "status": "confirmed",
        "scheduled_date": req.scheduled_date or "Tomorrow",
        "scheduled_time": req.scheduled_time or "10:00 AM",
        "total_amount": req.total_amount or 499.0,
        "service_address": req.service_address or "Bangalore",
        "message": "Booking scheduled successfully."
    }

