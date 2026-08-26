import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin, require_permission
from app.core.security import hash_password
from app.repositories.db import get_db
from app.repositories import user_repository, audit_repository
from app.models.user import User
from app.models.security import AdminRole
from app.schemas.people import AdminCreateRequest

router = APIRouter(prefix="/admin/admins", tags=["Admin People Management — Admins & Roles"])

from typing import Optional
from app.models.security import AuditLog
from app.schemas.people import (
    AdminCreateRequest, 
    AdminRoleUpdateRequest, 
    AdminDetailResponse, 
    AccountStatusRequest
)

router = APIRouter(prefix="/admin/admins", tags=["Admin People Management — Admins & Roles"])

SYSTEM_PERMISSION_MATRIX = [
    {
        "module": "Dashboard",
        "actions": ["View"]
    },
    {
        "module": "Catalog",
        "actions": ["View", "Create", "Edit", "Delete", "Export", "Import"]
    },
    {
        "module": "Providers",
        "actions": ["View", "Approve", "Edit", "Manage"]
    },
    {
        "module": "Customers",
        "actions": ["View", "Flag", "Suspend", "Manage"]
    },
    {
        "module": "Bookings",
        "actions": ["View", "Manage", "Cancel"]
    },
    {
        "module": "Support",
        "actions": ["View", "Manage"]
    },
    {
        "module": "Security",
        "actions": ["View", "Manage"]
    },
    {
        "module": "Admin Management",
        "actions": ["View", "Create", "Role Assignment", "Suspend"]
    }
]

