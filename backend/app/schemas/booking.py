from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class BookingCreateRequest(BaseModel):
    customer_id: str
    service_id: str
    scheduled_time: str
    address: str
    total_price: float = Field(gt=0)
    provider_id: Optional[str] = None
    emergency_flag: Optional[str] = None


class BookingStatusUpdateRequest(BaseModel):
    next_status: str  # Requested, Assigned, Accepted, Started, Completed, Paid, Cancelled, Rejected, Expired
    reason: Optional[str] = None


class ProviderReassignRequest(BaseModel):
    new_provider_id: str
    reason: Optional[str] = None


class BookingDetailResponse(BaseModel):
    id: str
    customer_id: str
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = "+91 98765 43210"
    provider_id: Optional[str] = None
    provider_name: Optional[str] = None
    service_id: str
    service_name: Optional[str] = None
    status: str
    payment_method: str = "COD"
    payment_status: str
    scheduled_time: str
    address: str
    total_price: float
    otp_code: Optional[str] = None
    start_otp: Optional[str] = None
    completion_otp: Optional[str] = None
    timeline: List[Dict[str, Any]] = []
    allowed_next_statuses: List[str] = []
    emergency_flag: Optional[str] = None
    cancellation_reason: Optional[str] = None
    customer_notes: Optional[str] = None
    before_photos: Optional[List[str]] = []
    after_photos: Optional[List[str]] = []
    warranty: Optional[Dict[str, Any]] = None
    created_at: str


class PaymentRecordResponse(BaseModel):
    id: str
    booking_id: str
    booking_reference: str
    customer_id: str
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    provider_id: Optional[str] = None
    provider_name: Optional[str] = None
    service_id: Optional[str] = None
    service_name: Optional[str] = None
    payment_method: str = "COD"
    agreed_amount: float
    reported_amount: Optional[float] = None
    status: str  # Pending, Collection Reported, Paid, Rejected
    discrepancy_flag: bool = False
    discrepancy_amount: float = 0.0
    collected_at: Optional[str] = None
    collection_notes: Optional[str] = None
    reviewed_by_id: Optional[str] = None
    reviewed_by_name: Optional[str] = None
    reviewed_at: Optional[str] = None
    rejection_reason: Optional[str] = None
    created_at: str
    updated_at: str


class PaymentVerifyRequest(BaseModel):
    notes: Optional[str] = None


class PaymentRejectRequest(BaseModel):
    reason: str = Field(..., min_length=1, description="Reason for rejecting collection report")
