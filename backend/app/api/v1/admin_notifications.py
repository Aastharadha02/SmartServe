import uuid
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.dependencies import require_admin
from app.models.user import User
from app.models.notification import NotificationLog
from app.schemas.notification import NotificationResponse
from app.services.notification import retry_notification, MAX_NOTIFICATION_RETRIES

router = APIRouter(prefix="/admins/notifications", tags=["Admin Notification Management"])


@router.get("", response_model=List[NotificationResponse], summary="List and filter notification audit history")
def list_notification_history(
    booking_reference: Optional[str] = Query(None, description="Filter by booking reference"),
    channel: Optional[str] = Query(None, description="Filter by channel ('email' or 'whatsapp')"),
    delivery_status: Optional[str] = Query(None, alias="status", description="Filter by delivery status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """
    Administrative monitoring view for automated Email and WhatsApp notification logs.
    Strictly restricted to authorized system administrators.
    """
    query = db.query(NotificationLog)

    if booking_reference:
        ref_clean = booking_reference.strip()
        query = query.filter(func.lower(NotificationLog.booking_reference) == ref_clean.lower())

    if channel:
        ch_clean = channel.strip().lower()
        query = query.filter(func.lower(NotificationLog.channel) == ch_clean)

    if delivery_status:
        st_clean = delivery_status.strip().lower()
        query = query.filter(func.lower(NotificationLog.delivery_status) == st_clean)

    records = (
        query.order_by(NotificationLog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return records


@router.get("/stats", summary="Summary statistics of notification delivery by channel and status")
def get_notification_stats(
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Aggregated notification delivery metrics for admin dashboard."""
    total_count = db.query(func.count(NotificationLog.id)).scalar() or 0
    email_count = db.query(func.count(NotificationLog.id)).filter(NotificationLog.channel == "email").scalar() or 0
    wa_count = db.query(func.count(NotificationLog.id)).filter(NotificationLog.channel == "whatsapp").scalar() or 0

    sent_count = db.query(func.count(NotificationLog.id)).filter(NotificationLog.delivery_status.in_(["Sent", "Delivered"])).scalar() or 0
    failed_count = db.query(func.count(NotificationLog.id)).filter(NotificationLog.delivery_status == "Failed").scalar() or 0
    unconfigured_count = db.query(func.count(NotificationLog.id)).filter(NotificationLog.delivery_status == "Unconfigured").scalar() or 0

    return {
        "total_notifications": total_count,
        "email_notifications": email_count,
        "whatsapp_notifications": wa_count,
        "successful_deliveries": sent_count,
        "failed_deliveries": failed_count,
        "unconfigured_deliveries": unconfigured_count,
    }


@router.post("/{notification_id}/retry", response_model=NotificationResponse, summary="Retry a failed notification")
def retry_failed_notification(
    notification_id: uuid.UUID,
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """
    Allow administrator to retry a failed notification.
    Follows max retry limits and updates last attempt timestamp.
    """
    try:
        updated_log = retry_notification(db, notification_id, max_retries=MAX_NOTIFICATION_RETRIES)
        return updated_log
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retry notification: {type(exc).__name__}",
        )
