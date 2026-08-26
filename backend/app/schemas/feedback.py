import uuid
from typing import Optional, List
from pydantic import BaseModel

class FeedbackResponse(BaseModel):
    id: str
    customer_id: Optional[str] = None
    provider_id: Optional[str] = None
    service_id: Optional[str] = None
    rating: float
    review_text: Optional[str] = None
    sentiment_score: Optional[float] = None
    ai_category: Optional[str] = None

class FeedbackAiScanResponse(BaseModel):
    feedback_id: str
    image_url: str
    ocr_extracted_text: str
    dispute_category: str
    sentiment_score: float
    authenticity_score: float
    ai_findings: str
    suggested_admin_action: str
