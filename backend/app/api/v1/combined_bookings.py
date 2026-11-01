import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_customer
from app.models.customer import Customer, CombinedBooking, CombinedBookingItem
from app.models.service import Service
from app.schemas.customer_schemas import (
    CombinedBookingEstimatePayload,
    CombinedBookingEstimateResponse,
    CombinedBookingEstimateItem,
    CombinedBookingCreatePayload,
    CombinedBookingDetail,
    CombinedBookingItemDetail,
    CancelBookingPayload,
)

router = APIRouter(prefix="/customer/combined-bookings", tags=["Customer Combined Bookings"])

# Bundle discount rules:
# 2 services -> 5% discount
# 3+ services -> 10% discount
BUNDLE_DISCOUNT_RULES = {
    2: 0.05,
    3: 0.10,
}


def compute_bundle_discount_rate(item_count: int) -> float:
    if item_count >= 3:
        return 0.10
    if item_count == 2:
        return 0.05
    return 0.0


@router.post("/estimate", response_model=CombinedBookingEstimateResponse)
def estimate_combined_booking(
    payload: CombinedBookingEstimatePayload,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    """Calculate itemized breakdown, bundle discount, and final estimate for multiple services."""
    if len(payload.service_ids) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A combined booking estimate requires at least 2 services."
        )

    # De-duplicate while preserving order
    seen = set()
    unique_service_ids = [sid for sid in payload.service_ids if not (sid in seen or seen.add(sid))]

    items: List[CombinedBookingEstimateItem] = []
    subtotal = 0.0

    for sid in unique_service_ids:
        try:
            s_uuid = uuid.UUID(sid)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid service UUID: {sid}")

        svc = db.query(Service).filter(Service.id == s_uuid).first()
        if not svc:
            raise HTTPException(status_code=404, detail=f"Service {sid} not found in catalog")
        if not svc.is_active:
            raise HTTPException(status_code=400, detail=f"Service '{svc.name}' is currently unavailable")

        u_price = float(svc.base_price)
        subtotal += u_price
        items.append(
            CombinedBookingEstimateItem(
                service_id=str(svc.id),
                name=svc.name,
                category=svc.category,
                unit_price=u_price,
            )
        )

    discount_rate = compute_bundle_discount_rate(len(items))
    discount_applied = round(subtotal * discount_rate, 2)
    final_price = round(subtotal - discount_applied, 2)

    return CombinedBookingEstimateResponse(
        items=items,
        subtotal=round(subtotal, 2),
        discount_rate=discount_rate,
        discount_applied=discount_applied,
        final_price=final_price,
    )


