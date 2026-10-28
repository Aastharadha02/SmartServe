import os
import uuid
import smtplib
import ssl
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.email import EmailTemplate, EmailLog
from app.repositories import audit_repository

logger = logging.getLogger("smartserve.services.email")

# Thread-safe in-memory test adapter outbox for local verification & automated tests
_in_memory_outbox: List[Dict[str, Any]] = []


def get_sent_test_emails() -> List[Dict[str, Any]]:
    """Retrieve in-memory outbox for testing verification without external credentials."""
    return list(_in_memory_outbox)


def clear_sent_test_emails() -> None:
    """Clear in-memory test outbox."""
    _in_memory_outbox.clear()


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


def _is_safe_smtp_recipient(email: str) -> bool:
    """Validate that email has a syntactically valid structure and is not a disposable dummy domain."""
    if not email or "@" not in email:
        return False
    parts = email.strip().split("@")
    if len(parts) != 2:
        return False
    domain = parts[1].lower().strip()
    blocked_domains = {"example.com", "example.org", "example.net", "test.local", "invalid", "localhost"}
    if domain in blocked_domains or "." not in domain:
        return False
    return True


def _dispatch_via_smtp(recipient_email: str, subject: str, body_text: str, body_html: Optional[str] = None) -> None:
    """
    Connect to configured SMTP server and transmit message.
    Raises smtplib / socket exceptions on delivery failure.
    """
    if not settings.SMTP_HOST:
        raise ValueError("SMTP_HOST is not configured.")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_FROM_EMAIL
    msg["To"] = recipient_email

    msg.attach(MIMEText(body_text, "plain", "utf-8"))
    if body_html:
        msg.attach(MIMEText(body_html, "html", "utf-8"))

    timeout = getattr(settings, "SMTP_TIMEOUT_SECONDS", 10)
    # Determine SSL vs STARTTLS: port 465 or explicit SSL when port is not standard STARTTLS (587)
    use_ssl = (settings.SMTP_PORT == 465) or (getattr(settings, "SMTP_USE_SSL", False) and settings.SMTP_PORT != 587)

    context = ssl.create_default_context()
    if use_ssl:
        server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, context=context, timeout=timeout)
    else:
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=timeout)
        if settings.SMTP_USE_TLS:
            server.starttls(context=context)

    try:
        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
    finally:
        try:
            server.quit()
        except Exception:
            pass


def send_email_dispatch(
    db: Session,
    recipient_email: str,
    subject: str,
    body_text: str,
    body_html: Optional[str] = None,
    template_key: Optional[str] = None,
    actor_email: Optional[str] = None
) -> EmailLog:
    """
    Deliver outbound email via configured transport (SMTP or in-memory test adapter)
    and record durable EmailLog entry.
    Ensures delivery failures are recorded without leaking internal errors.
    """
    status_val = "Sent"
    # Only transmit over live SMTP when backend is configured AND recipient is a valid real domain.
    # Simulated domains (e.g. @example.com) automatically route to the test adapter outbox.
    use_smtp = (settings.EMAIL_BACKEND == "smtp") and _is_safe_smtp_recipient(recipient_email)

    if use_smtp:
        try:
            _dispatch_via_smtp(recipient_email, subject, body_text, body_html)
            logger.info("Successfully delivered email via SMTP to %s", recipient_email)
        except Exception as exc:
            status_val = "Failed"
            logger.error("Failed to deliver email via SMTP to %s: %s", recipient_email, type(exc).__name__)
    else:
        # Deliver to in-memory test outbox
        _in_memory_outbox.append({
            "recipient_email": recipient_email,
            "subject": subject,
            "body_text": body_text,
            "body_html": body_html,
            "template_key": template_key,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        logger.info("Dispatched email via test in-memory adapter to %s", recipient_email)

    log_entry = EmailLog(
        id=uuid.uuid4(),
        recipient_email=recipient_email,
        subject=subject,
        template_key=template_key,
        status=status_val,
        sent_at=datetime.now(timezone.utc)
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)

    if actor_email:
        audit_repository.create_audit_log(
            db, actor_email=actor_email, actor_role="admin",
            action=f"Sent Email to {recipient_email} ('{subject}') - Status: {status_val}", risk_level="Info"
        )
    return log_entry


def get_email_logs(db: Session, skip: int = 0, limit: int = 50) -> List[EmailLog]:
    return db.query(EmailLog).order_by(EmailLog.sent_at.desc()).offset(skip).limit(limit).all()
