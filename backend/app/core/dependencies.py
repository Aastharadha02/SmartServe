import uuid
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.db import get_db
from app.repositories import user_repository
from app.core.security import verify_access_token

security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """Extract and verify JWT token from Authorization header and return authenticated User."""
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user identifier format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user


def require_customer(current_user: User = Depends(get_current_user)) -> User:
    """Enforce customer role."""
    if current_user.role != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Customer role required",
        )
    return current_user


def require_provider(current_user: User = Depends(get_current_user)) -> User:
    """Enforce provider role."""
    if current_user.role != "provider":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Provider role required",
        )
    return current_user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Enforce admin role."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Admin role required",
        )
    return current_user


def require_permission(required_permission: str):
    """Enforce specific RBAC permission dependency."""
    def dependency(
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
    ) -> User:
        from app.models.security import AdminRole

        # Super Admin bypasses single module restrictions
        if current_user.role == "super_admin":
            return current_user

        role_entry = db.query(AdminRole).filter(AdminRole.user_id == current_user.id).first()
        if role_entry and role_entry.role_name == "super_admin":
            return current_user

        user_perms = role_entry.permissions if role_entry else []
        r_name = role_entry.role_name if role_entry else current_user.role

        module_prefix = required_permission.split(":")[0]
        action_type = required_permission.split(":")[1] if ":" in required_permission else "view"

        has_perm = (
            required_permission in user_perms or
            f"{module_prefix}:manage" in user_perms or
            "super_admin" in user_perms or
            (action_type in ["edit", "create", "delete", "save", "update", "status"] and f"{module_prefix}:edit" in user_perms) or
            (action_type == "view" and (f"{module_prefix}:view" in user_perms or len(user_perms) > 0))
        )

        if not has_perm:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: Insufficient permissions for action '{required_permission}'. Required for role '{r_name}'."
            )

        return current_user

    return dependency
