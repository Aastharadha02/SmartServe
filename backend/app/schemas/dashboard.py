from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class DashboardStatsResponse(BaseModel):
    total_bookings: int
    active_providers: int
    online_providers: int
    total_revenue: float
    pending_verifications: int
    emergency_requests: int
    open_support_tickets: int

class BookingStatusCountsResponse(BaseModel):
    requested: int
    assigned: int
    accepted: int
    started: int
    completed: int
    paid: int
    cancelled: int
    rejected: int
    expired: int

class RecentActivityItem(BaseModel):
    id: str
    action: str
    actor: str
    timestamp: str
    risk_level: str

class AiInsightItem(BaseModel):
    topic: str
    insight: str
    confidence: float
    recommended_action: str

class OperationsDashboardResponse(BaseModel):
    kpis: DashboardStatsResponse
    booking_status_counts: BookingStatusCountsResponse
    recent_activity: List[RecentActivityItem]
    ai_insights: List[AiInsightItem]
