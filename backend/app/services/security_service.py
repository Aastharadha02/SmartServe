import uuid
import hmac
import hashlib
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone, timedelta
import pyotp
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.models.session import ActiveSession
from app.models.suspicious_activity import SuspiciousActivity

def setup_totp_2fa(db: Session, user: User) -> Dict[str, str]:
    """Generate TOTP secret key for Admin 2FA setup."""
    if not user.totp_secret:
        user.totp_secret = pyotp.random_base32()
        db.commit()

    totp = pyotp.TOTP(user.totp_secret)
    provisioning_uri = totp.provisioning_uri(name=user.email, issuer_name="SmartServe Admin")
    return {
        "secret": user.totp_secret,
        "provisioning_uri": provisioning_uri
    }

def verify_totp_2fa(db: Session, user: User, code: str) -> bool:
    """Validate 6-digit TOTP 2FA code."""
    if not user.totp_secret:
        return False
    totp = pyotp.TOTP(user.totp_secret)
    is_valid = totp.verify(code)
    if is_valid and not user.is_2fa_enabled:
        user.is_2fa_enabled = True
        db.commit()
    return is_valid

def create_active_session(
    db: Session,
    user_id: uuid.UUID,
    token_jti: str,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    expires_in_minutes: int = 30
) -> ActiveSession:
    """Track active JWT session."""
    now = datetime.now(timezone.utc)
    session = ActiveSession(
        id=uuid.uuid4(),
        user_id=user_id,
        token_jti=token_jti,
        ip_address=ip_address,
        user_agent=user_agent,
        is_revoked=False,
        created_at=now,
        expires_at=now + timedelta(minutes=expires_in_minutes)
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def get_active_sessions(db: Session, skip: int = 0, limit: int = 50) -> List[ActiveSession]:
    return db.query(ActiveSession).filter(ActiveSession.is_revoked == False).order_by(ActiveSession.created_at.desc()).offset(skip).limit(limit).all()

def revoke_session(db: Session, session_id: uuid.UUID) -> bool:
    session = db.query(ActiveSession).filter(ActiveSession.id == session_id).first()
    if session:
        session.is_revoked = True
        db.commit()
        return True
    return False

def generate_signed_evidence_url(ticket_id: str, file_path: str, expires_in_seconds: int = 900) -> str:
    """Generate time-limited HMAC signed URL (15 mins) for evidence access."""
    expiry_ts = int(datetime.now(timezone.utc).timestamp()) + expires_in_seconds
    raw_str = f"{ticket_id}:{file_path}:{expiry_ts}"
    signature = hmac.new(
        settings.JWT_SECRET_KEY.encode('utf-8'),
        raw_str.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return f"/api/v1/admin/support/evidence/stream?ticket_id={ticket_id}&path={file_path}&expires={expiry_ts}&sig={signature}"

def log_suspicious_activity(
    db: Session,
    anomaly_type: str,
    risk_score: float,
    user_id: Optional[uuid.UUID] = None,
    details: Optional[Dict[str, Any]] = None
) -> SuspiciousActivity:
    activity = SuspiciousActivity(
        id=uuid.uuid4(),
        user_id=user_id,
        anomaly_type=anomaly_type,
        risk_score=risk_score,
        details_json=details,
        created_at=datetime.now(timezone.utc)
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity
