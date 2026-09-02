import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    Numeric,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.provider import GUID


class User(Base):
    __tablename__ = "users"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column("password_hash", String(255), nullable=False)




    role = Column(String(50), default="customer", nullable=False)  # customer, admin, provider
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    customer_profile = relationship("Customer", back_populates="user", uselist=False, cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    is_verified = Column(Boolean, default=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    lifetime_spent = Column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    total_bookings = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="customer_profile")
    bookings = relationship("Booking", back_populates="customer", cascade="all, delete-orphan")
    tickets = relationship("SupportTicket", back_populates="customer", cascade="all, delete-orphan")
    feedbacks = relationship("BookingFeedback", back_populates="customer", cascade="all, delete-orphan")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    booking_reference = Column(String(50), unique=True, index=True, nullable=False)
    customer_id = Column(GUID(), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    service_id = Column(String(100), nullable=False)
    service_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    status = Column(String(50), default="CONFIRMED", nullable=False)  # PENDING, CONFIRMED, IN_PROGRESS, COMPLETED, CANCELLED
    scheduled_date = Column(String(50), nullable=False)
    scheduled_time = Column(String(50), nullable=False)
    address_line1 = Column(Text, nullable=False)
    landmark = Column(String(255), nullable=True)
    city = Column(String(100), default="Noida", nullable=False)
    pincode = Column(String(20), default="201301", nullable=False)
    total_price = Column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    payment_method = Column(String(50), default="COD", nullable=False)
    cancellation_reason = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    customer = relationship("Customer", back_populates="bookings")
    tickets = relationship("SupportTicket", back_populates="booking")
    feedback = relationship("BookingFeedback", back_populates="booking", uselist=False, cascade="all, delete-orphan")


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    customer_id = Column(GUID(), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    booking_id = Column(GUID(), ForeignKey("bookings.id", ondelete="SET NULL"), nullable=True)
    subject = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    priority = Column(String(50), default="Normal", nullable=False)  # High, Normal, Low
    status = Column(String(50), default="OPEN", nullable=False)  # OPEN, IN_PROGRESS, RESOLVED, CLOSED
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    customer = relationship("Customer", back_populates="tickets")
    booking = relationship("Booking", back_populates="tickets")
    messages = relationship("TicketMessage", back_populates="ticket", cascade="all, delete-orphan")


class TicketMessage(Base):
    __tablename__ = "ticket_messages"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    ticket_id = Column(GUID(), ForeignKey("support_tickets.id", ondelete="CASCADE"), nullable=False)
    sender_role = Column(String(50), nullable=False)  # customer, agent, system
    sender_name = Column(String(255), nullable=False)
    message_text = Column(Text, nullable=False)
    attachment_url = Column(String(1024), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    ticket = relationship("SupportTicket", back_populates="messages")


class BookingFeedback(Base):
    __tablename__ = "booking_feedbacks"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    booking_id = Column(GUID(), ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False, unique=True)
    customer_id = Column(GUID(), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)
    review_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    booking = relationship("Booking", back_populates="feedback")
    customer = relationship("Customer", back_populates="feedbacks")


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    device_info = Column(String(255), default="Web Browser", nullable=False)
    ip_address = Column(String(100), default="127.0.0.1", nullable=False)
    last_active = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="sessions")
