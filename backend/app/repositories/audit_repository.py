import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.security import AuditLog, FailedLoginAttempt

def create_audit_log(
    db: Session,
    actor_email: str,
    actor_role: str,
    action: str,
    target_resource: Optional[str] = None,
    ip_address: Optional[str] = None,
    risk_level: str = "Info",
    actor_id: Optional[uuid.UUID] = None,
    metadata_json: Optional[Dict[str, Any]] = None
) -> AuditLog:
    """Record an immutable audit log entry."""
    log_entry = AuditLog(
        id=uuid.uuid4(),
        actor_id=actor_id,
        actor_email=actor_email,
        actor_role=actor_role,
        action=action,
        target_resource=target_resource,
        ip_address=ip_address,
        risk_level=risk_level,
        metadata_json=metadata_json,
        created_at=datetime.now(timezone.utc)
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry

def get_audit_logs(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    risk_level: Optional[str] = None
) -> List[AuditLog]:
    """Retrieve audit logs sorted by created_at desc."""
    query = db.query(AuditLog)
    if risk_level:
        query = query.filter(AuditLog.risk_level == risk_level)
    return query.order_by(desc(AuditLog.created_at)).offset(skip).limit(limit).all()

def get_audit_logs_for_service(
    db: Session,
    service_id: str,
    skip: int = 0,
    limit: int = 50
) -> List[AuditLog]:
    """Retrieve immutable audit logs associated with a specific service ID."""
    return db.query(AuditLog).filter(
        (AuditLog.target_resource == service_id) |
        (AuditLog.target_resource == f"service:{service_id}")
    ).order_by(desc(AuditLog.created_at)).offset(skip).limit(limit).all()

def record_failed_login(db: Session, email: str, ip_address: Optional[str] = None) -> FailedLoginAttempt:
    """Track failed login attempt."""
    attempt = db.query(FailedLoginAttempt).filter(FailedLoginAttempt.email == email).first()
    now = datetime.now(timezone.utc)
    if not attempt:
        attempt = FailedLoginAttempt(
            id=uuid.uuid4(),
            email=email,
            ip_address=ip_address,
            attempt_count=1,
            last_attempt=now
        )
        db.add(attempt)
    else:
        attempt.attempt_count += 1
        attempt.last_attempt = now
        attempt.ip_address = ip_address
    db.commit()
    db.refresh(attempt)
    return attempt
