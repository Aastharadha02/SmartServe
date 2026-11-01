import uuid
from datetime import datetime, date, time
from decimal import Decimal
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


# ==========================================
# PROVIDER SCHEMAS
# ==========================================

class ProviderBase(BaseModel):
    full_name: str = Field(..., max_length=255)
    photo_url: Optional[str] = Field(None, max_length=1024)
    category: Optional[str] = Field(None, max_length=100)
    skills: Optional[str] = None
    experience_years: int = Field(0, ge=0)
    base_price: Decimal = Field(Decimal("0.00"), ge=Decimal("0.00"))
    service_area: Optional[str] = Field(None, max_length=255)


class ProviderProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=255)
    photo_url: Optional[str] = Field(None, max_length=1024)
    category: Optional[str] = Field(None, max_length=100)
    skills: Optional[str] = None
    experience_years: Optional[int] = Field(None, ge=0)
    base_price: Optional[Decimal] = Field(None, ge=Decimal("0.00"))
    service_area: Optional[str] = Field(None, max_length=255)


class ProviderProfileResponse(ProviderBase):
    user_id: uuid.UUID
    is_verified: bool
    reliability_score: Decimal
    acceptance_rate: Decimal
    cancellation_rate: Decimal
    no_show_rate: Decimal
    on_time_rate: Decimal
    response_time_score: Decimal
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProviderMetricsResponse(BaseModel):
    user_id: uuid.UUID
    reliability_score: Decimal
    acceptance_rate: Decimal
    cancellation_rate: Decimal
    no_show_rate: Decimal
    on_time_rate: Decimal
    response_time_score: Decimal

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# CERTIFICATE SCHEMAS
# ==========================================

class CertificateCreate(BaseModel):
    document_url: str = Field(..., max_length=1024, description="URL to the uploaded certificate document")
    certificate_type: str = Field(..., max_length=100, description="Type of document, e.g., Licence, ID, Diploma")


class CertificateResponse(BaseModel):
    id: uuid.UUID
    provider_id: uuid.UUID
    document_url: str
    certificate_type: str
    verification_status: str
    verified_by: Optional[uuid.UUID] = None
    uploaded_at: datetime
    verified_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# AVAILABILITY SCHEMAS
# ==========================================

class AvailabilityCreate(BaseModel):
    slot_date: date = Field(..., description="Date of the available slot")
    start_time: time = Field(..., description="Start time of the slot")
    end_time: time = Field(..., description="End time of the slot")


class AvailabilityResponse(BaseModel):
    id: uuid.UUID
    provider_id: uuid.UUID
    slot_date: date
    start_time: time
    end_time: time
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AvailabilityUpdate(BaseModel):
    status: Optional[str] = Field(None, description="Updated status: FREE or UNAVAILABLE")
    start_time: Optional[time] = None
    end_time: Optional[time] = None


# ==========================================
# PROVIDER SERVICE SCHEMAS
# ==========================================

class ProviderServiceCreate(BaseModel):
    service_id: uuid.UUID = Field(..., description="Target service UUID")
    price: Decimal = Field(..., ge=Decimal("0.00"), description="Service customized rate")
    duration_minutes: int = Field(60, ge=15, description="Estimated duration in minutes")
    active: bool = Field(True, description="Active status of this service offering")


class ProviderServiceUpdate(BaseModel):
    price: Optional[Decimal] = Field(None, ge=Decimal("0.00"))
    duration_minutes: Optional[int] = Field(None, ge=15)
    active: Optional[bool] = None


class ProviderServiceResponse(BaseModel):
    id: uuid.UUID
    provider_id: uuid.UUID
    service_id: uuid.UUID
    price: Decimal
    duration_minutes: int
    active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProviderServiceCatalogResponse(BaseModel):
    id: uuid.UUID
    provider_id: uuid.UUID
    service_id: uuid.UUID
    price: Decimal
    duration_minutes: int
    active: bool
    service_name: Optional[str] = "Home Service"
    category: Optional[str] = "General"
    subcategory: str
    base_price: Decimal
    is_emergency_eligible: bool
    distinct_features: Optional[Any] = None
    suggested_addons: Optional[Any] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProviderDashboardStatsResponse(BaseModel):
    today_bookings_count: int
    active_jobs_count: int
    completed_jobs_count: int
    pending_requests_count: int
    total_earnings: Decimal
    pipeline_count: int
    urgent_alerts_count: int
    recent_activity: List[Dict[str, Any]]