@router.get("/", response_model=List[AdminDetailResponse])
def list_admin_accounts(
    search: Optional[str] = None,
    role_name: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_2fa_enabled: Optional[bool] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """List all registered admin accounts with search & RBAC filters."""
    query = db.query(User).filter(User.role.in_(["admin", "super_admin"]))

    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    if is_2fa_enabled is not None:
        query = query.filter(User.is_2fa_enabled == is_2fa_enabled)

    admins = query.all()
    res = []

    for a in admins:
        if search:
            s_lower = search.lower()
            if s_lower not in a.email.lower() and s_lower not in str(a.id).lower():
                continue

        role_entry = db.query(AdminRole).filter(AdminRole.user_id == a.id).first()
        r_name = role_entry.role_name if role_entry else ("super_admin" if a.role == "super_admin" else "operations_admin")

        if role_name and r_name.lower() != role_name.lower():
            continue

        perms = role_entry.permissions if role_entry else ["dashboard:view", "catalog:manage", "providers:manage", "customers:manage", "security:manage"]

        # Fetch recent audit logs for this admin
        recent_logs = db.query(AuditLog).filter(
            (AuditLog.actor_id == a.id) | 
            (AuditLog.actor_email == a.email) | 
            (AuditLog.target_resource == str(a.id))
        ).order_by(AuditLog.created_at.desc()).limit(5).all()

        act_list = [
            {
                "id": str(log.id),
                "action": log.action,
                "created_at": log.created_at.isoformat() if log.created_at else ""
            } for log in recent_logs
        ]

        res.append(AdminDetailResponse(
            id=str(a.id),
            email=a.email,
            role=a.role,
            role_name=r_name,
            permissions=perms,
            is_active=a.is_active,
            is_2fa_enabled=a.is_2fa_enabled,
            created_at=a.created_at.isoformat() if a.created_at else "",
            recent_activity=act_list
        ))
    return res

@router.get("/permissions-matrix")
def get_permissions_matrix(
    admin: User = Depends(require_admin)
):
    """Return standard RBAC system permission matrix."""
    return SYSTEM_PERMISSION_MATRIX

@router.get("/{admin_id}", response_model=AdminDetailResponse)
def get_admin_detail(
    admin_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Retrieve detailed admin profile by ID, including permissions, 2FA status, and audit activity."""
    try:
        a_uuid = uuid.UUID(admin_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid admin ID format")

    target_admin = db.query(User).filter(User.id == a_uuid).first()
    if not target_admin or target_admin.role not in ["admin", "super_admin"]:
        raise HTTPException(status_code=404, detail="Admin account not found")

    role_entry = db.query(AdminRole).filter(AdminRole.user_id == a_uuid).first()
    r_name = role_entry.role_name if role_entry else "super_admin"
    perms = role_entry.permissions if role_entry else ["dashboard:view", "catalog:manage", "providers:manage", "customers:manage", "security:manage"]

    recent_logs = db.query(AuditLog).filter(
        (AuditLog.actor_id == target_admin.id) | 
        (AuditLog.actor_email == target_admin.email) | 
        (AuditLog.target_resource == str(target_admin.id))
    ).order_by(AuditLog.created_at.desc()).limit(10).all()

    act_list = [
        {
            "id": str(log.id),
            "action": log.action,
            "created_at": log.created_at.isoformat() if log.created_at else ""
        } for log in recent_logs
    ]

    return AdminDetailResponse(
        id=str(target_admin.id),
        email=target_admin.email,
        role=target_admin.role,
        role_name=r_name,
        permissions=perms,
        is_active=target_admin.is_active,
        is_2fa_enabled=target_admin.is_2fa_enabled,
        created_at=target_admin.created_at.isoformat() if target_admin.created_at else "",
        recent_activity=act_list
    )

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_admin_account(
    req: AdminCreateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("admins:manage"))
):
    """Create a new Admin account with RBAC permissions."""
    existing = user_repository.get_user_by_email(db, req.email)
    if existing:
        raise HTTPException(status_code=400, detail="User email already exists")

    new_user = User(
        id=uuid.uuid4(),
        email=req.email,
        password_hash=hash_password(req.password),
        role="admin",
        is_active=True
    )
    db.add(new_user)
    db.flush()

    default_perms = req.permissions or ["dashboard:view", "catalog:manage", "providers:manage"]
    role_entry = AdminRole(
        id=uuid.uuid4(),
        user_id=new_user.id,
        role_name=req.role_name,
        permissions=default_perms,
        is_active=True
    )
    db.add(role_entry)
    db.commit()

    audit_repository.create_audit_log(
        db, actor_id=admin.id, actor_email=admin.email, actor_role=admin.role,
        action=f"Created Admin Account '{req.email}' ({req.role_name})",
        target_resource=str(new_user.id)
    )

    return {
        "status": "success",
        "user_id": str(new_user.id),
        "email": new_user.email,
        "role_name": req.role_name,
        "permissions": role_entry.permissions
    }

@router.patch("/{admin_id}/role")
def update_admin_role(
    admin_id: str,
    req: AdminRoleUpdateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("admins:manage"))
):
    """Assign or change RBAC role & permissions for an administrator."""
    try:
        a_uuid = uuid.UUID(admin_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid admin ID format")

    target_user = db.query(User).filter(User.id == a_uuid).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Admin account not found")

    role_entry = db.query(AdminRole).filter(AdminRole.user_id == a_uuid).first()
    if not role_entry:
        role_entry = AdminRole(
            id=uuid.uuid4(),
            user_id=a_uuid,
            role_name=req.role_name,
            permissions=req.permissions or ["dashboard:view"],
            is_active=True
        )
        db.add(role_entry)
    else:
        role_entry.role_name = req.role_name
        if req.permissions:
            role_entry.permissions = req.permissions

    db.commit()

    audit_repository.create_audit_log(
        db, actor_id=admin.id, actor_email=admin.email, actor_role=admin.role,
        action=f"Role Changed for '{target_user.email}' to {req.role_name}",
        target_resource=str(a_uuid),
        metadata_json={"new_role": req.role_name, "permissions": role_entry.permissions}
    )

    return {
        "status": "success",
        "admin_id": admin_id,
        "role_name": req.role_name,
        "permissions": role_entry.permissions,
        "message": f"Admin role updated to {req.role_name}."
    }

@router.post("/{admin_id}/status", status_code=status.HTTP_200_OK)
def update_admin_account_status(
    admin_id: str,
    req: AccountStatusRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Suspend or reactivate an administrator account."""
    try:
        a_uuid = uuid.UUID(admin_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid admin ID format")

    if a_uuid == admin.id and not req.is_active:
        raise HTTPException(status_code=400, detail="You cannot deactivate your own active administrator account.")

    target_user = db.query(User).filter(User.id == a_uuid).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Admin account not found")

    target_user.is_active = req.is_active
    db.commit()

    action_str = "Reactivated" if req.is_active else "Suspended"
    audit_repository.create_audit_log(
        db, actor_id=admin.id, actor_email=admin.email, actor_role=admin.role,
        action=f"Admin Account {action_str} ({target_user.email})",
        target_resource=str(a_uuid),
        metadata_json={"reason": req.reason or "Admin Action"}
    )

    return {
        "status": "success",
        "admin_id": admin_id,
        "is_active": req.is_active,
        "message": f"Admin account successfully {action_str.lower()}."
    }
