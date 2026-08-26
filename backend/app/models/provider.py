import uuid
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import String, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User

class Provider(Base):
    __tablename__ = "providers"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    photo_url: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    skills: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    service_area: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    experience_years: Mapped[int] = mapped_column(default=5, nullable=False)
    base_price: Mapped[float] = mapped_column(default=499.0, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    reliability_score: Mapped[float] = mapped_column(default=98.0, nullable=False)
    acceptance_rate: Mapped[float] = mapped_column(default=95.0, nullable=False)
    on_time_rate: Mapped[float] = mapped_column(default=99.0, nullable=False)
    cancellation_rate: Mapped[float] = mapped_column(default=2.0, nullable=False)
    no_show_rate: Mapped[float] = mapped_column(default=0.0, nullable=False)
    response_time_score: Mapped[float] = mapped_column(default=95.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user: Mapped[Optional["User"]] = relationship("User", back_populates="provider")

class Certificate(Base):
    __tablename__ = "certificates"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    provider_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("providers.user_id", ondelete="CASCADE"), nullable=False
    )
    document_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    certificate_type: Mapped[str] = mapped_column(String(100), nullable=False)
    document_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    expiry_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    extracted_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_duplicate: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    verification_status: Mapped[str] = mapped_column(String(50), nullable=False, default="Pending")
    verified_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
