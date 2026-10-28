import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, EmailStr, Field, field_validator


# Auth Schemas
class CustomerRegisterPayload(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8)
    phone: Optional[str] = None
    preferences: Optional[List[str]] = None


class CustomerLoginPayload(BaseModel):
    email: EmailStr
    password: str
    totp_code: Optional[str] = None
    recovery_code: Optional[str] = None


class CustomerLocationPayload(BaseModel):
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    source: Optional[str] = "manual"

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, v):
        if v is not None and (v < -90 or v > 90):
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, v):
        if v is not None and (v < -180 or v > 180):
            raise ValueError("Longitude must be between -180 and 180")
        return v


class CustomerTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int = 1440
    customer_id: str
    user_id: str
    email: str
    full_name: str
    phone: Optional[str] = None
    requires_profile_completion: bool = False
    is_profile_complete: bool = True
    missing_profile_fields: List[str] = []
    is_new_user: bool = False
    location: Optional[Dict[str, Any]] = None


class CompleteProfilePayload(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=255)
    phone: str = Field(..., min_length=10, max_length=20)
    preferences: Optional[Union[List[str], Dict[str, Any]]] = None
    location: Optional[CustomerLocationPayload] = None


class SkipProfilePayload(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    preferences: Optional[Union[List[str], Dict[str, Any]]] = None
    location: Optional[CustomerLocationPayload] = None


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
    preferences: Optional[Union[List[str], Dict[str, Any]]] = None
    is_profile_complete: bool = True
    missing_profile_fields: List[str] = []
    location: Optional[Dict[str, Any]] = None


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
    is_key_step: Optional[bool] = False


class ServiceFeatureItem(BaseModel):
    title: str
    description: str


class ServiceMediaItem(BaseModel):
    id: Optional[str] = None
    url: str
    caption: Optional[str] = None
    media_type: Optional[str] = "image"
    is_cover: Optional[bool] = False


class ServiceFAQ(BaseModel):
    question: str
    answer: str


class SubcategorySummary(BaseModel):
    name: str
    service_count: int = 0
    active_count: int = 0


class CategoryItem(BaseModel):
    id: str
    name: str
    slug: str
    display_name: Optional[str] = None
    icon: Optional[str] = None
    image: Optional[str] = None
    order: int = 999
    subcategories_count: int = 0
    service_count: int = 0
    active_count: int = 0
    subcategories: List[SubcategorySummary] = []


class ServiceItem(BaseModel):
    id: str
    name: str
    category: str
    category_slug: str
    subcategory: str
    subcategory_slug: str
    description: Optional[str] = None
    distinct_features: List[str] = []
    features: List[str] = []
    included: List[str] = []
    excluded: List[str] = []
    highlights: List[str] = []
    base_price: float
    max_demand_increase: float = 0.0
    max_discount: float = 0.0
    duration_minutes: int = 45
    rating: float = 4.8
    review_count: int = 120
    is_emergency: bool = False
    is_emergency_eligible: bool = False
    is_active: bool = True
    image_url: Optional[str] = None
    suggested_addons: List[AddonItem] = []
    process_steps: List[ServiceProcessStep] = []
    tools_materials: List[str] = []
    customer_setup: List[str] = []
    aftercare: List[str] = []
    expected_results: List[str] = []
    important_notes: List[str] = []
    warranty: Optional[str] = None
    faqs: List[ServiceFAQ] = []
    tips: List[str] = []
    dos: List[str] = []
    donts: List[str] = []
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    keywords: List[str] = []
    service_features: List[ServiceFeatureItem] = []
    service_media: List[ServiceMediaItem] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ProviderSlotDetail(BaseModel):
    slot_id: str
    slot_date: str
    start_time: str
    end_time: str
    display_time: str
    is_available: bool = True
    available_times: List[str] = []


class EligibleProviderResponse(BaseModel):
    provider_id: str
    full_name: str
    category: Optional[str] = None
    skills: Optional[str] = None
    experience_years: int = 0
    reliability_score: float = 100.0
    acceptance_rate: float = 100.0
    service_area: Optional[str] = None
    available_slots: List[str] = []
    structured_slots: List[ProviderSlotDetail] = []
    is_available: bool = True


# Booking Schemas
class CreateBookingPayload(BaseModel):
    service_id: str
    scheduled_date: str
    scheduled_time: str
    address_line1: Optional[str] = None
    landmark: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    notes: Optional[str] = None
    addon_ids: List[str] = []
    payment_method: str = "COD"
    provider_id: Optional[str] = None


class CancelBookingPayload(BaseModel):
    reason: Optional[str] = "Cancelled by Customer"
    cancellation_reason: Optional[str] = None


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
    payment_method: str = "COD"
    payment_status: str = "Pending"
    cancellation_reason: Optional[str] = None
    notes: Optional[str] = None
    customer_notes: Optional[str] = None
    before_photos: Optional[List[str]] = None
    after_photos: Optional[List[str]] = None
    warranty: Optional[Dict[str, Any]] = None
    provider_id: Optional[str] = None
    provider_name: Optional[str] = None
    provider: Optional[Dict[str, Any]] = None
    otp_code: Optional[str] = None
    start_otp: Optional[str] = None
    completion_otp: Optional[str] = None
    emergency_flag: Optional[str] = None
    timeline: Optional[List[Dict[str, Any]]] = None
    created_at: datetime

    @field_validator("timeline", mode="before")
    @classmethod
    def normalize_timeline(cls, v):
        if isinstance(v, list):
            return [x if isinstance(x, dict) else {"event": str(x)} for x in v]
        if isinstance(v, dict):
            return [v]
        return []


# Warranty Schemas
class WarrantyClaimPayload(BaseModel):
    description: str = Field(..., min_length=5, max_length=2000)


class WarrantyCardResponse(BaseModel):
    id: str
    booking_id: str
    customer_id: str
    provider_id: Optional[str] = None
    service_name: str
    issued_at: datetime
    expires_at: datetime
    is_active: bool
    claim_status: str
    claim_description: Optional[str] = None
    claim_submitted_at: Optional[datetime] = None
    claim_resolved_at: Optional[datetime] = None
    claim_notes: Optional[str] = None
    days_remaining: int = 0


# Combined Booking Schemas
class CombinedBookingEstimateItem(BaseModel):
    service_id: str
    name: str
    category: str
    unit_price: float


class CombinedBookingEstimatePayload(BaseModel):
    service_ids: List[str] = Field(..., min_length=2)


class CombinedBookingEstimateResponse(BaseModel):
    items: List[CombinedBookingEstimateItem]
    subtotal: float
    discount_rate: float
    discount_applied: float
    final_price: float


class CombinedBookingCreatePayload(BaseModel):
    service_ids: List[str] = Field(..., min_length=2)
    scheduled_date: str
    scheduled_time: str
    address_line1: str = Field(..., min_length=5)
    city: str = "Noida"
    pincode: str = "201301"
    customer_notes: Optional[str] = None
    payment_method: str = "COD"
    provider_ids: Optional[Dict[str, str]] = None


class CombinedBookingItemDetail(BaseModel):
    id: str
    service_id: str
    service_name: str
    category: str
    provider_id: Optional[str] = None
    unit_price: float
    status: str
    scheduled_time: Optional[datetime] = None


class CombinedBookingDetail(BaseModel):
    id: str
    booking_reference: str
    customer_id: str
    status: str
    total_price: float
    discount_applied: float
    final_price: float
    scheduled_time: datetime
    address: str
    customer_notes: Optional[str] = None
    payment_status: str
    items: List[CombinedBookingItemDetail] = []
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
    description: Optional[str] = None
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
