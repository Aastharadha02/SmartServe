import uuid
from enum import Enum as PyEnum
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base

class BookingStatus(str, PyEnum):
    REQUESTED = "Requested"
    ASSIGNED = "Assigned"
    ACCEPTED = "Accepted"
    STARTED = "Started"
    COMPLETED = "Completed"
    PAID = "Paid"
    CANCELLED = "Cancelled"
    REJECTED = "Rejected"
    EXPIRED = "Expired"

class PaymentStatus(str, PyEnum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"
    REFUNDED = "Refunded"

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False, index=True)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.user_id"), nullable=True, index=True)
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id"), nullable=False, index=True)
    
    status = Column(Enum(BookingStatus), nullable=False, default=BookingStatus.REQUESTED, index=True)
    payment_status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    
    scheduled_time = Column(DateTime(timezone=True), nullable=False)
    address = Column(String(500), nullable=False)
    total_price = Column(Float, nullable=False)
    otp_code = Column(String(10), nullable=True)
    
    timeline = Column(JSON, nullable=True, default=list) # List of status change events
    emergency_flag = Column(String(50), nullable=True)
    
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    customer = relationship("Customer", backref="bookings")
    provider = relationship("Provider", backref="bookings")
    service = relationship("Service", backref="bookings")
