from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ServiceCreateRequest(BaseModel):
    category: str
    subcategory: str
    name: str
    base_price: float = Field(gt=0)
    max_demand_increase: float = Field(default=0.5)
    max_discount: float = Field(default=0.3)
    distinct_features: Optional[List[str]] = []
    suggested_addons: Optional[List[Dict[str, Any]]] = []
    is_active: bool = True

class ServiceUpdateRequest(BaseModel):
    category: Optional[str] = None
    subcategory: Optional[str] = None
    name: Optional[str] = None
    base_price: Optional[float] = Field(default=None, gt=0)
    max_demand_increase: Optional[float] = None
    max_discount: Optional[float] = None
    distinct_features: Optional[List[str]] = None
    suggested_addons: Optional[List[Dict[str, Any]]] = None
    is_active: Optional[bool] = None

class ServiceResponse(BaseModel):
    id: str
    category: str
    subcategory: str
    name: str
    base_price: float
    max_demand_increase: float
    max_discount: float
    distinct_features: Optional[List[str]] = []
    suggested_addons: Optional[List[Dict[str, Any]]] = []
    is_active: bool
    created_at: str

class CatalogTreeResponse(BaseModel):
    categories: List[Dict[str, Any]]
