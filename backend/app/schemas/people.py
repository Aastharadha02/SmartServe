from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr

class ProviderVerifyRequest(BaseModel):
    verification_status: str # Approved, Rejected
    reason: Optional[str] = None

class AccountStatusRequest(BaseModel):
    is_active: bool
    reason: Optional[str] = None

class CustomerFlagRequest(BaseModel):
    flag_type: str = "Fraud Risk"
    reason: str
    notes: Optional[str] = None

class AdminCreateRequest(BaseModel):
    email: EmailStr
    password: str
    role_name: str # super_admin, operations_admin, support_admin, catalog_admin
    permissions: List[str] = []

class AdminRoleUpdateRequest(BaseModel):
    role_name: str
    permissions: List[str] = []

class AdminDetailResponse(BaseModel):
    id: str
    email: str
    role: str
    role_name: str
    permissions: List[str] = []
    is_active: bool = True
    is_2fa_enabled: bool = False
    created_at: str
    recent_activity: List[Dict[str, Any]] = []

class ProviderDetailResponse(BaseModel):
    id: str
    user_id: str
    full_name: str
    email: Optional[str] = "provider@smartserve.com"
    phone: Optional[str] = "+91 98765 43210"
    category: Optional[str] = "General"
    experience_years: int = 5
    base_price: float = 499.0
    is_verified: bool = True
    is_active: bool = True
    reliability_score: float = 98.0
    acceptance_rate: float = 95.0
    on_time_rate: float = 99.0
    cancellation_rate: float = 2.0
    rating: float = 4.9
    completed_bookings: int = 142
    composite_rank_score: float = 88.5
    rank_tier: str = "Tier 1 — Elite"
    created_at: Optional[str] = ""
    documents: List[Dict[str, Any]] = []

class CustomerDetailResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    full_name: str
    email: str
    phone: Optional[str] = None
    is_active: bool = True
    bookings_count: int = 0
    completed_bookings_count: int = 0
    cancelled_bookings_count: int = 0
    is_flagged: bool = False
    flags: List[Dict[str, Any]] = []
    bookings: List[Dict[str, Any]] = []
    created_at: str
