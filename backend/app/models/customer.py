import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, String, Boolean, DateTime, Numeric, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base, GUID


class Customer(Base):
    __tablename__ = "customers"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=True)
    role = Column(String(50), default="customer", nullable=False)
    is_verified = Column(Boolean(), default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean(), default=True, nullable=False)
    lifetime_spent = Column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    total_bookings = Column(Numeric(10, 0), default=0, nullable=False)
    preferences = Column(JSON, nullable=True)

    user = relationship("User", back_populates="customer", foreign_keys=[user_id])
    bookings = relationship("Booking", back_populates="customer", cascade="all, delete-orphan")
    tickets = relationship("SupportTicket", back_populates="customer", cascade="all, delete-orphan")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    customer_id = Column(GUID(), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    provider_id = Column(GUID(), ForeignKey("providers.user_id", ondelete="CASCADE"), nullable=True)
    service_id = Column(GUID(), ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="Requested", nullable=False)
    payment_status = Column(String(50), default="Pending", nullable=False)
    scheduled_time = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    address = Column(String(500), nullable=False, default="Address on File")
    total_price = Column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    otp_code = Column(String(10), nullable=True)
    timeline = Column(JSON, nullable=True)
    emergency_flag = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    customer = relationship("Customer", back_populates="bookings", foreign_keys=[customer_id])
    provider = relationship("Provider", primaryjoin="Booking.provider_id == Provider.user_id", foreign_keys=[provider_id])
    service = relationship("Service", primaryjoin="Booking.service_id == Service.id", foreign_keys=[service_id])
    tickets = relationship("SupportTicket", back_populates="booking")
    feedback = relationship("BookingFeedback", back_populates="booking", uselist=False, cascade="all, delete-orphan")

    @property
    def booking_reference(self) -> str:
        return f"BK-{str(self.id)[:8].upper()}"

    @booking_reference.setter
    def booking_reference(self, value):
        pass

    @property
    def service_name(self) -> str:
        return self.service.name if self.service else "Home Service"

    @service_name.setter
    def service_name(self, value):
        pass

    @property
    def category(self) -> str:
        return self.service.category if self.service else "General"

    @category.setter
    def category(self, value):
        pass

    @property
    def scheduled_date(self) -> str:
        return self.scheduled_time.strftime("%Y-%m-%d") if self.scheduled_time else ""

    @scheduled_date.setter
    def scheduled_date(self, value):
        pass

    @property
    def address_line1(self) -> str:
        return self.address or ""

    @address_line1.setter
    def address_line1(self, value):
        if value:
            self.address = value

    @property
    def landmark(self) -> str:
        return ""

    @landmark.setter
    def landmark(self, value):
        pass

    @property
    def city(self) -> str:
        return "Noida"

    @city.setter
    def city(self, value):
        pass

    @property
    def pincode(self) -> str:
        return "201301"

    @pincode.setter
    def pincode(self, value):
        pass

    @property
    def payment_method(self) -> str:
        return self.payment_status or "COD"

    @payment_method.setter
    def payment_method(self, value):
        if value:
            self.payment_status = value

    @property
    def notes(self) -> str:
        return ""

    @notes.setter
    def notes(self, value):
        pass

    @property
    def cancellation_reason(self) -> str:
        return ""

    @cancellation_reason.setter
    def cancellation_reason(self, value):
        pass


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    customer_id = Column(GUID(), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    booking_id = Column(GUID(), ForeignKey("bookings.id", ondelete="SET NULL"), nullable=True)
    assigned_admin_id = Column(GUID(), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=False, default="")
    category = Column(String(100), default="General Inquiry", nullable=True)
    priority = Column(String(50), default="Normal", nullable=False)
    status = Column(String(50), default="Open", nullable=False)
    escalated_to_admin = Column(Boolean, default=False, nullable=False)
    image_evidence_url = Column(String(1024), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    customer = relationship("Customer", back_populates="tickets", foreign_keys=[customer_id])
    booking = relationship("Booking", back_populates="tickets", foreign_keys=[booking_id])
    assigned_admin = relationship("User", foreign_keys=[assigned_admin_id])
    messages = relationship("TicketMessage", back_populates="ticket", cascade="all, delete-orphan")


class TicketMessage(Base):
    __tablename__ = "ticket_messages"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    ticket_id = Column(GUID(), ForeignKey("support_tickets.id", ondelete="CASCADE"), nullable=False)
    sender_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    sender_role = Column(String(50), nullable=False)
    message_text = Column(Text, nullable=False)
    attachment_url = Column(String(1024), nullable=True)
    sender_name = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    @property
    def sender_user_id(self):
        return self.sender_id

    @sender_user_id.setter
    def sender_user_id(self, value):
        self.sender_id = value

    ticket = relationship("SupportTicket", back_populates="messages")
    sender_user = relationship("User", foreign_keys=[sender_id])


class BookingFeedback(Base):
    __tablename__ = "booking_feedbacks"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    booking_id = Column(GUID(), ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False, unique=True)
    customer_id = Column(GUID(), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Numeric(3, 2), nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    booking = relationship("Booking", back_populates="feedback")
    customer = relationship("Customer")
