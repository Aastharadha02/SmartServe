import os
import re
import uuid
import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Request
from sqlalchemy import func, update
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.cache import get_cache
from app.core.dependencies import get_db, get_current_customer
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.models.user import User, UserSession
from app.models.security import PasswordResetToken

from app.models.customer import (
    Customer,
    Booking,
    SupportTicket,
    TicketMessage,
    BookingFeedback,
    BookingWarranty,
)
from app.schemas.customer_schemas import (
    CustomerRegisterPayload,
    CustomerLoginPayload,
    CustomerTokenResponse,
    CustomerSessionResponse,
    CompleteProfilePayload,
    SkipProfilePayload,
    CustomerLocationPayload,
    ForgotPasswordPayload,
    ResetPasswordPayload,
    ChangePasswordPayload,
    CustomerProfileUpdate,
    CategoryItem,
    SubcategorySummary,
    ServiceItem,
    AddonItem,
    ServiceProcessStep,
    ServiceFeatureItem,
    ServiceMediaItem,
    ServiceFAQ,
    CreateBookingPayload,
    CancelBookingPayload,
    BookingFeedbackPayload,
    BookingDetail,
    CreateTicketPayload,
    TicketMessagePayload,
    SupportTicketDetail,
    MessageItem,
    SessionListItem,
    EligibleProviderResponse,
    WarrantyClaimPayload,
    WarrantyCardResponse,
)

router = APIRouter(prefix="/customer", tags=["Customer API"])

def get_customer_completeness(customer: Customer) -> tuple[bool, list[str]]:
    missing = []
    if not customer.full_name or len(customer.full_name.strip()) < 2:
        missing.append("full_name")
    phone_digits = re.sub(r"[^\d+]", "", customer.phone or "").strip()
    digits_only = re.sub(r"\D", "", phone_digits)
    if len(digits_only) < 10:
        missing.append("phone")
    return len(missing) == 0, missing


def get_customer_location_dict(customer: Customer) -> Optional[Dict[str, Any]]:
    if isinstance(customer.preferences, dict):
        return customer.preferences.get("location")
    return None


from app.api.v1.oauth import router as oauth_router
router.include_router(oauth_router)




# 1. POST /customer/auth/register
@router.post("/auth/register", response_model=CustomerTokenResponse)
def register_customer(payload: CustomerRegisterPayload, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email address is already registered")

    pwd_hash = hash_password(payload.password)
    new_user = User(
        id=uuid.uuid4(),
        email=payload.email,
        hashed_password=pwd_hash,
        role="customer",
        is_active=True,
    )
    new_customer = Customer(
        id=uuid.uuid4(),
        user_id=new_user.id,
        full_name=payload.full_name,
        email=payload.email,
        password_hash=pwd_hash,
        phone=payload.phone or "+91 9876543210",
        preferences=payload.preferences,
        is_verified=True,
        is_active=True,
    )
    db.add(new_user)
    db.add(new_customer)
    db.commit()

    token = create_access_token({"sub": str(new_user.id), "role": "customer", "customer_id": str(new_customer.id)})
    return CustomerTokenResponse(
        access_token=token,
        customer_id=str(new_customer.id),
        user_id=str(new_user.id),
        email=new_customer.email,
        full_name=new_customer.full_name,
        phone=new_customer.phone,
    )


# In-memory store for secure, single-use, time-limited password reset tokens
_password_reset_store: Dict[str, Dict[str, Any]] = {}


# 2. POST /customer/auth/login
@router.post("/auth/login", response_model=CustomerTokenResponse)
def login_customer(payload: CustomerLoginPayload, db: Session = Depends(get_db)):
    clean_email = payload.email.strip().lower()
    user = db.query(User).filter(User.email == clean_email, User.role == "customer").first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials. Please verify your email and password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    pwd_hash = user.password_hash or user.hashed_password
    pwd_ok = False
    if pwd_hash:
        try:
            pwd_ok = verify_password(payload.password, pwd_hash)
        except Exception:
            pwd_ok = False

    # Development compatibility for documented demo and legacy accounts
    if not pwd_ok:
        dev_customer_passwords = {
            "demo.customer@smartserve.com": ["DemoCustomer123!"],
            "customer@example.com": ["CustomerPass123!", "CustomerPassword123!"],
        }
        if clean_email in dev_customer_passwords and payload.password in dev_customer_passwords[clean_email]:
            pwd_ok = True

    if not pwd_ok:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials. Please verify your email and password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive or suspended.",
        )

    if user.is_2fa_enabled:
        totp_code = (payload.totp_code or "").strip()
        rec_code = (payload.recovery_code or "").strip()
        if not totp_code and not rec_code:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Two-factor authentication code required.",
                headers={"X-2FA-Required": "true", "WWW-Authenticate": "Bearer"},
            )

        from app.services import security_service
        is_2fa_valid = False
        if totp_code:
            is_2fa_valid = security_service.verify_totp_2fa(db, user, totp_code)

        if not is_2fa_valid and rec_code:
            is_2fa_valid = security_service.verify_recovery_code(db, user, rec_code)

        if not is_2fa_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid two-factor authentication code.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    customer = db.query(Customer).filter(Customer.user_id == user.id).first()
    customer_id = str(customer.id) if customer else str(user.id)
    full_name = customer.full_name if customer else user.email.split("@")[0].title()

    token_jti = f"jwt_{uuid.uuid4().hex}"
    token = create_access_token({
        "sub": str(user.id),
        "role": "customer",
        "customer_id": customer_id,
        "email": user.email,
        "jti": token_jti,
    })

    try:
        from app.services import security_service
        security_service.create_active_session(
            db, user_id=user.id, token_jti=token_jti,
            ip_address="127.0.0.1", user_agent="Customer Client",
            expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    except Exception:
        pass

    return CustomerTokenResponse(
        access_token=token,
        customer_id=customer_id,
        user_id=str(user.id),
        email=user.email,
        full_name=full_name,
        phone=customer.phone if customer else "+91 9876543210",
    )


# 2B. POST /customer/auth/complete-profile
@router.post("/auth/complete-profile", response_model=CustomerTokenResponse)
def complete_customer_profile(
    payload: CompleteProfilePayload,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Complete required profile details for customers onboarded via Google OAuth.
    Validates server-side required fields (full_name, phone), verifies non-revoked session,
    updates customer record, and issues a fully unrestricted JWT access token.
    """
    auth_header = request.headers.get("authorization", "")
    token = auth_header.replace("Bearer ", "").strip() if auth_header.startswith("Bearer ") else None
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    jwt_payload = decode_access_token(token)
    if not jwt_payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    jti = jwt_payload.get("jti")
    if jti:
        from app.models.session import ActiveSession
        revoked_sess = db.query(ActiveSession).filter(ActiveSession.token_jti == jti, ActiveSession.is_revoked == True).first()
        if revoked_sess:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked or logged out",
                headers={"WWW-Authenticate": "Bearer"},
            )

    sub = jwt_payload.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject.")

    user = None
    try:
        user_id = uuid.UUID(str(sub))
        user = db.query(User).filter(User.id == user_id).first()
    except (ValueError, TypeError):
        user = db.query(User).filter(User.email == str(sub).strip().lower()).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User account not found.")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is deactivated.")

    if user.role != "customer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Profile completion is only available for customer accounts.")

    customer = db.query(Customer).filter((Customer.user_id == user.id) | (Customer.id == user.id)).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer profile not found.")

    # Server-side validation
    full_name = payload.full_name.strip()
    if len(full_name) < 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Full name must be at least 2 characters long.")

    phone = payload.phone.strip()
    phone_digits = re.sub(r"[^\d+]", "", phone)
    if len(re.sub(r"\D", "", phone_digits)) < 10:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a valid phone number with at least 10 digits.")

    # Update customer record
    customer.full_name = full_name
    customer.phone = phone_digits
    
    pref_dict = customer.preferences if isinstance(customer.preferences, dict) else {}
    if not isinstance(customer.preferences, dict) and isinstance(customer.preferences, list):
        pref_dict = {"categories": customer.preferences}
    if payload.preferences is not None:
        if isinstance(payload.preferences, list):
            pref_dict["categories"] = payload.preferences
        elif isinstance(payload.preferences, dict):
            pref_dict.update(payload.preferences)
    if payload.location:
        loc_data = payload.location.model_dump() if hasattr(payload.location, "model_dump") else payload.location.dict()
        pref_dict["location"] = loc_data
    customer.preferences = pref_dict

    customer.is_verified = True
    customer.is_active = True

    # Revoke old temporary onboarding session
    if jti:
        from app.models.session import ActiveSession
        old_sess = db.query(ActiveSession).filter(ActiveSession.token_jti == jti).first()
        if old_sess:
            old_sess.is_revoked = True

    # Issue fully unrestricted access token
    new_token_jti = f"jwt_{uuid.uuid4().hex}"
    new_access_token = create_access_token({
        "sub": str(user.id),
        "role": "customer",
        "customer_id": str(customer.id),
        "email": user.email,
        "jti": new_token_jti,
        "pending_profile": False,
    })

    try:
        from app.services import security_service
        security_service.create_active_session(
            db, user_id=user.id, token_jti=new_token_jti,
            ip_address="127.0.0.1", user_agent="Customer Client",
            expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    except Exception:
        pass

    db.commit()
    db.refresh(customer)

    return CustomerTokenResponse(
        access_token=new_access_token,
        customer_id=str(customer.id),
        user_id=str(user.id),
        email=customer.email,
        full_name=customer.full_name,
        phone=customer.phone,
        requires_profile_completion=False,
        is_profile_complete=True,
        missing_profile_fields=[],
        is_new_user=False,
        location=get_customer_location_dict(customer),
    )


# 2C. POST /customer/auth/skip-profile
@router.post("/auth/skip-profile", response_model=CustomerTokenResponse)
def skip_customer_profile(
    payload: SkipProfilePayload,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Temporarily skip required profile completion for customer session.
    Saves any valid details (full_name, location, preferences) safely.
    Does NOT mark the profile as complete.
    Revokes the restricted pending-profile token and issues a session token
    permitting dashboard browsing while backend blocks order placement.
    """
    auth_header = request.headers.get("authorization", "")
    token = auth_header.replace("Bearer ", "").strip() if auth_header.startswith("Bearer ") else None
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    jwt_payload = decode_access_token(token)
    if not jwt_payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    jti = jwt_payload.get("jti")
    if jti:
        from app.models.session import ActiveSession
        revoked_sess = db.query(ActiveSession).filter(ActiveSession.token_jti == jti, ActiveSession.is_revoked == True).first()
        if revoked_sess:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked or logged out",
                headers={"WWW-Authenticate": "Bearer"},
            )

    sub = jwt_payload.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject.")

    user = None
    try:
        user_id = uuid.UUID(str(sub))
        user = db.query(User).filter(User.id == user_id).first()
    except (ValueError, TypeError):
        user = db.query(User).filter(User.email == str(sub).strip().lower()).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User account not found.")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is deactivated.")

    if user.role != "customer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Profile completion is only available for customer accounts.")

    customer = db.query(Customer).filter((Customer.user_id == user.id) | (Customer.id == user.id)).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer profile not found.")

    # Save any valid details entered safely
    if payload.full_name and len(payload.full_name.strip()) >= 2:
        customer.full_name = payload.full_name.strip()

    if payload.phone:
        phone_digits = re.sub(r"[^\d+]", "", payload.phone.strip())
        if len(re.sub(r"\D", "", phone_digits)) >= 10:
            customer.phone = phone_digits

    pref_dict = customer.preferences if isinstance(customer.preferences, dict) else {}
    if not isinstance(customer.preferences, dict) and isinstance(customer.preferences, list):
        pref_dict = {"categories": customer.preferences}

    if payload.preferences is not None:
        if isinstance(payload.preferences, list):
            pref_dict["categories"] = payload.preferences
        elif isinstance(payload.preferences, dict):
            pref_dict.update(payload.preferences)

    if payload.location:
        loc_data = payload.location.model_dump() if hasattr(payload.location, "model_dump") else payload.location.dict()
        pref_dict["location"] = loc_data

    customer.preferences = pref_dict

    # Revoke old temporary onboarding session
    if jti:
        from app.models.session import ActiveSession
        old_sess = db.query(ActiveSession).filter(ActiveSession.token_jti == jti).first()
        if old_sess:
            old_sess.is_revoked = True

    # Issue session access token allowing permitted browsing with pending_profile: False
    new_token_jti = f"jwt_{uuid.uuid4().hex}"
    new_access_token = create_access_token({
        "sub": str(user.id),
        "role": "customer",
        "customer_id": str(customer.id),
        "email": user.email,
        "jti": new_token_jti,
        "pending_profile": False,
    })

    try:
        from app.services import security_service
        security_service.create_active_session(
            db, user_id=user.id, token_jti=new_token_jti,
            ip_address=request.client.host if request.client else "127.0.0.1",
            user_agent=request.headers.get("user-agent", "Customer Client")[:250],
            expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    except Exception:
        pass

    db.commit()
    db.refresh(customer)

    is_complete, missing_fields = get_customer_completeness(customer)

    return CustomerTokenResponse(
        access_token=new_access_token,
        customer_id=str(customer.id),
        user_id=str(user.id),
        email=customer.email,
        full_name=customer.full_name,
        phone=customer.phone,
        requires_profile_completion=False,
        is_profile_complete=is_complete,
        missing_profile_fields=missing_fields,
        is_new_user=False,
        location=get_customer_location_dict(customer),
    )


# 3. GET /customer/auth/me
@router.get("/auth/me", response_model=CustomerSessionResponse)
def get_auth_me(current_customer: Customer = Depends(get_current_customer)):
    is_complete, missing = get_customer_completeness(current_customer)
    loc = get_customer_location_dict(current_customer)
    return CustomerSessionResponse(
        customer_id=str(current_customer.id),
        user_id=str(current_customer.user_id),
        email=current_customer.email,
        full_name=current_customer.full_name,
        phone=current_customer.phone,
        is_active=current_customer.is_active,
        is_verified=current_customer.is_verified,
        lifetime_spent=float(current_customer.lifetime_spent),
        total_bookings=current_customer.total_bookings,
        created_at=current_customer.created_at,
        preferences=current_customer.preferences if isinstance(current_customer.preferences, list) else (current_customer.preferences.get("categories") if isinstance(current_customer.preferences, dict) else []),
        is_profile_complete=is_complete,
        missing_profile_fields=missing,
        location=loc,
    )


# 3B. POST /customer/profile/location
@router.post("/profile/location")
def update_customer_location(
    payload: CustomerLocationPayload,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """
    Persist or update customer's service location in profile preferences.
    """
    loc_data = payload.model_dump() if hasattr(payload, "model_dump") else payload.dict()
    pref_dict = current_customer.preferences if isinstance(current_customer.preferences, dict) else {}
    if not isinstance(current_customer.preferences, dict) and isinstance(current_customer.preferences, list):
        pref_dict = {"categories": current_customer.preferences}

    pref_dict["location"] = loc_data
    current_customer.preferences = pref_dict
    db.commit()
    db.refresh(current_customer)
    return {"status": "ok", "location": loc_data}


# 4. POST /customer/auth/logout
@router.post("/auth/logout")
def logout_customer(
    request: Request,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """Invalidate customer active session and revoke JWT access."""
    auth_header = request.headers.get("authorization", "")
    token = auth_header.replace("Bearer ", "").strip() if auth_header.startswith("Bearer ") else None
    if token:
        payload = decode_access_token(token)
        jti = payload.get("jti") if payload else None
        if jti:
            from app.models.session import ActiveSession
            sess = db.query(ActiveSession).filter(ActiveSession.token_jti == jti).first()
            if sess:
                sess.is_revoked = True
                db.commit()
    return {"status": "ok", "message": "Signed out successfully"}


def create_password_reset_token(db: Session, user: User, raw_token: Optional[str] = None) -> str:
    """Generate and persist a single-use SHA-256 hashed password reset token."""
    if not raw_token:
        raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=15)

    # Invalidate any existing unused reset tokens for this user
    db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.is_used == False
    ).update({"is_used": True, "used_at": now}, synchronize_session=False)

    reset_record = PasswordResetToken(
        id=uuid.uuid4(),
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
        is_used=False
    )
    db.add(reset_record)
    db.commit()

    return raw_token


# 5. POST /customer/auth/forgot-password
@router.post("/auth/forgot-password")
def forgot_password(payload: ForgotPasswordPayload, db: Session = Depends(get_db)):
    """Generate time-limited secure reset token and return generic confirmation to prevent user enumeration."""
    clean_email = payload.email.strip().lower()
    user = db.query(User).filter(User.email == clean_email, User.role == "customer").first()
    if user:
        raw_token = create_password_reset_token(db, user)
        try:
            from app.services import email_service
            reset_url = f"{settings.FRONTEND_URL}/reset-password?token={raw_token}"
            body_text = (
                f"Hello,\n\n"
                f"A password reset request was received for your SmartServe account.\n"
                f"Please reset your password within 15 minutes using this secure link:\n\n"
                f"{reset_url}\n\n"
                f"If you did not request this, please ignore this email. Your account remains secure.\n\n"
                f"— The SmartServe Security Team"
            )
            body_html = (
                f"<div style='font-family: sans-serif; color: #1F2A1E; line-height: 1.5;'>"
                f"<h2>SmartServe Password Reset</h2>"
                f"<p>A password reset request was received for your SmartServe account.</p>"
                f"<p><a href='{reset_url}' style='background-color: #2F5233; color: white; padding: 10px 20px; text-decoration: none; border-radius: 6px; font-weight: bold;'>Reset Password</a></p>"
                f"<p>This link is single-use and will expire in 15 minutes.</p>"
                f"<p style='color: #666; font-size: 12px;'>If you did not request this change, you can safely ignore this email.</p>"
                f"</div>"
            )
            email_service.send_email_dispatch(
                db,
                recipient_email=user.email,
                subject="SmartServe Password Reset Instructions",
                body_text=body_text,
                body_html=body_html,
                template_key="password_reset",
                actor_email="system@smartserve.com"
            )
        except Exception as exc:
            logger.warning(f"[ForgotPassword] Dispatch suppressed: {type(exc).__name__}")
    return {"status": "ok", "message": "If the email exists, reset instructions have been sent."}


# 6. POST /customer/auth/reset-password
@router.post("/auth/reset-password")
def reset_password(payload: ResetPasswordPayload, db: Session = Depends(get_db)):
    """Verify single-use reset token and update password hash securely using atomic updates."""
    clean_token = (payload.token or "").strip()
    if not clean_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password reset token is invalid or has expired."
        )

    if not payload.new_password or len(payload.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be at least 8 characters long."
        )

    token_hash = hashlib.sha256(clean_token.encode("utf-8")).hexdigest()
    now = datetime.now(timezone.utc)

    # Atomic single-use update: only 1 concurrent execution can succeed
    stmt = (
        update(PasswordResetToken)
        .where(
            PasswordResetToken.token_hash == token_hash,
            PasswordResetToken.is_used == False,
            PasswordResetToken.expires_at > now,
        )
        .values(is_used=True, used_at=now)
    )
    res = db.execute(stmt)
    if res.rowcount == 0:
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password reset token is invalid or has expired."
        )

    token_record = db.query(PasswordResetToken).filter(PasswordResetToken.token_hash == token_hash).first()
    if not token_record:
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password reset token is invalid or has expired."
        )

    user = db.query(User).filter(User.id == token_record.user_id).first()
    if not user:
        db.commit()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User account not found.")

    user.password_hash = hash_password(payload.new_password)
    db.commit()

    # Revoke all active sessions to invalidate any stolen or active JWT sessions
    try:
        from app.services.security_service import revoke_all_user_sessions
        revoke_all_user_sessions(db, user.id)
    except Exception:
        pass

    try:
        from app.repositories import audit_repository
        audit_repository.create_audit_log(
            db, actor_id=user.id, actor_email=user.email, actor_role="customer",
            action="Password Reset Completed", risk_level="Info",
            target_resource=str(user.id),
        )
    except Exception:
        pass
    return {"status": "ok", "message": "Password reset successfully."}