class ProviderProfileTrustResponse(BaseModel):
    user_id: uuid.UUID
    full_name: str
    email: str
    phone: Optional[str] = None
    photo_url: Optional[str] = None
    category: Optional[str] = None
    skills: Optional[str] = None
    experience_years: int
    base_price: Decimal
    service_area: Optional[str] = None
    is_verified: bool
    reliability_score: Decimal
    acceptance_rate: Decimal
    cancellation_rate: Decimal
    no_show_rate: Decimal
    on_time_rate: Decimal
    response_time_score: Decimal
    completed_jobs_count: int
    certificates_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# PROVIDER APPLICATION STATUS SCHEMA
# ==========================================

class DocumentStatusItem(BaseModel):
    certificate_type: str
    verification_status: str  # PENDING, Verified, Rejected, Correction Requested
    document_number: Optional[str] = None
    uploaded_at: Optional[datetime] = None
    verified_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ProviderStatusResponse(BaseModel):
    """Returned by GET /providers/me/status — accessible to ALL authenticated providers."""
    provider_id: uuid.UUID
    full_name: str
    email: str
    category: Optional[str] = None
    is_verified: bool
    # Overall status string: "Pending", "Verified", "Rejected", "Correction Requested"
    verification_status: str
    documents_submitted: int
    documents_verified: int
    documents_rejected: int
    documents: List[DocumentStatusItem]
    rejection_reason: Optional[str] = None
    correction_instructions: Optional[str] = None
    submitted_at: Optional[datetime] = None
    verified_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ProviderResubmitDocumentItem(BaseModel):
    certificate_type: str
    document_url: str
    document_number: Optional[str] = None
    description: Optional[str] = None


class ProviderResubmitRequest(BaseModel):
    updated_documents: Optional[List[ProviderResubmitDocumentItem]] = []
    notes: Optional[str] = None


# ==========================================
# PROVIDER BOOKING SCHEMAS
# ==========================================

class ProviderBookingResponse(BaseModel):
    id: uuid.UUID
    booking_reference: str
    customer_id: uuid.UUID
    customer_name: str
    customer_phone: Optional[str] = None
    service_id: uuid.UUID
    service_name: Optional[str] = "Home Service"
    category: Optional[str] = "General"
    status: str
    payment_method: str = "COD"
    payment_status: str
    scheduled_time: datetime
    scheduled_date: str
    address: str
    total_price: Decimal
    otp_code: Optional[str] = None
    emergency_flag: Optional[str] = None
    customer_notes: Optional[str] = None
    before_photos: Optional[List[str]] = None
    after_photos: Optional[List[str]] = None
    timeline: Optional[List[Dict[str, Any]]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BookingStatusUpdatePayload(BaseModel):
    status: Optional[str] = Field(None, description="Target booking status (Accepted, Rejected, Started, Completed, On The Way, Arrived)")
    next_status: Optional[str] = Field(None, description="Alternative target status field")
    reason: Optional[str] = Field(None, description="Reason for status change")
    otp_code: Optional[str] = Field(None, description="Customer OTP verification code")

    @property
    def target_status(self) -> str:
        return self.status or self.next_status or ""


class BookingStartPayload(BaseModel):
    otp_code: Optional[str] = Field(None, description="Customer 4-digit start OTP verification code")


class BookingCompletePayload(BaseModel):
    otp_code: Optional[str] = Field(None, description="Customer 4-digit completion OTP verification code")
    notes: Optional[str] = Field(None, description="Optional completion notes")


class CashCollectionReportPayload(BaseModel):
    reported_amount: Decimal = Field(..., description="Cash amount collected from customer", ge=Decimal("0.00"))
    notes: Optional[str] = Field(None, description="Optional notes regarding the collection")


class ProviderPaymentReportResponse(BaseModel):
    payment_id: str
    booking_id: str
    booking_reference: str
    agreed_amount: float
    reported_amount: float
    status: str
    discrepancy_flag: bool
    discrepancy_amount: float
    collected_at: Optional[str] = None
    message: str


class BookingRejectPayload(BaseModel):
    reason: Optional[str] = Field(None, description="Reason for declining the booking request")



from app.schemas.support import TicketMessageResponse

class ProviderTicketCreateRequest(BaseModel):
    subject: str
    description: str
    booking_id: Optional[str] = None
    category: Optional[str] = "General Inquiry"
    priority: str = "Medium"
    image_evidence_url: Optional[str] = None
