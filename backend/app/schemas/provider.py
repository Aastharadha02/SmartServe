import uuid
from datetime import datetime, date, time
from decimal import Decimal
from typing import Optional, List
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
