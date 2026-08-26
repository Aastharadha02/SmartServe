import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.repositories.db import get_db
from app.repositories import audit_repository
from app.models.user import User
from app.models.security import FailedLoginAttempt
from app.models.suspicious_activity import SuspiciousActivity
from app.schemas.security import AuditLogResponse, FailedLoginAttemptResponse
from app.schemas.security_ext import (
    TotpSetupResponse,
    TotpVerifyRequest,
    ActiveSessionResponse,
    SuspiciousActivityResponse
)
from app.services import security_service

from app.core.dependencies import require_admin, require_permission

router = APIRouter(prefix="/admin/security", tags=["Admin Security & Risk Center"])

from app.models.security import AuditLog

@router.get("/summary")
def get_security_summary(
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("security:manage"))
):
    """Retrieve real security monitoring counts."""
    failed_logins = db.query(FailedLoginAttempt).count()
    suspicious_count = db.query(SuspiciousActivity).count()
    active_sessions_count = len(security_service.get_active_sessions(db))
    total_audit_events = db.query(AuditLog).count()
    critical_events = db.query(AuditLog).filter(AuditLog.risk_level.in_(["Critical", "High"])).count()

    return {
        "failed_logins": failed_logins,
        "suspicious_activities": suspicious_count,
        "active_sessions": active_sessions_count,
        "is_totp_enabled": bool(getattr(admin, 'totp_enabled', True)),
        "total_audit_events": total_audit_events,
        "critical_events": critical_events
    }

@router.get("/audit-logs", response_model=List[AuditLogResponse])
def get_audit_log_ledger(
    risk_level: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("security:manage"))
):
    """Retrieve immutable audit log ledger filtered by risk level or search."""
    logs = audit_repository.get_audit_logs(db, skip=skip, limit=limit, risk_level=risk_level)
    res = []
    for l in logs:
        if search:
            s_lower = search.lower()
            if (s_lower not in l.actor_email.lower() and 
                s_lower not in l.action.lower() and 
                s_lower not in (l.target_resource or "").lower()):
                continue

        res.append(AuditLogResponse(
            id=str(l.id),
            actor_email=l.actor_email,
            actor_role=l.actor_role,
            action=l.action,
            target_resource=l.target_resource,
            ip_address=l.ip_address,
            risk_level=l.risk_level,
            metadata_json=l.metadata_json,
            created_at=l.created_at.isoformat() if l.created_at else ""
        ))
    return res

@router.get("/failed-logins", response_model=List[FailedLoginAttemptResponse])
def get_failed_login_attempts(
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("security:manage"))
):
    """List failed login attempt tracking."""
    attempts = db.query(FailedLoginAttempt).order_by(FailedLoginAttempt.last_attempt.desc()).limit(50).all()
    return [
        FailedLoginAttemptResponse(
            id=str(a.id),
            email=a.email,
            ip_address=a.ip_address,
            attempt_count=a.attempt_count,
            last_attempt=a.last_attempt.isoformat(),
            locked_until=a.locked_until.isoformat() if a.locked_until else None
        ) for a in attempts
    ]

@router.post("/2fa/setup", response_model=TotpSetupResponse)
def setup_admin_2fa(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Setup TOTP 2FA secret key and QR provisioning URI for Admin."""
    res = security_service.setup_totp_2fa(db, admin)
    return TotpSetupResponse(
        secret=res["secret"],
        provisioning_uri=res["provisioning_uri"]
    )

@router.post("/2fa/verify")
def verify_admin_2fa(
    req: TotpVerifyRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Verify 6-digit TOTP 2FA code."""
    is_valid = security_service.verify_totp_2fa(db, admin, req.code)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid TOTP 2FA verification code")
    return {"status": "success", "message": "Admin 2FA verification successful."}

@router.post("/2fa/disable")
def disable_admin_2fa(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Disable TOTP 2FA for current admin."""
    admin.is_2fa_enabled = False
    admin.totp_secret = None
    db.commit()

    audit_repository.create_audit_log(
        db, actor_id=admin.id, actor_email=admin.email, actor_role=admin.role,
        action="Disabled Admin 2FA Authenticator", risk_level="Warning"
    )

    return {"status": "success", "message": "2FA disabled successfully."}

@router.get("/active-sessions", response_model=List[ActiveSessionResponse])
def get_active_sessions(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("security:manage"))
):
    """List active JWT sessions across admin/users."""
    sessions = security_service.get_active_sessions(db, skip=skip, limit=limit)
    return [
        ActiveSessionResponse(
            id=str(s.id),
            user_id=str(s.user_id),
            token_jti=s.token_jti,
            ip_address=s.ip_address,
            user_agent=s.user_agent,
            is_revoked=s.is_revoked,
            created_at=s.created_at.isoformat(),
            expires_at=s.expires_at.isoformat()
        ) for s in sessions
    ]

@router.post("/revoke-session/{session_id}")
def revoke_active_session(
    session_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("security:manage"))
):
    """Revoke active JWT session."""
    try:
        s_uuid = uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session ID format")

    revoked = security_service.revoke_session(db, s_uuid)
    if not revoked:
        raise HTTPException(status_code=404, detail="Active session not found")

    return {"status": "success", "session_id": session_id, "message": "Session revoked."}

@router.get("/suspicious-activities", response_model=List[SuspiciousActivityResponse])
def list_suspicious_activities(
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("security:manage"))
):
    """List flagged security anomalies and suspicious activities."""
    activities = db.query(SuspiciousActivity).order_by(SuspiciousActivity.created_at.desc()).limit(50).all()
    return [
        SuspiciousActivityResponse(
            id=str(act.id),
            user_id=str(act.user_id) if act.user_id else None,
            anomaly_type=act.anomaly_type,
            risk_score=act.risk_score,
            details_json=act.details_json,
            created_at=act.created_at.isoformat()
        ) for act in activities
    ]