# 7. POST /customer/auth/change-password
@router.post("/auth/change-password")
def change_password(payload: ChangePasswordPayload, current_customer: Customer = Depends(get_current_customer), db: Session = Depends(get_db)):
    if not payload.new_password or len(payload.new_password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password must be at least 8 characters long.")
    user = db.query(User).filter(User.id == current_customer.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User account not found.")
    pwd_hash = user.password_hash or user.hashed_password
    if not pwd_hash or not verify_password(payload.current_password, pwd_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
    user.password_hash = hash_password(payload.new_password)
    db.commit()

    # Invalidate all active sessions for this user on password change
    try:
        from app.services.security_service import revoke_all_user_sessions
        revoke_all_user_sessions(db, user.id)
    except Exception:
        pass

    try:
        from app.repositories import audit_repository
        audit_repository.create_audit_log(
            db, actor_id=user.id, actor_email=user.email, actor_role="customer",
            action="Password Changed", risk_level="Info",
            target_resource=str(user.id),
        )
    except Exception:
        pass
    return {"status": "ok", "message": "Password updated successfully"}


# 8. GET /customer/profile
@router.get("/profile", response_model=CustomerSessionResponse)
def get_profile(current_customer: Customer = Depends(get_current_customer)):
    is_complete, missing = get_customer_completeness(current_customer)
    loc = get_customer_location_dict(current_customer)
    return CustomerSessionResponse(
        customer_id=str(current_customer.id),
        user_id=str(current_customer.user_id),
        email=current_customer.email,
        full_name=current_customer.full_name,
        phone=current_customer.phone,
        is_active=current_customer.is_active,
        is_verified=current_customer.is_verified,
        lifetime_spent=float(current_customer.lifetime_spent),
        total_bookings=current_customer.total_bookings,
        created_at=current_customer.created_at,
        preferences=current_customer.preferences if isinstance(current_customer.preferences, list) else (current_customer.preferences.get("categories") if isinstance(current_customer.preferences, dict) else []),
        is_profile_complete=is_complete,
        missing_profile_fields=missing,
        location=loc,
    )


# 9. PATCH /customer/profile
@router.patch("/profile", response_model=CustomerSessionResponse)
def update_profile(
    payload: CustomerProfileUpdate,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    if payload.full_name:
        current_customer.full_name = payload.full_name
    if payload.email:
        current_customer.email = payload.email
    if payload.phone:
        current_customer.phone = payload.phone

    db.add(current_customer)
    db.commit()
    db.refresh(current_customer)

    is_complete, missing = get_customer_completeness(current_customer)
    loc = get_customer_location_dict(current_customer)

    return CustomerSessionResponse(
        customer_id=str(current_customer.id),
        user_id=str(current_customer.user_id),
        email=current_customer.email,
        full_name=current_customer.full_name,
        phone=current_customer.phone,
        is_active=current_customer.is_active,
        is_verified=current_customer.is_verified,
        lifetime_spent=float(current_customer.lifetime_spent),
        total_bookings=current_customer.total_bookings,
        created_at=current_customer.created_at,
        preferences=current_customer.preferences if isinstance(current_customer.preferences, list) else (current_customer.preferences.get("categories") if isinstance(current_customer.preferences, dict) else []),
        is_profile_complete=is_complete,
        missing_profile_fields=missing,
        location=loc,
    )


# 10. GET /customer/dashboard
@router.get("/dashboard")
def get_dashboard(current_customer: Customer = Depends(get_current_customer), db: Session = Depends(get_db)):
    from app.models.service import Service
    db_services = db.query(Service).filter(Service.is_active == True).all()
    cat_map = {}
    srv_list = []
    for s in db_services:
        if s.category not in cat_map:
            slug = s.category.lower().replace(" & ", "-").replace(" ", "-")
            cat_map[s.category] = CategoryItem(
                id=f"cat-{slug}",
                name=s.category,
                slug=slug,
                image=None,
                service_count=1
            )
        else:
            cat_map[s.category].service_count += 1
        
        if len(srv_list) < 6:
            srv_list.append(ServiceItem(
                id=str(s.id),
                name=s.name,
                category=s.category,
                category_slug=s.category.lower().replace(" & ", "-").replace(" ", "-"),
                subcategory=s.subcategory,
                subcategory_slug=s.subcategory.lower().replace(" & ", "-").replace(" ", "-"),
                description=f"Professional {s.name} service managed under {s.category}.",
                features=s.distinct_features if isinstance(s.distinct_features, list) else [],
                base_price=float(s.base_price),
                duration_minutes=60,
                rating=4.8,
                review_count=120,
                is_emergency=False,
                image_url=None,
                suggested_addons=[],
                process_steps=[],
                faqs=[]
            ))

    is_complete, missing = get_customer_completeness(current_customer)
    loc = get_customer_location_dict(current_customer)

    return {
        "greeting_name": current_customer.full_name,
        "is_profile_complete": is_complete,
        "missing_profile_fields": missing,
        "saved_location": loc,
        "categories": list(cat_map.values())[:8],
        "featured_services": srv_list,
        "recent_bookings": [],
    }


import re

def get_category_order(name: str) -> int:
    m = re.match(r"^(\d+)\.", name)
    return int(m.group(1)) if m else 999

def format_category_display_name(raw: str) -> str:
    cleaned = re.sub(r"^\d+\.\s*", "", raw)
    return cleaned.strip()

# 11. GET /customer/catalog/categories
@router.get("/catalog/categories", response_model=List[CategoryItem])
def get_catalog_categories(db: Session = Depends(get_db)):
    cache = get_cache()
    cached_categories = cache.get("customer:catalog:categories")
    if cached_categories is not None:
        return cached_categories

    from app.models.service import Service
    from sqlalchemy import func

    # Ultra-fast SQL aggregation using covering index (103 summary rows instead of 747 heavy full rows)
    rows = (
        db.query(
            Service.category,
            Service.subcategory,
            func.count(Service.id).label("cnt")
        )
        .filter(Service.is_active == True)
        .group_by(Service.category, Service.subcategory)
        .all()
    )
    
    cat_map: Dict[str, Dict[str, Any]] = {}
    for cat, sub, count in rows:
        cat_name = cat or "General"
        sub_name = sub or "General"
        if cat_name not in cat_map:
            slug = cat_name.lower().replace(" & ", "-").replace(" ", "-")
            cat_map[cat_name] = {
                "id": f"cat-{slug}",
                "name": cat_name,
                "slug": slug,
                "display_name": format_category_display_name(cat_name),
                "order": get_category_order(cat_name),
                "subcategories": {},
                "service_count": 0,
                "active_count": 0
            }
        
        cat_map[cat_name]["service_count"] += count
        cat_map[cat_name]["active_count"] += count
        
        sub_dict = cat_map[cat_name]["subcategories"]
        if sub_name not in sub_dict:
            sub_dict[sub_name] = {"name": sub_name, "service_count": 0, "active_count": 0}
        sub_dict[sub_name]["service_count"] += count
        sub_dict[sub_name]["active_count"] += count

    result = []
    for cat_data in cat_map.values():
        sub_list = [
            SubcategorySummary(
                name=sub_info["name"],
                service_count=sub_info["service_count"],
                active_count=sub_info["active_count"]
            )
            for sub_info in sorted(cat_data["subcategories"].values(), key=lambda x: x["name"])
        ]
        result.append(CategoryItem(
            id=cat_data["id"],
            name=cat_data["name"],
            slug=cat_data["slug"],
            display_name=cat_data["display_name"],
            order=cat_data["order"],
            subcategories_count=len(sub_list),
            service_count=cat_data["service_count"],
            active_count=cat_data["active_count"],
            subcategories=sub_list
        ))

    result.sort(key=lambda c: (c.order, c.display_name or c.name))
    cache.set("customer:catalog:categories", result, ttl_seconds=600)
    return result


def normalize_to_strings(raw_list) -> List[str]:
    if not isinstance(raw_list, list):
        return []
    res = []
    for elem in raw_list:
        if isinstance(elem, str):
            res.append(elem)
        elif isinstance(elem, dict):
            title = elem.get("title") or elem.get("name") or elem.get("label") or elem.get("step")
            desc = elem.get("description") or elem.get("desc") or elem.get("detail") or elem.get("details") or elem.get("text")
            if title and desc:
                res.append(f"{title}: {desc}")
            elif desc:
                res.append(str(desc))
            elif title:
                res.append(str(title))
            else:
                vals = [str(v) for v in elem.values() if v]
                res.append(": ".join(vals) if vals else str(elem))
        elif elem is not None:
            res.append(str(elem))
    return res


def parse_service_details(s) -> ServiceItem:
    cat_slug = s.category.lower().replace(" & ", "-").replace(" ", "-") if s.category else ""
    sub_slug = s.subcategory.lower().replace(" & ", "-").replace(" ", "-") if s.subcategory else ""

    included_features = normalize_to_strings(s.distinct_features)
    
    addons: List[AddonItem] = []
    process_steps: List[ServiceProcessStep] = []
    service_features: List[ServiceFeatureItem] = []
    service_media: List[ServiceMediaItem] = []
    faqs: List[ServiceFAQ] = []
    excluded: List[Any] = []
    tools_materials: List[Any] = []
    customer_setup: List[Any] = []
    aftercare: List[Any] = []
    expected_results: List[Any] = []
    important_notes: List[Any] = []
    highlights: List[Any] = []
    tips: List[Any] = []
    dos: List[Any] = []
    donts: List[Any] = []
    warranty_detail: Optional[str] = None
    description_text: Optional[str] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    keywords: List[str] = []
    explicit_duration: Optional[int] = None
    calc_duration: int = 0

    if s.suggested_addons and isinstance(s.suggested_addons, list):
        for idx, item in enumerate(s.suggested_addons):
            if not isinstance(item, dict):
                continue
            
            i_type = item.get("type")
            
            if i_type in ["description", "service_description"]:
                description_text = item.get("text") or item.get("description") or item.get("content")
            elif i_type == "seo_metadata":
                if not description_text and item.get("seo_description"):
                    description_text = item.get("seo_description")
                seo_title = item.get("seo_title")
                seo_description = item.get("seo_description")
                if isinstance(item.get("keywords"), list):
                    keywords = [str(k) for k in item.get("keywords")]
                if isinstance(item.get("highlights"), list):
                    highlights = item.get("highlights")
            elif i_type == "highlights":
                hl = item.get("highlights") or item.get("items") or []
                if isinstance(hl, list):
                    highlights = hl
            elif i_type in ["duration", "estimated_duration"]:
                mins = item.get("minutes") or item.get("duration") or item.get("duration_minutes")
                if mins:
                    try:
                        explicit_duration = int(mins)
                    except (ValueError, TypeError):
                        pass
            elif i_type in ["excluded", "excluded_scope"]:
                ex = item.get("excluded") or item.get("items") or []
                if isinstance(ex, list):
                    excluded = ex
            elif i_type == "process_steps":
                steps_data = item.get("steps") or item.get("items") or []
                if isinstance(steps_data, list):
                    for st in steps_data:
                        if isinstance(st, dict):
                            dur = int(st.get("duration_minutes", 15)) if st.get("duration_minutes") else 15
                            calc_duration += dur
                            process_steps.append(ServiceProcessStep(
                                step_number=int(st.get("step_number", len(process_steps) + 1)),
                                title=str(st.get("title", f"Step {len(process_steps) + 1}")),
                                description=str(st.get("description", "")),
                                duration_minutes=dur,
                                is_key_step=bool(st.get("is_key_step", False))
                            ))
            elif i_type == "service_features":
                sf = item.get("items") or item.get("features") or []
                if isinstance(sf, list):
                    for f in sf:
                        if isinstance(f, dict) and (f.get("title") or f.get("description")):
                            service_features.append(ServiceFeatureItem(
                                title=str(f.get("title", "")),
                                description=str(f.get("description", ""))
                            ))
            elif i_type == "service_media":
                sm = item.get("items") or item.get("media") or []
                if isinstance(sm, list):
                    for m in sm:
                        if isinstance(m, dict) and m.get("url"):
                            service_media.append(ServiceMediaItem(
                                id=str(m.get("id")) if m.get("id") else None,
                                url=str(m.get("url")),
                                caption=str(m.get("caption", "")),
                                media_type=str(m.get("media_type", "image")),
                                is_cover=bool(m.get("is_cover", False))
                            ))
            elif i_type in ["tools_materials", "products_and_tools"]:
                pt = item.get("products_and_tools") or item.get("items") or []
                if isinstance(pt, list) and pt:
                    tools_materials.extend(pt)
                else:
                    tools = item.get("tools") or []
                    mats = item.get("materials") or []
                    if isinstance(tools, list):
                        tools_materials.extend(tools)
                    if isinstance(mats, list):
                        tools_materials.extend(mats)
            elif i_type in ["customer_setup", "preparation"]:
                reqs = item.get("setup") or item.get("requirements") or item.get("items") or []
                if isinstance(reqs, list):
                    customer_setup = reqs
            elif i_type == "aftercare_precautions":
                ac = item.get("aftercare") or item.get("items") or []
                if isinstance(ac, list):
                    aftercare = ac
            elif i_type == "expected_results":
                exp = item.get("items") or item.get("results") or []
                if isinstance(exp, list):
                    expected_results = exp
            elif i_type == "important_notes":
                notes = item.get("items") or item.get("notes") or []
                if isinstance(notes, list):
                    important_notes = notes
            elif i_type == "tips":
                tp = item.get("items") or item.get("tips") or []
                if isinstance(tp, list):
                    tips = tp
            elif i_type in ["dos_donts", "dos_and_donts"]:
                if isinstance(item.get("dos"), list):
                    dos = item.get("dos")
                if isinstance(item.get("donts"), list):
                    donts = item.get("donts")
            elif i_type == "warranty":
                has_w = item.get("has_warranty", True)
                if has_w:
                    warranty_detail = item.get("details") or item.get("warranty")
            elif i_type == "faqs":
                faq_items = item.get("items") or item.get("faqs") or []
                if isinstance(faq_items, list):
                    for f in faq_items:
                        if isinstance(f, dict) and f.get("question"):
                            faqs.append(ServiceFAQ(
                                question=str(f.get("question")),
                                answer=str(f.get("answer", ""))
                            ))
            elif "price" in item and ("name" in item or "addon_id" in item):
                addons.append(AddonItem(
                    addon_id=str(item.get("addon_id", f"add-{idx}")),
                    name=str(item.get("name", "Add-on")),
                    price=float(item.get("price", 0.0)),
                    description=item.get("description")
                ))
            elif not description_text and item.get("description") and not i_type:
                description_text = item.get("description")

    duration_minutes = explicit_duration if explicit_duration is not None else (calc_duration if calc_duration > 0 else 45)

    cover_media = next((m.url for m in service_media if m.is_cover), None)
    first_media = service_media[0].url if service_media else None
    resolved_image = cover_media or first_media or None

    return ServiceItem(
        id=str(s.id),
        name=s.name,
        category=s.category,
        category_slug=cat_slug,
        subcategory=s.subcategory,
        subcategory_slug=sub_slug,
        description=description_text,
        distinct_features=included_features,
        features=included_features,
        included=included_features,
        excluded=normalize_to_strings(excluded),
        highlights=normalize_to_strings(highlights),
        base_price=float(s.base_price),
        max_demand_increase=float(s.max_demand_increase or 0.0),
        max_discount=float(s.max_discount or 0.0),
        duration_minutes=duration_minutes,
        rating=4.8,
        review_count=120,
        is_emergency=bool(getattr(s, "is_emergency_eligible", False)),
        is_emergency_eligible=bool(getattr(s, "is_emergency_eligible", False)),
        is_active=s.is_active,
        image_url=resolved_image,
        suggested_addons=addons,
        process_steps=process_steps,
        tools_materials=normalize_to_strings(tools_materials),
        customer_setup=normalize_to_strings(customer_setup),
        aftercare=normalize_to_strings(aftercare),
        expected_results=normalize_to_strings(expected_results),
        important_notes=normalize_to_strings(important_notes),
        warranty=warranty_detail,
        faqs=faqs,
        tips=normalize_to_strings(tips),
        dos=normalize_to_strings(dos),
        donts=normalize_to_strings(donts),
        seo_title=seo_title,
        seo_description=seo_description,
        keywords=keywords,
        service_features=service_features,
        service_media=service_media,
        created_at=s.created_at,
        updated_at=s.updated_at
    )


# 12. GET /customer/catalog/services
@router.get("/catalog/services", response_model=List[ServiceItem])
def get_catalog_services(
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    emergency_only: Optional[bool] = False,
    q: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: Optional[int] = Query(None, ge=1, le=500),
    db: Session = Depends(get_db),
):
    cache = get_cache()
    cache_key = f"customer:catalog:services:{category}:{subcategory}:{emergency_only}:{q}:{skip}:{limit}"
    cached_res = cache.get(cache_key)
    if cached_res is not None:
        return cached_res

    from app.models.service import Service
    query = db.query(Service).filter(Service.is_active == True)
    if category:
        clean_cat = category.strip()
        cat_no_num = re.sub(r'^\d+[\.\-]*\s*', '', clean_cat).replace("-", " ")
        slug_clean = re.sub(r'^\d+[\.\-]*\s*', '', clean_cat).replace("-", "%").replace(",", "%")
        query = query.filter(
            (Service.category.ilike(f"%{clean_cat}%")) | 
            (Service.category.ilike(f"%{cat_no_num}%")) |
            (Service.category.ilike(f"%{slug_clean}%"))
        )
    if subcategory:
        clean_sub = subcategory.strip().lower()
        if clean_sub in ["men's salon", "mens salon"]:
            query = query.filter(func.lower(func.trim(Service.subcategory)) == "men's salon")
        elif clean_sub in ["women's salon", "womens salon"]:
            query = query.filter(func.lower(func.trim(Service.subcategory)) == "women's salon")
        elif clean_sub == "ac":
            query = query.filter(func.lower(func.trim(Service.subcategory)) == "ac")
        else:
            clean_sub_fuzzy = clean_sub.replace("-", " ")
            query = query.filter(
                (func.lower(func.trim(Service.subcategory)) == clean_sub) |
                (func.lower(func.trim(Service.subcategory)) == clean_sub_fuzzy) |
                (Service.subcategory.ilike(f"%{clean_sub}%")) |
                (Service.subcategory.ilike(f"%{clean_sub_fuzzy}%"))
            )
    if q:
        query = query.filter((Service.name.ilike(f"%{q}%")) | (Service.category.ilike(f"%{q}%")) | (Service.subcategory.ilike(f"%{q}%")))

    if skip > 0:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)

    db_services = query.all()
    res = [parse_service_details(s) for s in db_services]
    cache.set(cache_key, res, ttl_seconds=300)
    return res


# 13. GET /customer/catalog/services/{id}
@router.get("/catalog/services/{service_id}", response_model=ServiceItem)
def get_catalog_service_by_id(service_id: str, db: Session = Depends(get_db)):
    cache = get_cache()
    cache_key = f"customer:catalog:service:{service_id}"
    cached_svc = cache.get(cache_key)
    if cached_svc is not None:
        return cached_svc

    from app.models.service import Service
    try:
        s_uuid = uuid.UUID(service_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid service ID format")

    s = db.query(Service).filter(Service.id == s_uuid).first()
    if not s:
        raise HTTPException(status_code=404, detail="Service not found in catalog")

    res = parse_service_details(s)
    cache.set(cache_key, res, ttl_seconds=300)
    return res


# 13b. GET /customer/catalog/services/{service_id}/eligible-providers
@router.get("/catalog/services/{service_id}/eligible-providers", response_model=List[EligibleProviderResponse])
def get_service_eligible_providers(service_id: str, db: Session = Depends(get_db)):
    from app.services.booking.eligibility_service import get_eligible_providers
    try:
        s_uuid = uuid.UUID(service_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid service ID format")

    providers_data = get_eligible_providers(db, s_uuid)
    return [EligibleProviderResponse(**p) for p in providers_data]



def _sanitize_photos(photos):
    if not photos:
        return []
    cleaned = []
    for p in photos:
        if isinstance(p, str):
            if p.startswith("/static/"):
                cleaned.append(f"https://smartserve-api-de3f.onrender.com{p}")
            elif p.startswith("data:image"):
                if len(p) <= 120000:
                    cleaned.append(p)
                else:
                    cleaned.append("https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=600&q=80")
            else:
                cleaned.append(p)
    return cleaned


def safe_timeline(raw_timeline):
    if isinstance(raw_timeline, list):
        return [x if isinstance(x, dict) else {"event": str(x)} for x in raw_timeline]
    if isinstance(raw_timeline, dict):
        return [raw_timeline]
    return []

# 14. GET /customer/bookings
@router.get("/bookings", response_model=List[BookingDetail])
def get_customer_bookings(
    status_filter: Optional[str] = None,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    from sqlalchemy.orm import joinedload
    query = (
        db.query(Booking)
        .options(
            joinedload(Booking.service),
            joinedload(Booking.warranty),
            joinedload(Booking.provider),
        )
        .filter(Booking.customer_id == current_customer.id)
    )
    if status_filter and status_filter.upper() != "ALL":
        query = query.filter(func.lower(Booking.status) == status_filter.lower())

    records = query.order_by(Booking.created_at.desc()).all()
    if not records:
        return []

    return [
        BookingDetail(
            id=str(b.id),
            booking_reference=b.booking_reference,
            customer_id=str(b.customer_id),
            service_id=str(b.service_id),
            service_name=b.get_service_name() if hasattr(b, "get_service_name") else (b.service_name or "Home Service"),
            category=b.get_category() if hasattr(b, "get_category") else (b.category or "General"),
            status=str(b.status.value if hasattr(b.status, "value") else b.status),
            scheduled_date=b.scheduled_date,
            scheduled_time=b.scheduled_time.strftime("%H:%M:%S") if hasattr(b.scheduled_time, "strftime") else str(b.scheduled_time),
            address_line1=b.address_line1,
            landmark=b.landmark,
            city=b.city,
            pincode=b.pincode,
            total_price=float(b.total_price),
            payment_method=b.payment_method or "COD",
            payment_status=b.payment_status or "Pending",
            cancellation_reason=b.cancellation_reason,
            notes=b.notes,
            customer_notes=b.customer_notes or b.notes,
            coupon_code=getattr(b, "coupon_code", None),
            coupon_discount=float(getattr(b, "coupon_discount", 0.0) or 0.0),
            before_photos=_sanitize_photos(b.before_photos),
            after_photos=_sanitize_photos(b.after_photos),
            warranty={
                "id": str(b.warranty.id),
                "booking_id": str(b.warranty.booking_id),
                "service_name": b.warranty.service_name,
                "issued_at": b.warranty.issued_at.isoformat() if b.warranty.issued_at else None,
                "expires_at": b.warranty.expires_at.isoformat() if b.warranty.expires_at else None,
                "is_active": b.warranty.is_active,
                "claim_status": b.warranty.claim_status,
                "claim_description": b.warranty.claim_description,
                "claim_submitted_at": b.warranty.claim_submitted_at.isoformat() if b.warranty.claim_submitted_at else None,
                "claim_resolved_at": b.warranty.claim_resolved_at.isoformat() if b.warranty.claim_resolved_at else None,
                "claim_notes": b.warranty.claim_notes,
                "days_remaining": max(0, (b.warranty.expires_at.date() - datetime.utcnow().date()).days) if b.warranty.expires_at else 0,
            } if b.warranty else None,
            provider_id=str(b.provider_id) if b.provider_id else None,
            provider_name=b.provider.full_name if b.provider else None,
            otp_code=b.completion_otp if str(b.status).lower() == 'started' else b.start_otp,
            start_otp=b.start_otp,
            completion_otp=b.completion_otp,
            emergency_flag=b.emergency_flag,
            timeline=safe_timeline(b.timeline),
            created_at=b.created_at,
        )
        for b in records
    ]


# 15. POST /customer/bookings
@router.post("/bookings", response_model=BookingDetail)
def create_customer_booking(
    payload: CreateBookingPayload,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    from app.models.service import Service
    from app.services.booking.eligibility_service import find_eligible_provider, parse_scheduled_datetime

    # 0. Backend Profile Completeness Check
    is_complete, missing_fields = get_customer_completeness(current_customer)
    if not is_complete:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "PROFILE_INCOMPLETE",
                "message": "Your profile is not complete yet. Please provide required profile details (e.g. mobile phone number) before placing an order.",
                "missing_fields": missing_fields,
            }
        )

    # 0b. Validate Location
    loc_dict = get_customer_location_dict(current_customer)
    resolved_address = payload.address_line1.strip() if payload.address_line1 and payload.address_line1.strip() else None
    if not resolved_address and loc_dict and loc_dict.get("address"):
        resolved_address = loc_dict["address"]
        if loc_dict.get("city") and loc_dict["city"] not in resolved_address:
            resolved_address += f", {loc_dict['city']}"

    if not resolved_address:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A service location is required to place a booking. Please provide an address or set your service location."
        )

    resolved_city = payload.city or (loc_dict.get("city") if loc_dict else None) or "Noida"
    resolved_pincode = payload.pincode or (loc_dict.get("postal_code") if loc_dict else None) or "201301"

    db_service = None
    try:
        s_uuid = uuid.UUID(payload.service_id)
        db_service = db.query(Service).filter(Service.id == s_uuid).first()
    except Exception:
        db_service = None

    if not db_service:
        raise HTTPException(status_code=404, detail="Selected service is not found in catalog")

    if not db_service.is_active:
        raise HTTPException(status_code=400, detail="Cannot book an inactive or unpublished service")

    srv_id = db_service.id
    srv_name = db_service.name
    srv_category = db_service.category
    base_price = float(db_service.base_price)

    addons_sum = 0.0
    total_price = base_price + addons_sum
    ref_code = f"BK-{uuid.uuid4().hex[:6].upper()}"

    parsed_sched_time = parse_scheduled_datetime(payload.scheduled_date, payload.scheduled_time)

    is_emergency = bool(getattr(db_service, "is_emergency_eligible", False))

    requested_prov_uuid = None
    if not is_emergency and payload.provider_id:
        try:
            requested_prov_uuid = uuid.UUID(payload.provider_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid provider ID format")

    # Determine eligible provider based on approved status, service association, availability, and requested slot
    eligible_provider, matched_slot, eligibility_msg = find_eligible_provider(
        db, srv_id, parsed_sched_time, requested_provider_id=requested_prov_uuid
    )

    if not eligible_provider:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to book service: {eligibility_msg}. Please select another date or time slot when a verified provider is available."
        )

    otp_code = str(uuid.uuid4().int)[:4]
    event_title = "Emergency Fast-Track Dispatch" if is_emergency else "Booking Requested"
    initial_event = {
        "event": event_title,
        "status": "Requested",
        "provider_assigned": eligible_provider.full_name,
        "provider_id": str(eligible_provider.user_id),
        "timestamp": datetime.utcnow().isoformat(),
    }

    coupon_obj = None
    coupon_discount = Decimal("0.00")
    if payload.coupon_code:
        from app.services.coupon_service import validate_coupon
        is_valid, c_msg, c_disc, coupon_obj = validate_coupon(
            db=db,
            code=payload.coupon_code,
            customer_id=current_customer.id,
            subtotal=Decimal(str(total_price)),
            category=srv_category,
            service_id=srv_id,
        )
        if not is_valid:
            raise HTTPException(status_code=400, detail=c_msg)
        coupon_discount = c_disc
        total_price = max(0.0, float(Decimal(str(total_price)) - coupon_discount))
        initial_event["coupon_applied"] = coupon_obj.code
        initial_event["coupon_discount"] = float(coupon_discount)

    new_booking = Booking(
        id=uuid.uuid4(),
        booking_reference=ref_code,
        customer_id=current_customer.id,
        provider_id=eligible_provider.user_id,
        service_id=srv_id,
        service_name=srv_name,
        category=srv_category,
        status="Requested",
        payment_method="COD",
        payment_status="Pending",
        scheduled_date=payload.scheduled_date,
        scheduled_time=parsed_sched_time,
        address_line1=resolved_address,
        landmark=payload.landmark,
        city=resolved_city,
        pincode=resolved_pincode,
        total_price=total_price,
        notes=payload.notes,
        timeline=[initial_event],
        emergency_flag="EMERGENCY" if is_emergency else None,
        coupon_code=coupon_obj.code if coupon_obj else None,
        coupon_discount=coupon_discount,
        created_at=datetime.utcnow(),
    )
    if matched_slot:
        matched_slot.status = "RESERVED"
        db.add(matched_slot)

    current_customer.total_bookings = (current_customer.total_bookings or 0) + 1
    current_customer.lifetime_spent = (current_customer.lifetime_spent or Decimal("0.00")) + Decimal(str(total_price))

    db.add(new_booking)
    db.add(current_customer)
    if coupon_obj:
        from app.services.coupon_service import redeem_coupon
        redeem_coupon(
            db=db,
            coupon_id=coupon_obj.id,
            customer_id=current_customer.id,
            subtotal=Decimal(str(base_price + addons_sum)),
            booking_id=new_booking.id,
            category=srv_category,
            service_id=srv_id,
        )
    db.commit()
    db.refresh(new_booking)

    # Generate cryptographically secure START OTP and initial BookingPayment record
    from app.services.booking.otp_service import generate_secure_otp
    from app.models.payment import BookingPayment
    secure_start_otp = generate_secure_otp(new_booking.id, "START", db)
    new_booking.otp_code = secure_start_otp.otp_code

    initial_payment = BookingPayment(
        id=uuid.uuid4(),
        booking_id=new_booking.id,
        customer_id=current_customer.id,
        provider_id=eligible_provider.user_id if eligible_provider else None,
        payment_method="COD",
        agreed_amount=Decimal(str(total_price)),
        status="Pending",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(initial_payment)
    db.commit()
    db.refresh(new_booking)

    # Automated Notification Trigger: Booking Confirmed
    try:
        from app.services.notification import notify_booking_event
        notify_booking_event(db, new_booking, "booking.confirmed")
    except Exception as exc:
        pass

    sched_time_str = (
        new_booking.scheduled_time.strftime("%H:%M:%S")
        if hasattr(new_booking.scheduled_time, "strftime")
        else str(new_booking.scheduled_time)
    )

    booking_payload = {
        "booking_id": str(new_booking.id),
        "booking_reference": new_booking.booking_reference,
        "customer_id": str(current_customer.id),
        "customer_name": current_customer.full_name,
        "customer_phone": current_customer.phone,
        "provider_id": str(new_booking.provider_id) if new_booking.provider_id else None,
        "provider_name": eligible_provider.full_name if eligible_provider else None,
        "service_id": str(srv_id),
        "service_name": srv_name,
        "category": srv_category,
        "status": str(new_booking.status),
        "scheduled_date": new_booking.scheduled_date,
        "scheduled_time": sched_time_str,
        "address": new_booking.address_line1,
        "total_price": float(new_booking.total_price),
        "emergency_flag": new_booking.emergency_flag,
        "created_at": new_booking.created_at.isoformat() if hasattr(new_booking.created_at, "isoformat") else str(new_booking.created_at),
    }

    # Direct realtime WebSocket broadcast (Phase 1: No Kafka required)
    from app.core.websockets import broadcast_realtime
    channels = ["dashboard", "bookings", f"booking_{new_booking.id}"]
    if new_booking.provider_id:
        channels.extend([f"provider_{new_booking.provider_id}", f"user_{new_booking.provider_id}"])
    channels.extend([f"customer_{current_customer.id}", f"user_{current_customer.id}"])

    broadcast_realtime(channels, {
        "type": "BOOKING_CREATED",
        "event": "booking.created",
        "event_type": "booking.created",
        "booking_id": str(new_booking.id),
        "status": "Requested",
        "booking": booking_payload,
        "data": booking_payload,
    })

    # Optional background Kafka notification if available
    try:
        from app.services.kafka import kafka_producer, KafkaTopics, KafkaEvent
        booking_event = KafkaEvent(
            event_type=KafkaTopics.BOOKING_CREATED,
            booking_id=str(new_booking.id),
            sender_id=str(current_customer.id),
            receiver_id=str(new_booking.provider_id) if new_booking.provider_id else None,
            payload=booking_payload
        )
        kafka_producer.publish_event(KafkaTopics.BOOKING_CREATED, booking_event)
    except Exception:
        pass

    return BookingDetail(
        id=str(new_booking.id),
        booking_reference=new_booking.booking_reference,
        customer_id=str(new_booking.customer_id),
        provider_id=str(new_booking.provider_id) if new_booking.provider_id else None,
        provider_name=eligible_provider.full_name if eligible_provider else None,
        service_id=str(new_booking.service_id),
        service_name=new_booking.service_name,
        category=new_booking.category,
        status=str(new_booking.status),
        scheduled_date=new_booking.scheduled_date,
        scheduled_time=sched_time_str,
        address_line1=new_booking.address_line1,
        landmark=new_booking.landmark,
        city=new_booking.city,
        pincode=new_booking.pincode,
        total_price=float(new_booking.total_price),
        payment_method=new_booking.payment_method or "COD",
        payment_status=new_booking.payment_status or "Pending",
        notes=new_booking.notes,
        coupon_code=new_booking.coupon_code,
        coupon_discount=float(new_booking.coupon_discount or 0.0),
        otp_code=new_booking.start_otp,
        start_otp=new_booking.start_otp,
        completion_otp=new_booking.completion_otp,
        emergency_flag=new_booking.emergency_flag,
        timeline=new_booking.timeline,
        created_at=new_booking.created_at,
    )


# 16. GET /customer/bookings/{id}
@router.get("/bookings/{booking_id}", response_model=BookingDetail)
def get_booking_by_id(
    booking_id: str,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    # Strict lookup: check if booking exists in DB first
    record = (
        db.query(Booking)
        .filter((Booking.id == booking_id) | (Booking.booking_reference == booking_id))
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Strict RBAC: Ensure requesting customer owns this booking
    if record.customer_id != current_customer.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You cannot access bookings belonging to another customer",
        )

    provider_info = None
    if record.provider_id:
        from app.models.provider import Provider
        p = db.query(Provider).filter(Provider.user_id == record.provider_id).first()
        if p:
            provider_info = {
                "provider_id": str(p.user_id),
                "full_name": p.full_name,
                "photo_url": p.photo_url or f"https://api.dicebear.com/7.x/avataaars/svg?seed={p.full_name}",
                "category": p.category,
                "skills": p.skills or "Certified Service Professional",
                "experience_years": p.experience_years or 5,
                "reliability_score": float(p.reliability_score or 99.0),
                "rating": 4.9,
                "is_verified": p.is_verified,
                "service_area": p.service_area or "Bengaluru, India",
            }

    return BookingDetail(
        id=str(record.id),
        booking_reference=record.booking_reference,
        customer_id=str(record.customer_id),
        provider_id=str(record.provider_id) if record.provider_id else None,
        provider_name=record.provider.full_name if record.provider else None,
        provider=provider_info,
        service_id=str(record.service_id),
        service_name=record.get_service_name() if hasattr(record, "get_service_name") else (record.service_name or "Home Service"),
        category=record.get_category() if hasattr(record, "get_category") else (record.category or "General"),
        status=str(record.status.value if hasattr(record.status, "value") else record.status),
        scheduled_date=record.scheduled_date,
        scheduled_time=record.scheduled_time.strftime("%H:%M:%S") if hasattr(record.scheduled_time, "strftime") else str(record.scheduled_time),
        address_line1=record.address_line1,
        landmark=record.landmark,
        city=record.city,
        pincode=record.pincode,
        total_price=float(record.total_price),
        payment_method=record.payment_method or "COD",
        payment_status=record.payment_status or "Pending",
        cancellation_reason=record.cancellation_reason,
        notes=record.notes,
        customer_notes=record.customer_notes or record.notes,
        before_photos=_sanitize_photos(record.before_photos),
        after_photos=_sanitize_photos(record.after_photos),
        warranty={
            "id": str(record.warranty.id),
            "booking_id": str(record.warranty.booking_id),
            "service_name": record.warranty.service_name,
            "issued_at": record.warranty.issued_at.isoformat() if record.warranty.issued_at else None,
            "expires_at": record.warranty.expires_at.isoformat() if record.warranty.expires_at else None,
            "is_active": record.warranty.is_active,
            "claim_status": record.warranty.claim_status,
            "claim_description": record.warranty.claim_description,
            "claim_submitted_at": record.warranty.claim_submitted_at.isoformat() if record.warranty.claim_submitted_at else None,
            "claim_resolved_at": record.warranty.claim_resolved_at.isoformat() if record.warranty.claim_resolved_at else None,
            "claim_notes": record.warranty.claim_notes,
            "days_remaining": max(0, (record.warranty.expires_at.date() - datetime.utcnow().date()).days) if record.warranty.expires_at else 0,
        } if record.warranty else None,
        otp_code=record.completion_otp if str(record.status).lower() == 'started' else (record.start_otp or record.otp_code),
        start_otp=record.start_otp,
        completion_otp=record.completion_otp,
        emergency_flag=record.emergency_flag,
        timeline=safe_timeline(record.timeline),
        created_at=record.created_at,
    )


# 16a. GET /customer/bookings/{id}/warranty
@router.get("/bookings/{booking_id}/warranty", response_model=WarrantyCardResponse)
def get_booking_warranty(
    booking_id: str,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    booking = (
        db.query(Booking)
        .filter((Booking.id == booking_id) | (Booking.booking_reference == booking_id))
        .first()
    )
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.customer_id != current_customer.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    from app.services.booking.warranty_service import get_warranty_policy, issue_booking_warranty
    policy = get_warranty_policy(booking.category, booking.service_name)

    warranty = db.query(BookingWarranty).filter(BookingWarranty.booking_id == booking.id).first()
    if not warranty and str(booking.status).lower() in ["completed", "paid"] and policy["is_eligible"]:
        warranty = issue_booking_warranty(booking, db)

    if not warranty:
        if not policy["is_eligible"]:
            now_dt = datetime.now(timezone.utc)
            return WarrantyCardResponse(
                id=str(uuid.uuid4()),
                booking_id=str(booking.id),
                customer_id=str(booking.customer_id),
                service_name=booking.service_name or "Service",
                issued_at=now_dt,
                expires_at=now_dt,
                is_active=False,
                claim_status="None",
                days_remaining=0,
                duration_days=0,
                nominal_fee=0.0,
                terms=policy["terms"],
                badge_label=policy["badge_label"],
                is_eligible=False,
            )
        raise HTTPException(status_code=404, detail="No warranty card found for this booking")

    exp_dt = warranty.expires_at.date() if hasattr(warranty.expires_at, "date") else datetime.utcnow().date()
    days_rem = max(0, (exp_dt - datetime.utcnow().date()).days)
    return WarrantyCardResponse(
        id=str(warranty.id),
        booking_id=str(warranty.booking_id),
        customer_id=str(warranty.customer_id),
        provider_id=str(warranty.provider_id) if warranty.provider_id else None,
        service_name=warranty.service_name,
        issued_at=warranty.issued_at,
        expires_at=warranty.expires_at,
        is_active=warranty.is_active,
        claim_status=warranty.claim_status,
        claim_description=warranty.claim_description,
        claim_submitted_at=warranty.claim_submitted_at,
        claim_resolved_at=warranty.claim_resolved_at,
        claim_notes=warranty.claim_notes,
        days_remaining=days_rem,
        duration_days=policy["duration_days"],
        nominal_fee=policy["nominal_fee"],
        terms=policy["terms"],
        badge_label=policy["badge_label"],
        is_eligible=policy["is_eligible"],
    )


# 16a-claim. POST /customer/bookings/{id}/warranty/claim
@router.post("/bookings/{booking_id}/warranty/claim")
def raise_warranty_claim(
    booking_id: str,
    payload: WarrantyClaimPayload,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    booking = (
        db.query(Booking)
        .filter((Booking.id == booking_id) | (Booking.booking_reference == booking_id))
        .first()
    )
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.customer_id != current_customer.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    from app.services.booking.warranty_service import get_warranty_policy, issue_booking_warranty, validate_warranty_claim
    warranty = db.query(BookingWarranty).filter(BookingWarranty.booking_id == booking.id).first()
    if not warranty and str(booking.status).lower() in ["completed", "paid"]:
        warranty = issue_booking_warranty(booking, db)

    is_valid, claim_msg, nominal_fee = validate_warranty_claim(warranty, booking.category, booking.service_name)
    if not is_valid:
        raise HTTPException(status_code=400, detail=claim_msg)

    if warranty.claim_status in ["Pending", "Resolved"]:
        return {
            "success": True,
            "message": f"Warranty claim is already registered (Status: {warranty.claim_status}). Our support team is reviewing it.",
            "claim_status": warranty.claim_status,
            "claim_submitted_at": warranty.claim_submitted_at.isoformat() if hasattr(warranty.claim_submitted_at, "isoformat") else str(warranty.claim_submitted_at),
        }

    sub_time = datetime.now(timezone.utc)
    warranty.claim_status = "Pending"
    warranty.claim_description = payload.description.strip()
    warranty.claim_submitted_at = sub_time

    cur_tl = list(booking.timeline or [])
    cur_tl.append({
        "event": "Warranty Claim Raised",
        "claim_description": warranty.claim_description,
        "nominal_fee": nominal_fee,
        "timestamp": sub_time.isoformat(),
        "actor": current_customer.full_name,
        "role": "customer",
    })
    booking.timeline = cur_tl

    db.add(warranty)
    db.add(booking)
    db.commit()
    db.refresh(warranty)

    return {
        "success": True,
        "message": f"Warranty claim raised successfully. Our quality team will inspect and provide 100% free rework labor under your 7-day warranty.",
        "claim_status": warranty.claim_status,
        "nominal_fee": nominal_fee,
        "claim_submitted_at": warranty.claim_submitted_at.isoformat() if hasattr(warranty.claim_submitted_at, "isoformat") else str(warranty.claim_submitted_at),
    }


# 16-pay. GET /customer/bookings/{id}/payments
@router.get("/bookings/{booking_id}/payments")
def get_customer_booking_payments(
    booking_id: str,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    """Retrieve payment and verification status for customer booking."""
    from app.models.payment import BookingPayment

    record = (
        db.query(Booking)
        .filter((Booking.id == booking_id) | (Booking.booking_reference == booking_id))
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="Booking not found")

    if record.customer_id != current_customer.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You cannot access payment records for bookings belonging to another customer",
        )

    payments = (
        db.query(BookingPayment)
        .filter(BookingPayment.booking_id == record.id)
        .order_by(BookingPayment.created_at.desc())
        .all()
    )
    return [
        {
            "id": str(p.id),
            "booking_id": str(p.booking_id),
            "booking_reference": record.booking_reference,
            "payment_method": p.payment_method or "COD",
            "agreed_amount": float(p.agreed_amount or 0.0),
            "reported_amount": float(p.reported_amount) if p.reported_amount is not None else None,
            "status": p.status,
            "discrepancy_flag": bool(p.discrepancy_flag),
            "collected_at": p.collected_at.isoformat() if p.collected_at else None,
            "reviewed_at": p.reviewed_at.isoformat() if p.reviewed_at else None,
            "created_at": p.created_at.isoformat() if p.created_at else "",
        }
        for p in payments
    ]


# 16b. GET /customer/bookings/{id}/location
@router.get("/bookings/{booking_id}/location")
def get_booking_location(
    booking_id: str,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    from app.models.provider import Provider, ProviderLocation

    record = (
        db.query(Booking)
        .filter((Booking.id == booking_id) | (Booking.booking_reference == booking_id))
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="Booking not found")

    if record.customer_id != current_customer.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You cannot access location for bookings belonging to another customer",
        )

    provider_info = None
    if record.provider_id:
        provider = db.query(Provider).filter(Provider.user_id == record.provider_id).first()
        if provider:
            provider_info = {
                "provider_id": str(provider.user_id),
                "full_name": provider.full_name,
                "photo_url": provider.photo_url or f"https://api.dicebear.com/7.x/avataaars/svg?seed={provider.full_name}",
                "category": provider.category,
                "skills": provider.skills,
                "experience_years": provider.experience_years,
                "reliability_score": float(provider.reliability_score or 100.0),
                "rating": 4.9,
                "is_verified": provider.is_verified,
                "service_area": provider.service_area or "Delhi NCR",
            }

    loc = None
    active_tracking_statuses = ["Accepted", "On The Way", "Arrived", "Started"]
    if record.provider_id and record.status in active_tracking_statuses:
        loc = db.query(ProviderLocation).filter(
            ProviderLocation.provider_id == record.provider_id,
            ProviderLocation.is_active == True,
        ).first()

    provider_loc_data = None
    if loc:
        provider_loc_data = {
            "latitude": float(loc.latitude),
            "longitude": float(loc.longitude),
            "heading": float(loc.heading) if loc.heading is not None else None,
            "speed": float(loc.speed) if loc.speed is not None else None,
            "accuracy": float(loc.accuracy) if loc.accuracy is not None else None,
            "updated_at": loc.updated_at.isoformat() if loc.updated_at else None,
        }

    c_lat = 28.6280
    c_lng = 77.3649
    if record.timeline:
        for item in reversed(record.timeline):
            if isinstance(item, dict) and item.get("event") == "Customer Coordinates Updated":
                if item.get("latitude") is not None and item.get("longitude") is not None:
                    c_lat = float(item["latitude"])
                    c_lng = float(item["longitude"])
                    break

    customer_loc = {
        "latitude": c_lat,
        "longitude": c_lng,
        "address": record.address_line1 or record.address or "Sector 62, Noida",
        "city": record.city or "Noida",
    }

    return {
        "booking_id": str(record.id),
        "booking_reference": record.booking_reference,
        "status": str(record.status.value if hasattr(record.status, "value") else record.status),
        "provider": provider_info,
        "provider_location": provider_loc_data,
        "customer_location": customer_loc,
        "service_name": record.service_name,
        "scheduled_date": record.scheduled_date,
        "scheduled_time": record.scheduled_time.strftime("%H:%M:%S") if hasattr(record.scheduled_time, "strftime") else str(record.scheduled_time),
    }


class CustomerCoordinatesPayload(BaseModel):
    latitude: float
    longitude: float


# 16c. PATCH /customer/bookings/{id}/location
@router.patch("/bookings/{booking_id}/location")
def update_customer_booking_location(
    booking_id: str,
    payload: CustomerCoordinatesPayload,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    if not (-90.0 <= payload.latitude <= 90.0 and -180.0 <= payload.longitude <= 180.0):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid GPS coordinates: latitude must be in [-90, 90] and longitude in [-180, 180]."
        )

    record = (
        db.query(Booking)
        .filter((Booking.id == booking_id) | (Booking.booking_reference == booking_id))
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="Booking not found")

    if record.customer_id != current_customer.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You cannot access location for bookings belonging to another customer",
        )

    tl = list(record.timeline or [])
    found = False
    for item in tl:
        if isinstance(item, dict) and item.get("event") == "Customer Coordinates Updated":
            item["latitude"] = float(payload.latitude)
            item["longitude"] = float(payload.longitude)
            item["updated_at"] = datetime.utcnow().isoformat()
            found = True
            break
    if not found:
        tl.append({
            "event": "Customer Coordinates Updated",
            "latitude": float(payload.latitude),
            "longitude": float(payload.longitude),
            "updated_at": datetime.utcnow().isoformat(),
        })
    record.timeline = tl
    db.add(record)
    db.commit()

    return {
        "status": "success",
        "booking_id": str(record.id),
        "customer_location": {
            "latitude": float(payload.latitude),
            "longitude": float(payload.longitude),
            "address": record.address_line1 or record.address or "Service Location",
            "city": record.city or "Noida",
        }
    }


# 17. POST /customer/bookings/{id}/cancel
@router.post("/bookings/{booking_id}/cancel", response_model=BookingDetail)
def cancel_booking(
    booking_id: str,
    payload: CancelBookingPayload,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    effective_reason = payload.reason or payload.cancellation_reason or "Cancelled by Customer"
    record = (
        db.query(Booking)
        .filter((Booking.id == booking_id) | (Booking.booking_reference == booking_id))
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="Booking not found")

    if record.customer_id != current_customer.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You cannot cancel a booking belonging to another customer",
        )

    curr_status = str(record.status.value if hasattr(record.status, "value") else record.status).upper()
    if curr_status in ["COMPLETED", "PAID", "CANCELLED", "REJECTED"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel booking with current status '{record.status}'."
        )

    record.status = "CANCELLED"
    record.cancellation_reason = effective_reason
    db.commit()
    db.refresh(record)

    # Automated Notification Trigger: Booking Cancelled
    try:
        from app.services.notification import notify_booking_event
        notify_booking_event(db, record, "booking.cancelled", extra_context={"notes": effective_reason})
    except Exception as exc:
        pass
    
    sched_time_str = (
        record.scheduled_time.strftime("%H:%M:%S")
        if hasattr(record.scheduled_time, "strftime")
        else str(record.scheduled_time)
    )
    
    return BookingDetail(
        id=str(record.id),
        booking_reference=record.booking_reference,
        customer_id=str(record.customer_id),
        provider_id=str(record.provider_id) if record.provider_id else None,
        provider_name=record.provider.full_name if record.provider else None,
        service_id=str(record.service_id),
        service_name=record.get_service_name() if hasattr(record, "get_service_name") else (record.service_name or "Home Service"),
        category=record.get_category() if hasattr(record, "get_category") else (record.category or "General"),
        status=str(record.status.value if hasattr(record.status, "value") else record.status),
        scheduled_date=record.scheduled_date,
        scheduled_time=sched_time_str,
        address_line1=record.address_line1,
        landmark=record.landmark,
        city=record.city,
        pincode=record.pincode,
        total_price=float(record.total_price),
        payment_method=record.payment_method,
        cancellation_reason=effective_reason,
        notes=record.notes,
        otp_code=record.otp_code,
        emergency_flag=record.emergency_flag,
        timeline=record.timeline,
        created_at=record.created_at,
    )


# 18. POST /customer/bookings/{id}/feedback
@router.post("/bookings/{booking_id}/feedback")
def submit_booking_feedback(
    booking_id: str,
    payload: BookingFeedbackPayload,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    record = (
        db.query(Booking)
        .filter((Booking.id == booking_id) | (Booking.booking_reference == booking_id))
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="Booking not found")

    if record.customer_id != current_customer.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You cannot submit feedback for a booking belonging to another customer",
        )

    b_status = str(record.status.value if hasattr(record.status, "value") else record.status).upper()
    if b_status != "COMPLETED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot submit feedback for booking in '{b_status}' status. Service must be Completed.",
        )

    fb = BookingFeedback(
        id=uuid.uuid4(),
        booking_id=record.id,
        customer_id=current_customer.id,
        rating=payload.rating,
        review_text=payload.review_text,
        created_at=datetime.utcnow(),
    )
    try:
        db.add(fb)
        db.commit()
    except Exception:
        db.rollback()

    return {"status": "ok", "message": "Feedback submitted successfully"}


# 19. GET /customer/support/tickets
@router.get("/support/tickets", response_model=List[SupportTicketDetail])
def get_customer_support_tickets(
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    records = db.query(SupportTicket).filter(SupportTicket.customer_id == current_customer.id).all()
    if not records:
        return []

    return [

        SupportTicketDetail(
            id=str(t.id),
            customer_id=str(t.customer_id),
            booking_id=str(t.booking_id) if t.booking_id else None,
            subject=t.subject,
            category=t.category,
            priority=t.priority,
            status=t.status,
            created_at=t.created_at,
            messages=[
                MessageItem(
                    id=str(m.id),
                    ticket_id=str(m.ticket_id),
                    sender_role=m.sender_role,
                    sender_name=m.sender_name or (
                        "Customer" if m.sender_role.lower() == "customer"
                        else ("Service Provider" if m.sender_role.lower() == "provider" else "SmartServe Support Operations")
                    ),
                    message_text=m.message_text,
                    attachment_url=m.attachment_url,
                    created_at=m.created_at,
                )
                for m in t.messages
            ],
        )
        for t in records
    ]


# 20. POST /customer/support/tickets
@router.post("/support/tickets", response_model=SupportTicketDetail)
def create_support_ticket(
    payload: CreateTicketPayload,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    ticket_id = uuid.uuid4()
    priority = "High" if payload.category in ["Booking issue", "Service quality"] else (payload.priority or "Normal")

    b_uuid = None
    b_prov_id = None
    if payload.booking_id:
        try:
            b_uuid = uuid.UUID(payload.booking_id)
            bk = db.query(Booking).filter(Booking.id == b_uuid).first()
            if bk:
                b_prov_id = bk.provider_id
        except Exception:
            pass

    new_ticket = SupportTicket(
        id=ticket_id,
        customer_id=current_customer.id,
        provider_id=b_prov_id,
        booking_id=b_uuid,
        subject=payload.subject,
        description=payload.description,
        category=payload.category,
        priority=priority,
        status="OPEN",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    first_message = TicketMessage(
        id=uuid.uuid4(),
        ticket_id=ticket_id,
        sender_id=current_customer.user_id,
        sender_role="customer",
        sender_name=current_customer.full_name,
        message_text=payload.description,
        created_at=datetime.utcnow(),
    )
    db.add(new_ticket)
    db.add(first_message)
    db.commit()
    db.refresh(new_ticket)

    return SupportTicketDetail(
        id=str(new_ticket.id),
        customer_id=str(new_ticket.customer_id),
        booking_id=str(new_ticket.booking_id) if new_ticket.booking_id else None,
        subject=new_ticket.subject,
        description=new_ticket.description,
        category=new_ticket.category,
        priority=new_ticket.priority,
        status=new_ticket.status,
        created_at=new_ticket.created_at,
        messages=[
            MessageItem(
                id=str(first_message.id),
                ticket_id=str(first_message.ticket_id),
                sender_role=first_message.sender_role,
                sender_name=first_message.sender_name,
                message_text=first_message.message_text,
                attachment_url=first_message.attachment_url,
                created_at=first_message.created_at,
            )
        ],
    )


# 21. GET /customer/support/tickets/{id}
@router.get("/support/tickets/{ticket_id}", response_model=SupportTicketDetail)
def get_support_ticket_by_id(
    ticket_id: str,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    try:
        t_uuid = uuid.UUID(ticket_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ticket ID format")

    t = db.query(SupportTicket).filter(SupportTicket.id == t_uuid, SupportTicket.customer_id == current_customer.id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Support ticket not found")

    return SupportTicketDetail(
        id=str(t.id),
        customer_id=str(t.customer_id),
        booking_id=str(t.booking_id) if t.booking_id else None,
        subject=t.subject,
        description=t.description,
        category=t.category,
        priority=t.priority,
        status=t.status,
        created_at=t.created_at,
        messages=[
            MessageItem(
                id=str(m.id),
                ticket_id=str(m.ticket_id),
                sender_role=m.sender_role,
                sender_name=m.sender_name or (
                    "Customer" if m.sender_role.lower() == "customer"
                    else ("Service Provider" if m.sender_role.lower() == "provider" else "SmartServe Support Operations")
                ),
                message_text=m.message_text,
                attachment_url=m.attachment_url,
                created_at=m.created_at,
            )
            for m in (t.messages or [])
        ],
    )


# 22. POST /customer/support/tickets/{id}/messages
@router.post("/support/tickets/{ticket_id}/messages", response_model=MessageItem)
def add_ticket_message(
    ticket_id: str,
    payload: TicketMessagePayload,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    try:
        t_uuid = uuid.UUID(ticket_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ticket ID format")

    ticket = db.query(SupportTicket).filter(
        SupportTicket.id == t_uuid,
        SupportTicket.customer_id == current_customer.id
    ).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Support ticket not found")

    new_msg = TicketMessage(
        id=uuid.uuid4(),
        ticket_id=t_uuid,
        sender_id=current_customer.user_id,
        sender_role="customer",
        sender_name=current_customer.full_name,
        message_text=payload.message_text,
        attachment_url=payload.attachment_url,
        created_at=datetime.utcnow(),
    )
    db.add(new_msg)
    ticket.updated_at = datetime.utcnow()
    if ticket.status and ticket.status.lower() in ["resolved", "closed"]:
        ticket.status = "Open"
    db.commit()
    db.refresh(new_msg)

    try:
        from app.services.kafka import kafka_producer, KafkaTopics, KafkaEvent
        msg_event = KafkaEvent(
            event_type=KafkaTopics.SUPPORT_MESSAGE,
            ticket_id=str(ticket.id),
            booking_id=str(ticket.booking_id) if ticket.booking_id else None,
            sender_id=str(current_customer.user_id),
            receiver_id=str(ticket.provider_id) if ticket.provider_id else None,
            payload={
                "ticket_id": str(ticket.id),
                "message_id": str(new_msg.id),
                "booking_id": str(ticket.booking_id) if ticket.booking_id else None,
                "sender_id": str(current_customer.user_id),
                "sender_role": "customer",
                "sender_name": current_customer.full_name,
                "receiver_id": str(ticket.provider_id) if ticket.provider_id else None,
                "message_text": new_msg.message_text,
                "attachment_url": new_msg.attachment_url,
                "category": getattr(ticket, "category", "General"),
                "created_at": new_msg.created_at.isoformat() if hasattr(new_msg.created_at, "isoformat") else str(new_msg.created_at),
            }
        )
        kafka_producer.publish_event(KafkaTopics.SUPPORT_MESSAGE, msg_event)
    except Exception as exc:
        print(f"[Customer Ticket Msg Kafka Publish Error] {exc}")

    return MessageItem(
        id=str(new_msg.id),
        ticket_id=str(ticket.id),
        sender_role=new_msg.sender_role,
        sender_name=new_msg.sender_name,
        message_text=new_msg.message_text,
        attachment_url=new_msg.attachment_url,
        created_at=new_msg.created_at,
    )


# 23. GET /customer/feedback
@router.get("/feedback")
def get_customer_feedbacks(current_customer: Customer = Depends(get_current_customer), db: Session = Depends(get_db)):
    fbs = db.query(BookingFeedback).filter(BookingFeedback.customer_id == current_customer.id).all()
    return [
        {
            "id": str(f.id),
            "booking_id": str(f.booking_id),
            "rating": f.rating,
            "review_text": f.review_text,
            "created_at": f.created_at,
        }
        for f in fbs
    ]


# 24. GET /customer/sessions
@router.get("/sessions", response_model=List[SessionListItem])
def get_customer_sessions(current_customer: Customer = Depends(get_current_customer)):
    return [
        SessionListItem(
            id="sess-1",
            device_info="Chrome on Windows 11",
            ip_address="127.0.0.1",
            last_active=datetime.utcnow(),
            is_current=True,
        )
    ]


# 25. POST /customer/sessions/{id}/revoke
@router.post("/sessions/{session_id}/revoke")
def revoke_session(
    session_id: str,
    current_customer: Customer = Depends(get_current_customer),
):
    return {"status": "ok", "message": f"Session {session_id} revoked"}


# 26. POST /customer/sessions/revoke-all
@router.post("/sessions/revoke-all")
def revoke_all_sessions(
    current_customer: Customer = Depends(get_current_customer),
):
    return {"status": "ok", "message": "All other sessions revoked"}


# 27. GET /customer/recommendations
@router.get("/recommendations", response_model=List[ServiceItem])
def get_recommendations(db: Session = Depends(get_db)):
    from app.models.service import Service
    db_services = db.query(Service).filter(Service.is_active == True).limit(4).all()
    return [parse_service_details(s) for s in db_services]


# 28. POST /customer/uploads/image
@router.post("/uploads/image")
async def upload_image(
    file: UploadFile = File(...),
    current_customer: Customer = Depends(get_current_customer),
):
    """
    Secure customer image upload:
    - Enforces authentication
    - Validates file extensions (JPEG, PNG, WebP)
    - Validates MIME type and magic bytes
    - Enforces 5MB maximum file size
    - Sanitizes filename with UUID (prevents path traversal)
    """
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
    ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}

    orig_ext = os.path.splitext(file.filename or "")[1].lower()
    if orig_ext not in ALLOWED_EXTENSIONS or file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only JPEG, PNG, and WebP images are allowed."
        )

    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds maximum limit of 5MB."
        )

    # Magic header byte verification
    is_jpeg = content.startswith(b"\xff\xd8\xff")
    is_png = content.startswith(b"\x89PNG\r\n\x1a\n")
    is_webp = content.startswith(b"RIFF") and b"WEBP" in content[:16]

    if not (is_jpeg or is_png or is_webp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File content does not match genuine image structure."
        )

    # 3. Antivirus and Malware Scanning
    from app.services.malware_scanner import validate_upload_safety
    validate_upload_safety(content, file.filename or "customer_upload")

    os.makedirs("customer_uploads", exist_ok=True)
    safe_filename = f"{uuid.uuid4().hex}{orig_ext}"
    filepath = os.path.join("customer_uploads", safe_filename)
    with open(filepath, "wb") as f:
        f.write(content)

    return {"url": f"/static/uploads/{safe_filename}"}


# ==========================================
# BOOKING CHAT (Customer ↔ Provider)
# ==========================================

# 29. GET /customer/bookings/{booking_id}/chat
@router.get("/bookings/{booking_id}/chat", response_model=SupportTicketDetail)
def get_booking_chat(
    booking_id: str,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    """Get or create the Customer ↔ Provider chat thread for a specific booking."""
    try:
        b_uuid = uuid.UUID(booking_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid booking ID format")

    booking = db.query(Booking).filter(Booking.id == b_uuid).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.customer_id != current_customer.id:
        raise HTTPException(status_code=403, detail="Forbidden: You cannot access another customer's booking chat")
    if not booking.provider_id:
        raise HTTPException(status_code=400, detail="No provider assigned to this booking yet")

    # Find existing booking chat ticket (customer_id + provider_id + booking_id all set)
    ticket = db.query(SupportTicket).filter(
        SupportTicket.booking_id == b_uuid,
        SupportTicket.customer_id == current_customer.id,
        SupportTicket.provider_id == booking.provider_id,
    ).first()

    if not ticket:
        # Create a new booking chat ticket
        provider_name = booking.provider.full_name if booking.provider else "Your Provider"
        ticket = SupportTicket(
            id=uuid.uuid4(),
            customer_id=current_customer.id,
            provider_id=booking.provider_id,
            booking_id=b_uuid,
            subject=f"Chat: {booking.service_name} (Booking {booking.booking_reference})",
            description=f"Booking chat thread between customer and provider for {booking.service_name}.",
            category="Booking Chat",
            priority="Normal",
            status="Open",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(ticket)
        db.commit()
        db.refresh(ticket)

    return SupportTicketDetail(
        id=str(ticket.id),
        customer_id=str(ticket.customer_id),
        booking_id=str(ticket.booking_id) if ticket.booking_id else None,
        subject=ticket.subject,
        description=ticket.description,
        category=ticket.category,
        priority=ticket.priority,
        status=ticket.status,
        created_at=ticket.created_at,
        messages=[
            MessageItem(
                id=str(m.id),
                ticket_id=str(m.ticket_id),
                sender_role=m.sender_role,
                sender_name=m.sender_name or m.sender_role.title(),
                message_text=m.message_text,
                attachment_url=m.attachment_url,
                created_at=m.created_at,
            )
            for m in sorted(ticket.messages or [], key=lambda x: x.created_at)
        ],
    )


# 30. POST /customer/bookings/{booking_id}/chat/messages
@router.post("/bookings/{booking_id}/chat/messages", response_model=MessageItem)
def send_booking_chat_message(
    booking_id: str,
    payload: TicketMessagePayload,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    """Customer sends a message in the Provider ↔ Customer booking chat."""
    try:
        b_uuid = uuid.UUID(booking_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid booking ID format")

    booking = db.query(Booking).filter(Booking.id == b_uuid).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.customer_id != current_customer.id:
        raise HTTPException(status_code=403, detail="Forbidden: You cannot access another customer's booking chat")
    if not booking.provider_id:
        raise HTTPException(status_code=400, detail="No provider assigned to this booking yet")

    # Get or create ticket
    ticket = db.query(SupportTicket).filter(
        SupportTicket.booking_id == b_uuid,
        SupportTicket.customer_id == current_customer.id,
        SupportTicket.provider_id == booking.provider_id,
    ).first()

    if not ticket:
        ticket = SupportTicket(
            id=uuid.uuid4(),
            customer_id=current_customer.id,
            provider_id=booking.provider_id,
            booking_id=b_uuid,
            subject=f"Chat: {booking.service_name} (Booking {booking.booking_reference})",
            description=f"Booking chat thread between customer and provider for {booking.service_name}.",
            category="Booking Chat",
            priority="Normal",
            status="Open",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(ticket)
        db.flush()

    new_msg = TicketMessage(
        id=uuid.uuid4(),
        ticket_id=ticket.id,
        sender_id=current_customer.user_id,
        sender_role="customer",
        sender_name=current_customer.full_name,
        message_text=payload.message_text,
        attachment_url=payload.attachment_url,
        created_at=datetime.utcnow(),
    )
    db.add(new_msg)
    ticket.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(new_msg)

    try:
        from app.services.kafka import kafka_producer, KafkaTopics, KafkaEvent
        chat_event = KafkaEvent(
            event_type=KafkaTopics.SUPPORT_MESSAGE,
            ticket_id=str(ticket.id),
            booking_id=str(booking.id),
            sender_id=str(current_customer.user_id),
            receiver_id=str(booking.provider_id) if booking.provider_id else None,
            payload={
                "ticket_id": str(ticket.id),
                "booking_id": str(booking.id),
                "message_id": str(new_msg.id),
                "sender_id": str(current_customer.user_id),
                "sender_role": "customer",
                "sender_name": current_customer.full_name,
                "receiver_id": str(booking.provider_id) if booking.provider_id else None,
                "message_text": new_msg.message_text,
                "attachment_url": new_msg.attachment_url,
                "category": "Booking Chat",
                "created_at": new_msg.created_at.isoformat() if hasattr(new_msg.created_at, "isoformat") else str(new_msg.created_at),
            }
        )
        kafka_producer.publish_event(KafkaTopics.SUPPORT_MESSAGE, chat_event)
    except Exception as exc:
        print(f"[Customer Chat Msg Kafka Publish Error] {exc}")

    return MessageItem(
        id=str(new_msg.id),
        ticket_id=str(ticket.id),
        sender_role=new_msg.sender_role,
        sender_name=new_msg.sender_name,
        message_text=new_msg.message_text,
        attachment_url=new_msg.attachment_url,
        created_at=new_msg.created_at,
    )


# -------------------------------------------------------------------------
# 18. POST /customer/bookings/{id}/reschedule
# -------------------------------------------------------------------------
from app.schemas.notification import RescheduleBookingPayload, CustomerNotificationItem
from app.models.notification import NotificationLog


@router.post("/bookings/{booking_id}/reschedule", response_model=BookingDetail)
def reschedule_booking(
    booking_id: str,
    payload: RescheduleBookingPayload,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    """
    Allow customer to reschedule an active booking before service execution starts.
    Validates upcoming date and slot availability, updates scheduled datetime,
    and triggers automated booking.rescheduled notifications.
    """
    from datetime import date
    from app.services.booking.eligibility_service import parse_scheduled_datetime, find_eligible_provider

    record = (
        db.query(Booking)
        .filter((Booking.id == booking_id) | (Booking.booking_reference == booking_id))
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="Booking not found")

    if record.customer_id != current_customer.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You cannot reschedule a booking belonging to another customer",
        )

    curr_st = str(record.status.value if hasattr(record.status, "value") else record.status).upper()
    if curr_st in ["STARTED", "COMPLETED", "PAID", "CANCELLED", "REJECTED"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot reschedule booking with current status '{record.status}'. Only pending or accepted bookings may be rescheduled.",
        )

    new_sched_dt = parse_scheduled_datetime(payload.new_date, payload.new_time)
    if new_sched_dt.date() < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot reschedule to a past date. Please select an upcoming date and time.",
        )

    # Validate provider availability on the new slot
    eligible_prov, matched_slot, msg = find_eligible_provider(
        db, record.service_id, new_sched_dt, requested_provider_id=record.provider_id
    )
    if not eligible_prov:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to reschedule: {msg}. Please pick another open date or time.",
        )

    prev_date = record.scheduled_date
    prev_time = (
        record.scheduled_time.strftime("%I:%M %p")
        if record.scheduled_time and hasattr(record.scheduled_time, "strftime")
        else str(record.scheduled_time)
    )

    record.scheduled_date = payload.new_date
    record.scheduled_time = new_sched_dt

    tl_event = {
        "event": "Booking Rescheduled by Customer",
        "actor": current_customer.full_name,
        "previous_schedule": f"{prev_date} at {prev_time}",
        "new_schedule": f"{payload.new_date} at {payload.new_time}",
        "reason": payload.reason or "Customer requested reschedule",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    cur_tl = list(record.timeline or [])
    cur_tl.append(tl_event)
    record.timeline = cur_tl

    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(record, "timeline")

    db.commit()
    db.refresh(record)

    # Trigger Automated Notification: booking.rescheduled
    try:
        from app.services.notification import notify_booking_event
        notify_booking_event(
            db,
            record,
            "booking.rescheduled",
            extra_context={
                "notes": f"Rescheduled from {prev_date} {prev_time} to {payload.new_date} {payload.new_time}. {payload.reason or ''}".strip()
            },
        )
    except Exception as exc:
        pass

    sched_time_str = (
        record.scheduled_time.strftime("%H:%M:%S")
        if hasattr(record.scheduled_time, "strftime")
        else str(record.scheduled_time)
    )
    return BookingDetail(
        id=str(record.id),
        booking_reference=record.booking_reference,
        customer_id=str(record.customer_id),
        provider_id=str(record.provider_id) if record.provider_id else None,
        provider_name=record.provider.full_name if record.provider else None,
        service_id=str(record.service_id),
        service_name=record.get_service_name() if hasattr(record, "get_service_name") else (record.service_name or "Home Service"),
        category=record.get_category() if hasattr(record, "get_category") else (record.category or "General"),
        status=str(record.status.value if hasattr(record.status, "value") else record.status),
        scheduled_date=record.scheduled_date,
        scheduled_time=sched_time_str,
        address_line1=record.address_line1,
        landmark=record.landmark,
        city=record.city,
        pincode=record.pincode,
        total_price=float(record.total_price),
        timeline=record.timeline or [],
        created_at=record.created_at,
    )


# -------------------------------------------------------------------------
# 19. GET /customer/bookings/{id}/notifications
# -------------------------------------------------------------------------
@router.get("/bookings/{booking_id}/notifications", response_model=List[CustomerNotificationItem])
def get_customer_booking_notifications(
    booking_id: str,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    """
    Retrieve notification audit history for a booking owned by the authenticated customer.
    Enforces strict customer ownership isolation.
    """
    record = (
        db.query(Booking)
        .filter((Booking.id == booking_id) | (Booking.booking_reference == booking_id))
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="Booking not found")

    if record.customer_id != current_customer.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You cannot access notifications for another customer's booking",
        )

    logs = (
        db.query(NotificationLog)
        .filter(NotificationLog.booking_id == record.id)
        .order_by(NotificationLog.created_at.desc())
        .all()
    )

    results = []
    for l in logs:
        # Mask phone number slightly if present for customer privacy (e.g. +91 98*** 00001)
        rec = l.recipient
        if rec and "@" not in rec and len(rec) >= 8:
            rec = rec[:4] + "***" + rec[-3:]
        results.append(
            CustomerNotificationItem(
                id=l.id,
                booking_reference=l.booking_reference,
                event_type=l.event_type,
                channel=l.channel,
                recipient=rec,
                delivery_status=l.delivery_status,
                last_attempt_at=l.last_attempt_at,
                created_at=l.created_at,
            )
        )
    return results

