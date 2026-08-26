import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class AddOnSchema(BaseModel):
    name: str
    price: float


class ServiceBase(BaseModel):
    category: str
    subcategory: str
    name: str
    base_price: float
    max_demand_increase: float = 0.0
    max_discount: float = 0.0
    distinct_features: Optional[List[str]] = None
    suggested_addons: Optional[List[AddOnSchema]] = None
    is_active: bool = True


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    category: Optional[str] = None
    subcategory: Optional[str] = None
    name: Optional[str] = None
    base_price: Optional[float] = None
    max_demand_increase: Optional[float] = None
    max_discount: Optional[float] = None
    distinct_features: Optional[List[str]] = None
    suggested_addons: Optional[List[AddOnSchema]] = None
    is_active: Optional[bool] = None


class ServiceRead(ServiceBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CategorySubcategoryResponse(BaseModel):
    category: str
    subcategories: List[str]
