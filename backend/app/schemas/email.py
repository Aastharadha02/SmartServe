from typing import Optional, List
from pydantic import BaseModel, EmailStr

class EmailTemplateUpsertRequest(BaseModel):
    template_key: str
    subject: str
    body_html: str
    is_active: Optional[bool] = True

class EmailTemplateResponse(BaseModel):
    id: str
    template_key: str
    subject: str
    body_html: str
    is_active: bool = True
    supported_variables: List[str] = ["customer_name", "booking_id", "service_name", "provider_name", "scheduled_time", "amount", "otp_code"]
    updated_at: str

class EmailSendRequest(BaseModel):
    recipient_email: EmailStr
    subject: str
    body_text: str
    template_key: Optional[str] = None

class EmailLogResponse(BaseModel):
    id: str
    recipient_email: str
    subject: str
    template_key: Optional[str] = None
    status: str
    error_message: Optional[str] = None
    sent_at: str
