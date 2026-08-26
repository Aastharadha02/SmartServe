from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class CustomerResponse(BaseModel):
    id: UUID
    full_name: str
    phone: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ProviderResponse(BaseModel):
    id: UUID
    full_name: str
    phone: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
    customer: Optional[CustomerResponse] = None
    provider: Optional[ProviderResponse] = None

    model_config = ConfigDict(from_attributes=True)
