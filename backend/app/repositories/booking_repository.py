import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.models.booking import Booking, BookingStatus, PaymentStatus

def create_booking(
    db: Session,
    customer_id: uuid.UUID,
    service_id: uuid.UUID,
    scheduled_time: datetime,
    address: str,
    total_price: float,
    provider_id: Optional[uuid.UUID] = None,
    emergency_flag: Optional[str] = None
) -> Booking:
    otp_code = str(uuid.uuid4().int)[:4]
    initial_event = {
        "event": "Booking Created",
        "status": BookingStatus.REQUESTED.value,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    booking = Booking(
        id=uuid.uuid4(),
        customer_id=customer_id,
        provider_id=provider_id,
        service_id=service_id,
        status=BookingStatus.REQUESTED if not provider_id else BookingStatus.ASSIGNED,
        payment_status=PaymentStatus.PENDING,
        scheduled_time=scheduled_time,
        address=address,
        total_price=total_price,
        otp_code=otp_code,
        timeline=[initial_event],
        emergency_flag=emergency_flag,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

def get_booking_by_id(db: Session, booking_id: uuid.UUID) -> Optional[Booking]:
    return db.query(Booking).filter(Booking.id == booking_id).first()

def get_bookings(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    customer_id: Optional[uuid.UUID] = None,
    provider_id: Optional[uuid.UUID] = None
) -> List[Booking]:
    query = db.query(Booking)
    if status:
        query = query.filter(Booking.status == status)
    if customer_id:
        query = query.filter(Booking.customer_id == customer_id)
    if provider_id:
        query = query.filter(Booking.provider_id == provider_id)
    return query.order_by(desc(Booking.created_at)).offset(skip).limit(limit).all()

def update_booking_status(
    db: Session,
    booking: Booking,
    next_status: BookingStatus,
    reason: Optional[str] = None
) -> Booking:
    booking.status = next_status
    booking.updated_at = datetime.now(timezone.utc)
    
    timeline_event = {
        "event": f"Status changed to {next_status.value}",
        "status": next_status.value,
        "reason": reason or "",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    timeline = list(booking.timeline or [])
    timeline.append(timeline_event)
    booking.timeline = timeline

    if next_status == BookingStatus.PAID:
        booking.payment_status = PaymentStatus.COMPLETED

    db.commit()
    db.refresh(booking)
    return booking

def count_bookings_by_status(db: Session) -> Dict[str, int]:
    results = db.query(Booking.status, func.count(Booking.id)).group_by(Booking.status).all()
    counts = {s.value.lower(): 0 for s in BookingStatus}
    for status_enum, count in results:
        if status_enum:
            counts[status_enum.value.lower()] = count
    return counts
