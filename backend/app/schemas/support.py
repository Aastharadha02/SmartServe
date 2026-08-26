from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class TicketCreateRequest(BaseModel):
    customer_id: str
    subject: str
    description: str
    booking_id: Optional[str] = None
    priority: str = "Medium"
    image_evidence_url: Optional[str] = None

class TicketReplyRequest(BaseModel):
    message_text: str
    attachment_url: Optional[str] = None

class TicketStatusUpdateRequest(BaseModel):
    status: str # Open, In_Progress, Resolved, Closed
    priority: Optional[str] = None
    escalated_to_admin: Optional[bool] = None

class TicketMessageResponse(BaseModel):
    id: str
    sender_id: str
    sender_role: str
    message_text: str
    attachment_url: Optional[str] = None
    created_at: str

class SupportTicketResponse(BaseModel):
    id: str
    customer_id: str
    customer_name: Optional[str] = "Customer"
    customer_email: Optional[str] = "customer@example.com"
    customer_phone: Optional[str] = "+91 98765 43210"
    assigned_admin_email: Optional[str] = None
    booking_id: Optional[str] = None
    subject: str
    description: str
    priority: str
    status: str
    escalated_to_admin: bool
    image_evidence_url: Optional[str] = None
    ai_analysis: Optional[Dict[str, Any]] = None
    customer_context: Optional[Dict[str, Any]] = None
    created_at: str
    updated_at: Optional[str] = ""
    messages: List[TicketMessageResponse] = []
