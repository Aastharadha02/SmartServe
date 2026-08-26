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
    next_status: str # Requested, Assigned, Accepted, Started, Completed, Paid, Cancelled, Rejected, Expired
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
    payment_status: str
    scheduled_time: str
    address: str
    total_price: float
    otp_code: Optional[str] = None
    timeline: List[Dict[str, Any]] = []
    allowed_next_statuses: List[str] = []
    emergency_flag: Optional[str] = None
    created_at: str
