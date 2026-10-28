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

def setup_totp_2fa(db: Session, user: User) -> Dict[str, Any]:
    """Generate TOTP secret key and backup recovery codes for Admin/Provider 2FA setup."""
    import secrets
    from app.models.security import TwoFactorRecoveryCode

    if not user.totp_secret:
        user.totp_secret = pyotp.random_base32()

    # Clear old unused recovery codes for this user
    db.query(TwoFactorRecoveryCode).filter(
        TwoFactorRecoveryCode.user_id == user.id,
        TwoFactorRecoveryCode.is_used == False
    ).delete(synchronize_session=False)

    recovery_codes = []
    for _ in range(5):
        raw_code = f"{secrets.token_hex(2).upper()}-{secrets.token_hex(2).upper()}"
        recovery_codes.append(raw_code)
        code_hash = hashlib.sha256(raw_code.encode("utf-8")).hexdigest()
        rc = TwoFactorRecoveryCode(
            id=uuid.uuid4(),
            user_id=user.id,
            code_hash=code_hash,
            is_used=False
        )
        db.add(rc)

    db.commit()

    totp = pyotp.TOTP(user.totp_secret)
    issuer = "SmartServe Admin" if user.role in ["admin", "super_admin"] else "SmartServe Provider"
    provisioning_uri = totp.provisioning_uri(name=user.email, issuer_name=issuer)
    return {
        "secret": user.totp_secret,
        "provisioning_uri": provisioning_uri,
        "recovery_codes": recovery_codes,
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

def verify_recovery_code(db: Session, user: User, code: str) -> bool:
    """Validate and atomically burn a single-use backup recovery code."""
    from app.models.security import TwoFactorRecoveryCode
    from sqlalchemy import update
    clean_code = (code or "").strip().upper()
    if not clean_code:
        return False
    code_hash = hashlib.sha256(clean_code.encode("utf-8")).hexdigest()
    now = datetime.now(timezone.utc)

    stmt = (
        update(TwoFactorRecoveryCode)
        .where(
            TwoFactorRecoveryCode.user_id == user.id,
            TwoFactorRecoveryCode.code_hash == code_hash,
            TwoFactorRecoveryCode.is_used == False,
        )
        .values(is_used=True, used_at=now)
    )
    res = db.execute(stmt)
    if res.rowcount > 0:
        db.commit()
        return True
    return False


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

def verify_signed_evidence_url(ticket_id: str, file_path: str, expires_ts: int, signature: str) -> bool:
    """Verify time-limited HMAC signature for evidence stream access."""
    now_ts = int(datetime.now(timezone.utc).timestamp())
    if now_ts > expires_ts:
        return False
    raw_str = f"{ticket_id}:{file_path}:{expires_ts}"
    expected_sig = hmac.new(
        settings.JWT_SECRET_KEY.encode('utf-8'),
        raw_str.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_sig, signature)

def revoke_all_user_sessions(db: Session, user_id: uuid.UUID) -> int:
    """Revoke all active sessions for a user (e.g. upon password reset, password change, or suspension)."""
    count = (
        db.query(ActiveSession)
        .filter(ActiveSession.user_id == user_id, ActiveSession.is_revoked == False)
        .update({"is_revoked": True}, synchronize_session=False)
    )
    try:
        from app.models.user import UserSession
        db.query(UserSession).filter(UserSession.user_id == user_id).delete(synchronize_session=False)
    except Exception:
        pass
    db.commit()
    return count
def cleanup_expired_security_records(
    db: Session,
    max_records_per_table: int = 1000
) -> Dict[str, int]:
    """
    Safely and boundedly purges expired records across security tables:
    1. Revoked ActiveSessions whose expiration time has passed (expires_at < now).
       NEVER touches active or non-expired sessions.
    2. RateLimitEntry records older than 15 minutes.
       NEVER touches active rate-limit windows (last 60 seconds).
    3. PasswordResetTokens that are either expired (expires_at < now) or already used (is_used == True).
    4. TwoFactorRecoveryCodes that have already been used (is_used == True).
    """
    from app.models.security import RateLimitEntry, PasswordResetToken, TwoFactorRecoveryCode

    now = datetime.now(timezone.utc)
    results = {}

    # 1. Purge expired AND revoked sessions
    expired_sess = (
        db.query(ActiveSession.id)
        .filter(ActiveSession.is_revoked == True, ActiveSession.expires_at < now)
        .limit(max_records_per_table)
        .all()
    )
    expired_sess_ids = [s[0] for s in expired_sess]
    if expired_sess_ids:
        del_sess = db.query(ActiveSession).filter(ActiveSession.id.in_(expired_sess_ids)).delete(synchronize_session=False)
    else:
        del_sess = 0
    results["revoked_sessions_purged"] = del_sess

    # 2. Purge stale rate limit entries older than 15 mins
    rate_cutoff = now - timedelta(minutes=15)
    stale_rl = (
        db.query(RateLimitEntry.id)
        .filter(RateLimitEntry.created_at < rate_cutoff)
        .limit(max_records_per_table)
        .all()
    )
    stale_rl_ids = [r[0] for r in stale_rl]
    if stale_rl_ids:
        del_rl = db.query(RateLimitEntry).filter(RateLimitEntry.id.in_(stale_rl_ids)).delete(synchronize_session=False)
    else:
        del_rl = 0
    results["rate_limit_entries_purged"] = del_rl

    # 3. Purge expired or used password reset tokens
    stale_tokens = (
        db.query(PasswordResetToken.id)
        .filter((PasswordResetToken.expires_at < now) | (PasswordResetToken.is_used == True))
        .limit(max_records_per_table)
        .all()
    )
    stale_token_ids = [t[0] for t in stale_tokens]
    if stale_token_ids:
        del_tokens = db.query(PasswordResetToken).filter(PasswordResetToken.id.in_(stale_token_ids)).delete(synchronize_session=False)
    else:
        del_tokens = 0
    results["password_reset_tokens_purged"] = del_tokens

    # 4. Purge used 2FA recovery codes
    stale_rc = (
        db.query(TwoFactorRecoveryCode.id)
        .filter(TwoFactorRecoveryCode.is_used == True)
        .limit(max_records_per_table)
        .all()
    )
    stale_rc_ids = [rc[0] for rc in stale_rc]
    if stale_rc_ids:
        del_rc = db.query(TwoFactorRecoveryCode).filter(TwoFactorRecoveryCode.id.in_(stale_rc_ids)).delete(synchronize_session=False)
    else:
        del_rc = 0
    results["used_recovery_codes_purged"] = del_rc

    db.commit()
    return results
