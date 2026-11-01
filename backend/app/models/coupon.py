import uuid
from decimal import Decimal
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Numeric,
    Integer,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from app.models.base import Base, GUID


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
    discount_type = Column(String(20), nullable=False, default="FIXED")  # "FIXED" or "PERCENTAGE"
    discount_value = Column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    max_discount_amount = Column(Numeric(10, 2), nullable=True)
    min_order_amount = Column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    is_active = Column(Boolean, default=True, nullable=False)
    valid_from = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    valid_until = Column(DateTime(timezone=True), nullable=True)
    max_uses = Column(Integer, nullable=True)  # Global maximum redemptions (None = unlimited)
    max_uses_per_customer = Column(Integer, default=1, nullable=False)
    applicable_categories = Column(JSON, nullable=True)  # List of categories or None for all
    applicable_services = Column(JSON, nullable=True)  # List of service ID strings or None for all
    is_spin_reward = Column(Boolean, default=False, nullable=False)
    customer_id = Column(GUID(), ForeignKey("customers.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    redemptions = relationship("CouponRedemption", back_populates="coupon", cascade="all, delete-orphan")
    customer = relationship("Customer", foreign_keys=[customer_id])


class CouponRedemption(Base):
    __tablename__ = "coupon_redemptions"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    coupon_id = Column(GUID(), ForeignKey("coupons.id", ondelete="CASCADE"), nullable=False, index=True)
    customer_id = Column(GUID(), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, index=True)
    booking_id = Column(GUID(), ForeignKey("bookings.id", ondelete="SET NULL"), nullable=True, index=True)
    combined_booking_id = Column(GUID(), ForeignKey("combined_bookings.id", ondelete="SET NULL"), nullable=True, index=True)
    discount_applied = Column(Numeric(10, 2), nullable=False)
    order_amount_before_discount = Column(Numeric(10, 2), nullable=False)
    final_amount = Column(Numeric(10, 2), nullable=False)
    redeemed_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    coupon = relationship("Coupon", back_populates="redemptions")
    customer = relationship("Customer", foreign_keys=[customer_id])
    booking = relationship("Booking", foreign_keys=[booking_id])
    combined_booking = relationship("CombinedBooking", foreign_keys=[combined_booking_id])

