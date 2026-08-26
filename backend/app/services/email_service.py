import uuid
from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.email import EmailTemplate, EmailLog
from app.repositories import audit_repository

def get_email_templates(db: Session) -> List[EmailTemplate]:
    """List system email templates."""
    return db.query(EmailTemplate).all()

def get_template_by_key(db: Session, template_key: str) -> Optional[EmailTemplate]:
    return db.query(EmailTemplate).filter(EmailTemplate.template_key == template_key).first()

def upsert_email_template(db: Session, template_key: str, subject: str, body_html: str) -> EmailTemplate:
    tmpl = get_template_by_key(db, template_key)
    now = datetime.now(timezone.utc)
    if not tmpl:
        tmpl = EmailTemplate(
            id=uuid.uuid4(),
            template_key=template_key,
            subject=subject,
            body_html=body_html,
            updated_at=now
        )
        db.add(tmpl)
    else:
        tmpl.subject = subject
        tmpl.body_html = body_html
        tmpl.updated_at = now
    db.commit()
    db.refresh(tmpl)
    return tmpl

def send_email_dispatch(
    db: Session,
    recipient_email: str,
    subject: str,
    body_text: str,
    template_key: Optional[str] = None,
    actor_email: Optional[str] = None
) -> EmailLog:
    """Record and log outbound system/admin email dispatch."""
    log_entry = EmailLog(
        id=uuid.uuid4(),
        recipient_email=recipient_email,
        subject=subject,
        template_key=template_key,
        status="Sent",
        sent_at=datetime.now(timezone.utc)
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)

    if actor_email:
        audit_repository.create_audit_log(
            db, actor_email=actor_email, actor_role="admin",
            action=f"Sent Email to {recipient_email} ('{subject}')", risk_level="Info"
        )
    return log_entry

def get_email_logs(db: Session, skip: int = 0, limit: int = 50) -> List[EmailLog]:
    return db.query(EmailLog).order_by(EmailLog.sent_at.desc()).offset(skip).limit(limit).all()
