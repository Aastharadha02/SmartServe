import uuid
from typing import Optional, Generator
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.security import decode_access_token
from app.models.customer import Customer
from app.models.user import User

security_scheme = HTTPBearer(auto_error=False)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class AuthUser(BaseModel):
    id: uuid.UUID
    email: str
    role: str
    full_name: str
    is_verified: bool = True
    is_active: bool = True


def get_current_user(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> AuthUser:
    """
    Extracts Bearer token, decodes and verifies JWT, checks revocation against ActiveSession,
    and validates against authoritative database record.
    """
    if not auth or not auth.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated: Bearer token required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Token Revocation Check (JTI session invalidation)
    jti = payload.get("jti")
    if jti:
        try:
            from app.models.session import ActiveSession
            revoked_session = (
                db.query(ActiveSession)
                .filter(ActiveSession.token_jti == jti, ActiveSession.is_revoked == True)
                .first()
            )
            if revoked_session:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has been revoked or logged out",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except HTTPException:
            raise
        except Exception:
            pass

    if payload.get("pending_profile") is True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Profile onboarding incomplete. Please complete your profile to continue.",
        )

    sub = payload.get("sub")
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload: missing subject",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Support lookup by UUID ID or Email identifier for robust integration
    user = None
    try:
        user_id = uuid.UUID(str(sub))
        user = db.query(User).filter(User.id == user_id).first()
    except (ValueError, TypeError):
        user = db.query(User).filter(User.email == str(sub).strip().lower()).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found in system",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive or suspended",
        )

    # Authoritative DB role enforcement: never trust client-altered or stale role claim
    role = user.role
    full_name = payload.get("full_name") or user.email

    if user.role == "provider":
        from app.models.provider import Provider
        prov = db.query(Provider).filter(Provider.user_id == user.id).first()
        if prov and prov.full_name:
            full_name = prov.full_name
    elif user.role == "customer":
        cust = db.query(Customer).filter(Customer.user_id == user.id).first()
        if cust and cust.full_name:
            full_name = cust.full_name

    return AuthUser(
        id=user.id,
        email=user.email,
        role=role,
        full_name=full_name,
        is_verified=True,
        is_active=user.is_active,
    )


def require_provider(
    current_user: AuthUser = Depends(get_current_user),
) -> AuthUser:
    """Role-based access guard: Ensures caller has Provider role."""
    if current_user.role != "provider":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Provider role required",
        )
    return current_user


def require_admin(
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Guard ensuring caller has Admin or Super Admin role."""
    if current_user.role not in ["admin", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Admin role required",
        )
    admin_user = (
        db.query(User)
        .filter(User.id == current_user.id, User.role.in_(["admin", "super_admin"]))
        .first()
    )
    if not admin_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Admin account not found",
        )
    return admin_user


def require_permission(perm: str):
    """Guard checking specific granular admin permission."""
    def permission_guard(
        admin_user: User = Depends(require_admin),
        db: Session = Depends(get_db),
    ) -> User:
        if admin_user.role == "super_admin":
            return admin_user

        from app.models.security import AdminRole
        role_entry = (
            db.query(AdminRole)
            .filter(AdminRole.user_id == admin_user.id, AdminRole.is_active == True)
            .first()
        )
        if role_entry:
            perms_set = set(role_entry.permissions or [])

            if "*" in perms_set or perm in perms_set:
                return admin_user
            if ":" in perm:
                domain, _ = perm.split(":", 1)
                if f"{domain}:manage" in perms_set or f"{domain}:*" in perms_set:
                    return admin_user
        elif admin_user.role == "admin" and perm in ["dashboard:view"]:
            return admin_user


        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access forbidden: Permission '{perm}' required",
        )
    return permission_guard


def get_current_customer(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> Customer:
    """
    Authenticates and retrieves the current Customer entity from JWT token.
    Enforces token validity, non-revocation, active state, and customer role.
    """
    if not auth or not auth.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated: Bearer token required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Token Revocation Check
    jti = payload.get("jti")
    if jti:
        try:
            from app.models.session import ActiveSession
            revoked_session = (
                db.query(ActiveSession)
                .filter(ActiveSession.token_jti == jti, ActiveSession.is_revoked == True)
                .first()
            )
            if revoked_session:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has been revoked or logged out",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except HTTPException:
            raise
        except Exception:
            pass

    if payload.get("pending_profile") is True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Profile onboarding incomplete. Please complete your profile to continue.",
        )

    sub = payload.get("sub")
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload: missing subject",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = None
    try:
        user_id = uuid.UUID(str(sub))
        user = db.query(User).filter(User.id == user_id).first()
    except (ValueError, TypeError):
        user = db.query(User).filter(User.email == str(sub).strip().lower()).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found in system",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive or suspended",
        )

    if user.role != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Customer role required",
        )

    customer = (
        db.query(Customer)
        .filter((Customer.user_id == user.id) | (Customer.id == user.id))
        .first()
    )
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer profile not found",
        )

    return customer
