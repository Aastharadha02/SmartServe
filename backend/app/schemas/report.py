from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class AggregatePeriodReport(BaseModel):
    period: str # today, 7days, 30days, monthly, custom
    total_revenue: float
    period_revenue: float
    total_bookings: int
    completed_bookings: int
    cancelled_bookings: int
    in_progress_bookings: int
    completion_rate: float
    cancellation_rate: float
    average_booking_value: float
    new_customers: int
    daily_trend: List[Dict[str, Any]] = []
    ai_insight: Optional[Dict[str, Any]] = None

class ProviderPerformanceReport(BaseModel):
    provider_id: str
    provider_name: str
    total_jobs: int
    completed_jobs: int
    completion_rate: float = 95.0
    reliability_score: float
    earnings: float
    rating: float

class ServiceDemandReport(BaseModel):
    category: str
    service_name: str
    booking_count: int
    total_revenue: float
    demand_trend: Optional[str] = "+24% demand surge"
