import uuid
from datetime import datetime, date, time
from decimal import Decimal
from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    Numeric,
    Boolean,
    Date,
    Time,
    DateTime,
    ForeignKey,
    TypeDecorator,
    CHAR,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.core.database import Base


class GUID(TypeDecorator):
    """
    Platform-independent GUID type.
    Uses PostgreSQL's native UUID type, otherwise uses CHAR(36), storing as stringified hex.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return value if isinstance(value, uuid.UUID) else uuid.UUID(str(value))
        else:
            if isinstance(value, uuid.UUID):
                return str(value)
            else:
                return str(uuid.UUID(str(value)))

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(str(value))


class Provider(Base):
    __tablename__ = "providers"

    # Primary key links 1-to-1 with USERS.user_id when auth is merged
    user_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(255), nullable=False)
    photo_url = Column(String(1024), nullable=True)
    category = Column(String(100), nullable=True)
    skills = Column(Text, nullable=True)
    experience_years = Column(Integer, default=0, nullable=False)
    base_price = Column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    service_area = Column(String(255), nullable=True)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Reliability and Performance Metrics (0.00 - 100.00)
    reliability_score = Column(Numeric(5, 2), default=Decimal("100.00"), nullable=False)
    acceptance_rate = Column(Numeric(5, 2), default=Decimal("100.00"), nullable=False)
    cancellation_rate = Column(Numeric(5, 2), default=Decimal("0.00"), nullable=False)
    no_show_rate = Column(Numeric(5, 2), default=Decimal("0.00"), nullable=False)
    on_time_rate = Column(Numeric(5, 2), default=Decimal("100.00"), nullable=False)
    response_time_score = Column(Numeric(5, 2), default=Decimal("100.00"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    certificates = relationship("Certificate", back_populates="provider", cascade="all, delete-orphan")
    availability_slots = relationship("Availability", back_populates="provider", cascade="all, delete-orphan")
    services = relationship("ProviderService", back_populates="provider", cascade="all, delete-orphan")


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    provider_id = Column(GUID(), ForeignKey("providers.user_id", ondelete="CASCADE"), nullable=False)
    document_url = Column(String(1024), nullable=False)
    certificate_type = Column(String(100), nullable=False)
    verification_status = Column(String(50), default="PENDING", nullable=False)  # PENDING, VERIFIED, REJECTED
    verified_by = Column(GUID(), nullable=True)  # Admin UUID
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    verified_at = Column(DateTime, nullable=True)

    provider = relationship("Provider", back_populates="certificates")


class Availability(Base):
    __tablename__ = "availability"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    provider_id = Column(GUID(), ForeignKey("providers.user_id", ondelete="CASCADE"), nullable=False)
    slot_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(String(50), default="FREE", nullable=False)  # FREE, RESERVED, BOOKED, UNAVAILABLE
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    provider = relationship("Provider", back_populates="availability_slots")


class ProviderService(Base):
    __tablename__ = "provider_services"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    provider_id = Column(GUID(), ForeignKey("providers.user_id", ondelete="CASCADE"), nullable=False)
    
    # TODO: add FK to services after catalog merge
    service_id = Column(GUID(), nullable=False)
    
    price = Column(Numeric(10, 2), nullable=False)
    duration_minutes = Column(Integer, default=60, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    provider = relationship("Provider", back_populates="services")
