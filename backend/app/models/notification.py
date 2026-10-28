import uuid
from typing import Optional, Any
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.base import Base


class NotificationLog(Base):
    """
    Durable record of notification events dispatched across Email and WhatsApp.
    Ensures independent delivery tracking, idempotency, retry safety, and auditability.
    """
    __tablename__ = "notification_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    booking_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("bookings.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    booking_reference: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, index=True
    )
    customer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    event_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )  # e.g. booking.confirmed, booking.accepted, payment.verified
    channel: Mapped[str] = mapped_column(
        String(20), nullable=False, index=True
    )  # 'email' or 'whatsapp'
    recipient: Mapped[str] = mapped_column(
        String(255), nullable=False
    )  # email address or validated phone number
    delivery_status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="Pending", index=True
    )  # 'Sent', 'Delivered', 'Failed', 'Unconfigured', 'Pending'
    idempotency_key: Mapped[str] = mapped_column(
        String(128), unique=True, index=True, nullable=False
    )
    retry_count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )
    last_attempt_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    provider_message_id: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    error_message: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True
    )
    metadata_json: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    booking = relationship("Booking", foreign_keys=[booking_id])
    customer = relationship("Customer", foreign_keys=[customer_id])
