import uuid
from datetime import datetime, timezone, timedelta
from app.repositories.db import get_db
from app.models.user import User
from app.models.security import AdminRole, AuditLog
from app.core.security import hash_password

def seed_initial_admins():
    db = next(get_db())

    # Ensure admin@smartserve.com exists and has AdminRole record
    default_admin = db.query(User).filter(User.email == "admin@smartserve.com").first()
    if not default_admin:
        default_admin = User(
            id=uuid.uuid4(),
            email="admin@smartserve.com",
            password_hash=hash_password("AdminPassword123!"),
            role="super_admin",
            is_active=True,
            is_2fa_enabled=False,
            created_at=datetime.now(timezone.utc) - timedelta(days=90)
        )
        db.add(default_admin)
        db.flush()

    role_entry = db.query(AdminRole).filter(AdminRole.user_id == default_admin.id).first()
    if not role_entry:
        role_entry = AdminRole(
            id=uuid.uuid4(),
            user_id=default_admin.id,
            role_name="super_admin",
            permissions=["dashboard:view", "catalog:manage", "providers:manage", "customers:manage", "bookings:manage", "insights:view", "support:manage", "security:manage", "admins:manage", "emails:manage", "settings:manage"],
            is_active=True
        )
        db.add(role_entry)
        db.commit()

    existing_count = db.query(User).filter(User.role == "admin").count()
    if existing_count >= 4:
        print(f"Admin accounts already exist ({existing_count} records). Skipping seed.")
        return

    print("Seeding initial realistic admin accounts & RBAC permissions into PostgreSQL...")

    sample_admins = [
        {
            "email": "priya.sharma@smartserve.com",
            "role_name": "operations_admin",
            "permissions": ["dashboard:view", "catalog:edit", "providers:manage", "customers:view", "bookings:manage", "support:manage"],
            "is_2fa": True,
            "is_active": True
        },
        {
            "email": "rahul.verma@smartserve.com",
            "role_name": "support_admin",
            "permissions": ["dashboard:view", "providers:view", "customers:view", "bookings:view", "support:manage"],
            "is_2fa": False,
            "is_active": True
        },
        {
            "email": "vikram.patel@smartserve.com",
            "role_name": "catalog_admin",
            "permissions": ["dashboard:view", "catalog:manage", "catalog:export", "catalog:import"],
            "is_2fa": False,
            "is_active": False
        }
    ]

    for adata in sample_admins:
        existing = db.query(User).filter(User.email == adata["email"]).first()
        if existing:
            continue

        user = User(
            id=uuid.uuid4(),
            email=adata["email"],
            password_hash=hash_password("AdminPassword123!"),
            role="admin",
            is_active=adata["is_active"],
            is_2fa_enabled=adata["is_2fa"],
            created_at=datetime.now(timezone.utc) - timedelta(days=60)
        )
        db.add(user)
        db.flush()

        role_entry = AdminRole(
            id=uuid.uuid4(),
            user_id=user.id,
            role_name=adata["role_name"],
            permissions=adata["permissions"],
            is_active=adata["is_active"],
            created_at=datetime.now(timezone.utc) - timedelta(days=60)
        )
        db.add(role_entry)

        audit = AuditLog(
            id=uuid.uuid4(),
            actor_id=default_admin.id if default_admin else user.id,
            actor_email="admin@smartserve.com",
            actor_role="super_admin",
            action=f"Created Admin Account '{user.email}' ({adata['role_name']})",
            target_resource=str(user.id),
            risk_level="Info",
            created_at=datetime.now(timezone.utc) - timedelta(days=60)
        )
        db.add(audit)

    db.commit()
    print("Initial admin accounts & RBAC permissions seeded successfully!")

if __name__ == "__main__":
    seed_initial_admins()
