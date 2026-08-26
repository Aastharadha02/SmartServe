import uuid
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate, FeedbackSummaryResponse


def create_feedback(db: Session, feedback_in: FeedbackCreate) -> Feedback:
    fb = Feedback(
        customer_id=feedback_in.customer_id,
        provider_id=feedback_in.provider_id,
        service_id=feedback_in.service_id,
        rating=feedback_in.rating,
        review_text=feedback_in.review_text,
        sentiment_score=feedback_in.sentiment_score,
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb


def get_feedback_list(
    db: Session,
    provider_id: Optional[uuid.UUID] = None,
    service_id: Optional[uuid.UUID] = None,
    customer_id: Optional[uuid.UUID] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[Feedback]:
    query = db.query(Feedback)
    if provider_id:
        query = query.filter(Feedback.provider_id == provider_id)
    if service_id:
        query = query.filter(Feedback.service_id == service_id)
    if customer_id:
        query = query.filter(Feedback.customer_id == customer_id)
    return query.order_by(Feedback.created_at.desc()).offset(skip).limit(limit).all()


def get_feedback_summary(
    db: Session,
    provider_id: Optional[uuid.UUID] = None,
    service_id: Optional[uuid.UUID] = None,
) -> FeedbackSummaryResponse:
    query = db.query(Feedback)
    if provider_id:
        query = query.filter(Feedback.provider_id == provider_id)
    if service_id:
        query = query.filter(Feedback.service_id == service_id)

    total_reviews = query.count()
    if total_reviews == 0:
        return FeedbackSummaryResponse(
            average_rating=0.0,
            total_reviews=0,
            rating_distribution={1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
        )

    avg_rating = query.with_entities(func.avg(Feedback.rating)).scalar() or 0.0

    # Calculate distribution
    distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for r in range(1, 6):
        cnt = query.filter(func.round(Feedback.rating) == r).count()
        distribution[r] = cnt

    return FeedbackSummaryResponse(
        average_rating=round(float(avg_rating), 2),
        total_reviews=total_reviews,
        rating_distribution=distribution,
    )
