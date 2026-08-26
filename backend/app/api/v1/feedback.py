import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.repositories.db import get_db
from app.repositories import audit_repository
from app.models.user import User
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackResponse, FeedbackAiScanResponse
from app.services.ai_service import ai_service

router = APIRouter(prefix="/admin/feedback", tags=["Customer Feedback & Complaints"])

@router.get("/", response_model=List[FeedbackResponse])
def list_customer_feedback(
    min_rating: Optional[float] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Query and filter customer feedback and ratings."""
    query = db.query(Feedback)
    if min_rating is not None:
        query = query.filter(Feedback.rating >= min_rating)

    feedbacks = query.offset(skip).limit(limit).all()
    return [
        FeedbackResponse(
            id=str(f.id),
            customer_id=str(f.customer_id) if f.customer_id else None,
            provider_id=str(f.provider_id) if f.provider_id else None,
            service_id=str(f.service_id) if f.service_id else None,
            rating=f.rating,
            review_text=f.review_text,
            sentiment_score=float(f.sentiment_score) if f.sentiment_score else 0.0,
            ai_category=f.ai_category or "General"
        ) for f in feedbacks
    ]

@router.post("/{feedback_id}/ai-scan", response_model=FeedbackAiScanResponse)
def scan_complaint_evidence(
    feedback_id: str,
    image_url: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Scan complaint photo / chat screenshot with OCR text extraction and sentiment scoring."""
    try:
        f_uuid = uuid.UUID(feedback_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid feedback ID format")

    feedback = db.query(Feedback).filter(Feedback.id == f_uuid).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback record not found")

    scan_res = ai_service.scan_complaint_image(image_url, complaint_context=feedback.review_text or "")

    feedback.sentiment_score = scan_res["sentiment_score"]
    feedback.ai_category = scan_res["dispute_category"]
    db.commit()

    audit_repository.create_audit_log(
        db, actor_id=admin.id, actor_email=admin.email, actor_role=admin.role,
        action=f"AI Complaint OCR Scan for Feedback #{feedback_id}", target_resource=feedback_id
    )

    return FeedbackAiScanResponse(
        feedback_id=feedback_id,
        image_url=image_url,
        ocr_extracted_text=scan_res["ocr_extracted_text"],
        dispute_category=scan_res["dispute_category"],
        sentiment_score=scan_res["sentiment_score"],
        authenticity_score=scan_res["authenticity_score"],
        ai_findings=scan_res["ai_findings"],
        suggested_admin_action=scan_res["suggested_admin_action"]
    )
