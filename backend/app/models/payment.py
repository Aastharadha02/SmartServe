import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Boolean, DateTime, Numeric, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from app.models.base import Base, GUID


class PaymentStatus(str, PyEnum):
    PENDING = "Pending"
    COLLECTION_REPORTED = "Collection Reported"
    PAID = "Paid"
    REJECTED = "Rejected"
    COMPLETED = "Completed"
    FAILED = "Failed"
    REFUNDED = "Refunded"


class PaymentMethod(str, PyEnum):
    COD = "COD"


class OTPType(str, PyEnum):
    START = "START"
    COMPLETE = "COMPLETE"


class BookingPayment(Base):
    __tablename__ = "booking_payments"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    booking_id = Column(GUID(), ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False, index=True)
    customer_id = Column(GUID(), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, index=True)
    provider_id = Column(GUID(), ForeignKey("providers.user_id", ondelete="SET NULL"), nullable=True, index=True)
    payment_method = Column(String(50), default="COD", nullable=False)
    agreed_amount = Column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    reported_amount = Column(Numeric(10, 2), nullable=True)
    status = Column(String(50), default=PaymentStatus.PENDING.value, nullable=False, index=True)
    discrepancy_flag = Column(Boolean, default=False, nullable=False)
    discrepancy_amount = Column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    collected_at = Column(DateTime(timezone=True), nullable=True)
    collection_notes = Column(Text, nullable=True)
    reviewed_by_id = Column(GUID(), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reviewed_by_name = Column(String(255), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    booking = relationship("Booking", back_populates="payments", foreign_keys=[booking_id])
    customer = relationship("Customer", foreign_keys=[customer_id])
    provider = relationship("Provider", primaryjoin="BookingPayment.provider_id == Provider.user_id", foreign_keys=[provider_id])
    reviewed_by = relationship("User", foreign_keys=[reviewed_by_id])


class BookingOTP(Base):
    __tablename__ = "booking_otps"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    booking_id = Column(GUID(), ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False, index=True)
    otp_type = Column(String(20), nullable=False, index=True)  # 'START' or 'COMPLETE'
    otp_code = Column(String(20), nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)
    used_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    failed_attempts = Column(Integer, default=0, nullable=False)
    max_attempts = Column(Integer, default=5, nullable=False)
    is_locked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    booking = relationship("Booking", back_populates="otps", foreign_keys=[booking_id])
