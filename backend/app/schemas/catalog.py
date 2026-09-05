from typing import Optional, List, Dict, Any, Union
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
    description: Optional[str] = None
    highlights: Optional[List[str]] = None
    included: Optional[List[str]] = None
    excluded: Optional[List[str]] = None
    process_steps: Optional[List[Dict[str, Any]]] = None
    aftercare: Optional[List[str]] = None
    tools_materials: Optional[List[str]] = None
    customer_setup: Optional[List[str]] = None
    expected_results: Optional[List[str]] = None
    important_notes: Optional[List[str]] = None
    warranty: Optional[str] = None
    faqs: Optional[List[Dict[str, Any]]] = None
    tips: Optional[List[str]] = None
    dos: Optional[List[str]] = None
    donts: Optional[List[str]] = None
    duration_minutes: Optional[int] = None
    service_media: Optional[List[Dict[str, Any]]] = None
    service_features: Optional[List[Union[str, Dict[str, Any]]]] = None
    seo_metadata: Optional[Dict[str, Any]] = None

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
    description: Optional[str] = None
    highlights: Optional[List[str]] = None
    included: Optional[List[str]] = None
    excluded: Optional[List[str]] = None
    process_steps: Optional[List[Dict[str, Any]]] = None
    aftercare: Optional[List[str]] = None
    tools_materials: Optional[List[str]] = None
    customer_setup: Optional[List[str]] = None
    expected_results: Optional[List[str]] = None
    important_notes: Optional[List[str]] = None
    warranty: Optional[str] = None
    faqs: Optional[List[Dict[str, Any]]] = None
    tips: Optional[List[str]] = None
    dos: Optional[List[str]] = None
    donts: Optional[List[str]] = None
    duration_minutes: Optional[int] = None
    addons: Optional[List[Dict[str, Any]]] = None
    service_media: Optional[List[Dict[str, Any]]] = None
    service_features: Optional[List[Union[str, Dict[str, Any]]]] = None
    seo_metadata: Optional[Dict[str, Any]] = None

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
    description: Optional[str] = None
    highlights: Optional[List[str]] = None
    included: Optional[List[str]] = None
    excluded: Optional[List[str]] = None
    process_steps: Optional[List[Dict[str, Any]]] = None
    aftercare: Optional[List[str]] = None
    tools_materials: Optional[List[str]] = None
    customer_setup: Optional[List[str]] = None
    expected_results: Optional[List[str]] = None
    important_notes: Optional[List[str]] = None
    warranty: Optional[str] = None
    faqs: Optional[List[Dict[str, Any]]] = None
    tips: Optional[List[str]] = None
    dos: Optional[List[str]] = None
    donts: Optional[List[str]] = None
    duration_minutes: Optional[int] = None
    addons: Optional[List[Dict[str, Any]]] = None
    service_media: Optional[List[Dict[str, Any]]] = None
    service_features: Optional[List[Union[str, Dict[str, Any]]]] = None
    seo_metadata: Optional[Dict[str, Any]] = None

class CatalogTreeResponse(BaseModel):
    categories: List[Dict[str, Any]]