@router.post("", response_model=CombinedBookingDetail)
def create_combined_booking(
    payload: CombinedBookingCreatePayload,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    """Create a unified combined service booking request."""
    if len(payload.service_ids) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A combined booking requires at least 2 services."
        )

    # Parse scheduled datetime
    from app.services.booking.eligibility_service import parse_scheduled_datetime
    try:
        parsed_sched_time = parse_scheduled_datetime(payload.scheduled_date, payload.scheduled_time)
    except Exception as e:
        parsed_sched_time = datetime.now(timezone.utc)

    # De-duplicate services
    seen = set()
    unique_service_ids = [sid for sid in payload.service_ids if not (sid in seen or seen.add(sid))]

    services_to_book = []
    subtotal = Decimal("0.00")

    for sid in unique_service_ids:
        try:
            s_uuid = uuid.UUID(sid)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid service UUID: {sid}")

        svc = db.query(Service).filter(Service.id == s_uuid).first()
        if not svc:
            raise HTTPException(status_code=404, detail=f"Service {sid} not found in catalog")
        if not svc.is_active:
            raise HTTPException(status_code=400, detail=f"Service '{svc.name}' is currently inactive")

        services_to_book.append(svc)
        subtotal += Decimal(str(svc.base_price))

    discount_rate = compute_bundle_discount_rate(len(services_to_book))
    discount_applied = Decimal(str(round(float(subtotal) * discount_rate, 2)))
    net_after_bundle = subtotal - discount_applied

    coupon_obj = None
    coupon_discount = Decimal("0.00")
    if payload.coupon_code:
        from app.services.coupon_service import validate_coupon
        is_valid, c_msg, c_disc, coupon_obj = validate_coupon(
            db=db,
            code=payload.coupon_code,
            customer_id=current_customer.id,
            subtotal=net_after_bundle,
            service_ids=[s.id for s in services_to_book],
        )
        if not is_valid:
            raise HTTPException(status_code=400, detail=c_msg)
        coupon_discount = c_disc

    final_price = max(Decimal("0.00"), net_after_bundle - coupon_discount)

    combined_booking = CombinedBooking(
        id=uuid.uuid4(),
        customer_id=current_customer.id,
        status="Requested",
        total_price=subtotal,
        discount_applied=discount_applied,
        coupon_code=coupon_obj.code if coupon_obj else None,
        coupon_discount=coupon_discount,
        final_price=final_price,
        scheduled_time=parsed_sched_time,
        address=payload.address_line1.strip(),
        customer_notes=payload.customer_notes.strip() if payload.customer_notes else None,
        payment_status="Pending",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    db.add(combined_booking)
    if coupon_obj:
        from app.services.coupon_service import redeem_coupon
        redeem_coupon(
            db=db,
            coupon_id=coupon_obj.id,
            customer_id=current_customer.id,
            subtotal=net_after_bundle,
            combined_booking_id=combined_booking.id,
            service_ids=[s.id for s in services_to_book],
        )

    # Create line items and actionable service bookings for pipeline & customer tracking
    from app.models.customer import Booking
    from app.models.provider import Provider
    import random

    items_out = []
    bundle_ref = f"CB-{str(combined_booking.id)[:8].upper()}"

    for svc in services_to_book:
        assigned_prov = None
        if payload.provider_ids and str(svc.id) in payload.provider_ids:
            try:
                assigned_prov = uuid.UUID(payload.provider_ids[str(svc.id)])
            except ValueError:
                pass

        if not assigned_prov:
            prov_match = (
                db.query(Provider)
                .filter(Provider.category.ilike(f"%{svc.category}%"))
                .first()
            )
            if not prov_match:
                prov_match = db.query(Provider).first()
            if prov_match:
                assigned_prov = prov_match.user_id

        item = CombinedBookingItem(
            id=uuid.uuid4(),
            combined_booking_id=combined_booking.id,
            service_id=svc.id,
            provider_id=assigned_prov,
            unit_price=Decimal(str(svc.base_price)),
            status="Requested",
            scheduled_time=parsed_sched_time,
        )
        db.add(item)
        items_out.append(
            CombinedBookingItemDetail(
                id=str(item.id),
                service_id=str(svc.id),
                service_name=svc.name,
                category=svc.category,
                provider_id=str(assigned_prov) if assigned_prov else None,
                unit_price=float(svc.base_price),
                status=item.status,
                scheduled_time=parsed_sched_time,
            )
        )

        # Create live Booking record so this service appears in Customer Bookings and Provider Pipeline!
        discounted_unit = round(float(svc.base_price) * (1.0 - discount_rate), 2)
        booking_otp = f"{random.randint(1000, 9999)}"
        b_entry = Booking(
            id=uuid.uuid4(),
            customer_id=current_customer.id,
            provider_id=assigned_prov,
            service_id=svc.id,
            status="Requested",
            payment_status="Pending",
            scheduled_time=parsed_sched_time,
            address=payload.address_line1.strip(),
            total_price=Decimal(str(discounted_unit)),
            otp_code=booking_otp,
            customer_notes=f"[{bundle_ref} • {int(discount_rate * 100)}% Bundle Discount] {payload.customer_notes or ''}".strip(),
            timeline=[
                {
                    "event": "Booking Created via Multi-Service Bundle",
                    "bundle_reference": bundle_ref,
                    "bundle_id": str(combined_booking.id),
                    "discount_rate": f"{int(discount_rate * 100)}%",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "actor": current_customer.full_name,
                    "role": "customer",
                }
            ],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(b_entry)

    # Update customer stats
    current_customer.total_bookings = (current_customer.total_bookings or 0) + 1
    current_customer.lifetime_spent = (current_customer.lifetime_spent or Decimal("0.00")) + final_price
    db.add(current_customer)

    db.commit()
    db.refresh(combined_booking)

    return CombinedBookingDetail(
        id=str(combined_booking.id),
        booking_reference=combined_booking.booking_reference,
        customer_id=str(current_customer.id),
        status=combined_booking.status,
        total_price=float(combined_booking.total_price),
        discount_applied=float(combined_booking.discount_applied),
        final_price=float(combined_booking.final_price),
        scheduled_time=combined_booking.scheduled_time,
        address=combined_booking.address,
        customer_notes=combined_booking.customer_notes,
        payment_status=combined_booking.payment_status,
        coupon_code=combined_booking.coupon_code,
        coupon_discount=float(combined_booking.coupon_discount or 0.0),
        items=items_out,
        created_at=combined_booking.created_at,
    )


@router.get("", response_model=List[CombinedBookingDetail])
def list_combined_bookings(
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    """Retrieve all combined bookings belonging to the authenticated customer."""
    records = (
        db.query(CombinedBooking)
        .filter(CombinedBooking.customer_id == current_customer.id)
        .order_by(CombinedBooking.created_at.desc())
        .all()
    )

    result = []
    for b in records:
        items_list = []
        for it in b.items:
            items_list.append(
                CombinedBookingItemDetail(
                    id=str(it.id),
                    service_id=str(it.service_id),
                    service_name=it.service.name if it.service else "Service",
                    category=it.service.category if it.service else "General",
                    provider_id=str(it.provider_id) if it.provider_id else None,
                    unit_price=float(it.unit_price),
                    status=it.status,
                    scheduled_time=it.scheduled_time,
                )
            )
        result.append(
            CombinedBookingDetail(
                id=str(b.id),
                booking_reference=b.booking_reference,
                customer_id=str(b.customer_id),
                status=b.status,
                total_price=float(b.total_price),
                discount_applied=float(b.discount_applied),
                final_price=float(b.final_price),
                scheduled_time=b.scheduled_time,
                address=b.address,
                customer_notes=b.customer_notes,
                payment_status=b.payment_status,
                coupon_code=b.coupon_code,
                coupon_discount=float(b.coupon_discount or 0.0),
                items=items_list,
                created_at=b.created_at,
            )
        )
    return result


@router.get("/{combined_id}", response_model=CombinedBookingDetail)
def get_combined_booking_detail(
    combined_id: str,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    """Get single combined booking detail."""
    try:
        cb_uuid = uuid.UUID(combined_id)
        query = db.query(CombinedBooking).filter(CombinedBooking.id == cb_uuid)
    except ValueError:
        query = db.query(CombinedBooking).filter(CombinedBooking.booking_reference == combined_id)

    record = query.first()
    if not record:
        raise HTTPException(status_code=404, detail="Combined booking not found")
    if record.customer_id != current_customer.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    items_list = []
    for it in record.items:
        items_list.append(
            CombinedBookingItemDetail(
                id=str(it.id),
                service_id=str(it.service_id),
                service_name=it.service.name if it.service else "Service",
                category=it.service.category if it.service else "General",
                provider_id=str(it.provider_id) if it.provider_id else None,
                unit_price=float(it.unit_price),
                status=it.status,
                scheduled_time=it.scheduled_time,
            )
        )

    return CombinedBookingDetail(
        id=str(record.id),
        booking_reference=record.booking_reference,
        customer_id=str(record.customer_id),
        status=record.status,
        total_price=float(record.total_price),
        discount_applied=float(record.discount_applied),
        final_price=float(record.final_price),
        scheduled_time=record.scheduled_time,
        address=record.address,
        customer_notes=record.customer_notes,
        payment_status=record.payment_status,
        coupon_code=record.coupon_code,
        coupon_discount=float(record.coupon_discount or 0.0),
        items=items_list,
        created_at=record.created_at,
    )


@router.post("/{combined_id}/cancel", response_model=CombinedBookingDetail)
def cancel_combined_booking(
    combined_id: str,
    payload: Optional[CancelBookingPayload] = None,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    """Cancel an active combined booking."""
    try:
        cb_uuid = uuid.UUID(combined_id)
        query = db.query(CombinedBooking).filter(CombinedBooking.id == cb_uuid)
    except ValueError:
        query = db.query(CombinedBooking).filter(CombinedBooking.booking_reference == combined_id)

    record = query.first()
    if not record:
        raise HTTPException(status_code=404, detail="Combined booking not found")
    if record.customer_id != current_customer.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    if record.status in ["Completed", "Paid", "Cancelled"]:
        raise HTTPException(status_code=400, detail=f"Cannot cancel a booking in status '{record.status}'")

    record.status = "Cancelled"
    for item in record.items:
        item.status = "Cancelled"
        db.add(item)

    db.add(record)
    db.commit()
    db.refresh(record)

    return get_combined_booking_detail(str(record.id), current_customer=current_customer, db=db)
