import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# Auth Schemas
class CustomerRegisterPayload(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8)
    phone: Optional[str] = None


class CustomerLoginPayload(BaseModel):
    email: EmailStr
    password: str


class CustomerTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int = 1440
    customer_id: str
    user_id: str
    email: str
    full_name: str
    phone: Optional[str] = None


class CustomerSessionResponse(BaseModel):
    customer_id: str
    user_id: str
    email: str
    full_name: str
    phone: Optional[str] = None
    is_active: bool = True
    is_verified: bool = True
    lifetime_spent: float = 0.0
    total_bookings: int = 0
    created_at: Optional[datetime] = None


class ForgotPasswordPayload(BaseModel):
    email: EmailStr


class ResetPasswordPayload(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)


class ChangePasswordPayload(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)


# Profile Schemas
class CustomerProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


# Catalog Schemas
class AddonItem(BaseModel):
    addon_id: str
    name: str
    price: float
    description: Optional[str] = None


class ServiceProcessStep(BaseModel):
    step_number: int
    title: str
    description: str
    duration_minutes: int


class ServiceFAQ(BaseModel):
    question: str
    answer: str


class CategoryItem(BaseModel):
    id: str
    name: str
    slug: str
    icon: Optional[str] = None
    image: str
    service_count: int = 0


class ServiceItem(BaseModel):
    id: str
    name: str
    category: str
    category_slug: str
    subcategory: str
    subcategory_slug: str
    description: str
    features: List[str] = []
    base_price: float
    duration_minutes: int
    rating: float = 4.8
    review_count: int = 0
    is_emergency: bool = False
    image_url: str
    suggested_addons: List[AddonItem] = []
    process_steps: List[ServiceProcessStep] = []
    faqs: List[ServiceFAQ] = []


# Booking Schemas
class CreateBookingPayload(BaseModel):
    service_id: str
    scheduled_date: str
    scheduled_time: str
    address_line1: str = Field(..., min_length=10)
    landmark: Optional[str] = None
    city: str = "Noida"
    pincode: str = "201301"
    notes: Optional[str] = None
    addon_ids: List[str] = []
    payment_method: str = "COD"


class CancelBookingPayload(BaseModel):
    reason: str


class BookingFeedbackPayload(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    review_text: Optional[str] = None
    image_urls: List[str] = []


class BookingDetail(BaseModel):
    id: str
    booking_reference: str
    customer_id: str
    service_id: str
    service_name: str
    category: str
    status: str
    scheduled_date: str
    scheduled_time: str
    address_line1: str
    landmark: Optional[str] = None
    city: str
    pincode: str
    total_price: float
    payment_method: str
    cancellation_reason: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime


# Support Schemas
class CreateTicketPayload(BaseModel):
    subject: str = Field(..., min_length=3)
    description: str = Field(..., min_length=10)
    category: str
    booking_id: Optional[str] = None
    priority: Optional[str] = "Normal"
    image_urls: List[str] = []


class TicketMessagePayload(BaseModel):
    message_text: str = Field(..., min_length=1)
    attachment_url: Optional[str] = None


class MessageItem(BaseModel):
    id: str
    ticket_id: str
    sender_role: str
    sender_name: str
    message_text: str
    attachment_url: Optional[str] = None
    created_at: datetime


class SupportTicketDetail(BaseModel):
    id: str
    customer_id: str
    booking_id: Optional[str] = None
    subject: str
    category: str
    priority: str
    status: str
    created_at: datetime
    messages: List[MessageItem] = []


# Session Schema
class SessionListItem(BaseModel):
    id: str
    device_info: str
    ip_address: str
    last_active: datetime
    is_current: bool = False
