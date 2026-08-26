from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password, create_access_token, hash_password
from app.core.dependencies import get_current_user, require_admin
from app.repositories.db import get_db
from app.repositories import user_repository, audit_repository
from app.schemas.admin_auth import AdminLoginRequest, TokenResponse, SessionResponse
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Admin Auth"])

@router.post("/login", response_model=TokenResponse)
def admin_login(
    req: AdminLoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Authenticate Admin user and issue JWT access token with role claims."""
    client_ip = request.client.host if request.client else "127.0.0.1"
    clean_email = req.email.strip().lower()
    clean_password = req.password.strip()
    user = user_repository.get_user_by_email(db, clean_email)

    if not user or user.role != "admin":
        audit_repository.record_failed_login(db, clean_email, client_ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(clean_password, user.password_hash):
        audit_repository.record_failed_login(db, clean_email, client_ip)
        audit_repository.create_audit_log(
            db, actor_email=req.email, actor_role="unknown",
            action="Admin Login Failed", risk_level="Warning", ip_address=client_ip
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin account is suspended",
        )

    # Generate JWT
    token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role},
        expires_delta=token_expires
    )

    # Track Active Session
    import uuid
    from app.services import security_service
    user_agent = request.headers.get("user-agent", "Admin Console / Chrome")
    security_service.create_active_session(
        db, user_id=user.id, token_jti=f"jwt_{uuid.uuid4().hex[:12]}",
        ip_address=client_ip, user_agent=user_agent
    )

    # Audit log
    audit_repository.create_audit_log(
        db, actor_id=user.id, actor_email=user.email, actor_role=user.role,
        action="Admin Login Success", risk_level="Info", ip_address=client_ip
    )

    from app.models.security import AdminRole
    role_entry = db.query(AdminRole).filter(AdminRole.user_id == user.id).first()
    r_name = role_entry.role_name if role_entry else ("super_admin" if user.role == "super_admin" else "operations_admin")
    if r_name == "super_admin" or user.role == "super_admin":
        perms = ['dashboard:view', 'catalog:manage', 'providers:manage', 'customers:manage', 'admins:manage', 'bookings:manage', 'insights:view', 'support:manage', 'security:manage', 'emails:manage', 'settings:manage']
    else:
        perms = role_entry.permissions if role_entry else ['dashboard:view', 'catalog:manage']

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        user_id=str(user.id),
        email=user.email,
        role=user.role,
        role_name=r_name,
        permissions=perms
    )

from pydantic import BaseModel

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

@router.get("/me", response_model=SessionResponse)
def get_admin_session(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Return active admin session details with dynamic role & permissions."""
    from app.models.security import AdminRole
    role_entry = db.query(AdminRole).filter(AdminRole.user_id == current_user.id).first()
    r_name = role_entry.role_name if role_entry else ("super_admin" if current_user.role == "super_admin" else "operations_admin")
    if r_name == "super_admin" or current_user.role == "super_admin":
        perms = ['dashboard:view', 'catalog:manage', 'providers:manage', 'customers:manage', 'admins:manage', 'bookings:manage', 'insights:view', 'support:manage', 'security:manage', 'emails:manage', 'settings:manage']
    else:
        perms = role_entry.permissions if role_entry else ['dashboard:view', 'catalog:manage']

    return SessionResponse(
        user_id=str(current_user.id),
        email=current_user.email,
        role=current_user.role,
        role_name=r_name,
        permissions=perms,
        is_active=current_user.is_active
    )

@router.post("/change-password")
def change_admin_password(
    req: PasswordChangeRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Safely update authenticated admin password."""
    if not verify_password(req.current_password, admin.password_hash):
        raise HTTPException(status_code=400, detail="Current password verification failed.")

    if req.new_password != req.confirm_password:
        raise HTTPException(status_code=400, detail="New password and confirmation do not match.")

    if len(req.new_password) < 8:
        raise HTTPException(status_code=400, detail="New password must be at least 8 characters.")

    admin.password_hash = hash_password(req.new_password)
    db.commit()

    audit_repository.create_audit_log(
        db, actor_id=admin.id, actor_email=admin.email, actor_role=admin.role,
        action="Changed Account Password", risk_level="Info"
    )

    return {"status": "success", "message": "Password updated successfully."}
