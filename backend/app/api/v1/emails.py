from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.repositories.db import get_db
from app.models.user import User
from app.schemas.email import (
    EmailTemplateUpsertRequest,
    EmailTemplateResponse,
    EmailSendRequest,
    EmailLogResponse
)
from app.services import email_service

router = APIRouter(prefix="/admin/emails", tags=["Admin Email Center"])

from typing import Optional
from app.repositories import audit_repository

SUPPORTED_VARS = ["customer_name", "booking_id", "service_name", "provider_name", "scheduled_time", "amount", "otp_code"]

@router.get("/templates", response_model=List[EmailTemplateResponse])
def list_email_templates(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """List system email templates."""
    templates = email_service.get_email_templates(db)
    return [
        EmailTemplateResponse(
            id=str(t.id),
            template_key=t.template_key,
            subject=t.subject,
            body_html=t.body_html,
            is_active=True,
            supported_variables=SUPPORTED_VARS,
            updated_at=t.updated_at.isoformat() if t.updated_at else ""
        ) for t in templates
    ]

from app.core.dependencies import require_admin, require_permission

@router.post("/templates", response_model=EmailTemplateResponse)
def upsert_template(
    req: EmailTemplateUpsertRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("emails:manage"))
):
    """Create or update system email template."""
    tmpl = email_service.upsert_email_template(
        db, template_key=req.template_key, subject=req.subject, body_html=req.body_html
    )

    audit_repository.create_audit_log(
        db, actor_id=admin.id, actor_email=admin.email, actor_role=admin.role,
        action=f"Upserted Email Template '{req.template_key}'", target_resource=str(tmpl.id)
    )

    return EmailTemplateResponse(
        id=str(tmpl.id),
        template_key=tmpl.template_key,
        subject=tmpl.subject,
        body_html=tmpl.body_html,
        is_active=True,
        supported_variables=SUPPORTED_VARS,
        updated_at=tmpl.updated_at.isoformat() if tmpl.updated_at else ""
    )

@router.post("/send", response_model=EmailLogResponse)
def dispatch_email(
    req: EmailSendRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("emails:manage"))
):
    """Dispatch manual or system email to customer/provider."""
    log_entry = email_service.send_email_dispatch(
        db,
        recipient_email=req.recipient_email,
        subject=req.subject,
        body_text=req.body_text,
        template_key=req.template_key,
        actor_email=admin.email
    )
    return EmailLogResponse(
        id=str(log_entry.id),
        recipient_email=log_entry.recipient_email,
        subject=log_entry.subject,
        template_key=log_entry.template_key,
        status=log_entry.status,
        error_message="Recipient domain unroutable" if log_entry.status == "Failed" else None,
        sent_at=log_entry.sent_at.isoformat() if log_entry.sent_at else ""
    )

@router.get("/logs", response_model=List[EmailLogResponse])
def get_email_logs(
    search: Optional[str] = None,
    status_filter: Optional[str] = None,
    template_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """List outbound email history logs with search and status filters."""
    logs = email_service.get_email_logs(db, skip=skip, limit=limit)
    res = []
    for l in logs:
        if status_filter and l.status.lower() != status_filter.lower():
            continue
        if template_filter and (l.template_key or "").lower() != template_filter.lower():
            continue
        if search:
            s_lower = search.lower()
            if (s_lower not in l.recipient_email.lower() and 
                s_lower not in l.subject.lower() and 
                s_lower not in (l.template_key or "").lower()):
                continue

        res.append(EmailLogResponse(
            id=str(l.id),
            recipient_email=l.recipient_email,
            subject=l.subject,
            template_key=l.template_key,
            status=l.status,
            error_message="SMTP 550 Recipient unroutable" if l.status == "Failed" else None,
            sent_at=l.sent_at.isoformat() if l.sent_at else ""
        ))
    return res
