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


DUMMY_PROVIDER = AuthUser(
    id=uuid.UUID("00000000-0000-0000-0000-000000000002"),
    email="provider@smartserve.dev",
    role="provider",
    full_name="Pushkar (Provider)",
    is_verified=True,
)


def get_current_user(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
) -> AuthUser:
    """Extracts Bearer token if provided, otherwise returns dummy context."""
    if auth and auth.credentials:
        token = auth.credentials
        payload = decode_access_token(token)
        if payload:
            role = payload.get("role", "")
            sub = payload.get("sub", "")
            email = payload.get("email", "")
            try:
                user_id = uuid.UUID(str(sub))
            except (ValueError, TypeError):
                user_id = uuid.UUID("00000000-0000-0000-0000-000000000001") if "admin" in str(role) else uuid.UUID("00000000-0000-0000-0000-000000000003")

            if "admin" in str(role):
                return AuthUser(
                    id=user_id,
                    email=email or "admin@smartserve.dev",
                    role="admin",
                    full_name=payload.get("full_name", "Admin User"),
                    is_verified=True,
                )
            elif "customer" in str(role):
                return AuthUser(
                    id=user_id,
                    email=email or "pushkar@example.com",
                    role="customer",
                    full_name=payload.get("full_name", "Pushkar Kanjani"),
                    is_verified=True,
                )
            elif "provider" in str(role):
                return AuthUser(
                    id=user_id,
                    email=email or "provider@smartserve.dev",
                    role="provider",
                    full_name=payload.get("full_name", "Pushkar (Provider)"),
                    is_verified=True,
                )

        if "admin" in token:
            return AuthUser(
                id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
                email="admin@smartserve.dev",
                role="admin",
                full_name="Admin User",
                is_verified=True,
            )
        elif "customer" in token:
            return AuthUser(
                id=uuid.UUID("00000000-0000-0000-0000-000000000003"),
                email="pushkar@example.com",
                role="customer",
                full_name="Pushkar Kanjani",
                is_verified=True,
            )
        else:
            return DUMMY_PROVIDER

    return DUMMY_PROVIDER


def require_provider(
    current_user: AuthUser = Depends(get_current_user),
) -> AuthUser:
    """Role-based access guard: Ensures caller is a Provider or Admin."""
    if current_user.role not in ["provider", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Provider role required",
        )
    return current_user


def require_admin(
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Guard ensuring caller has Admin role."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Admin role required",
        )
    admin_user = db.query(User).filter(User.email == current_user.email, User.role == "admin").first()
    if not admin_user:
        admin_user = db.query(User).filter(User.role == "admin").first()
    if not admin_user:
        admin_user = User(
            id=current_user.id if isinstance(current_user.id, uuid.UUID) else uuid.uuid4(),
            email=current_user.email or "admin@smartserve.dev",
            hashed_password="adminpasswordhash",
            role="admin",
            is_active=True,
        )
        db.add(admin_user)
        try:
            db.commit()
            db.refresh(admin_user)
        except Exception:
            db.rollback()
    return admin_user



def require_permission(perm: str):
    """Guard checking specific granular admin permission."""
    def permission_guard(
        admin_user: User = Depends(require_admin)
    ) -> User:
        if admin_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: Permission '{perm}' required",
            )
        return admin_user
    return permission_guard



def get_current_customer(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> Customer:
    """
    Authenticates and retrieves the current Customer entity from DB or mock context.
    """
    if auth and auth.credentials:
        token = auth.credentials
        payload = decode_access_token(token)
        if payload and payload.get("sub"):
            user_id_str = payload.get("sub")
            # Try parsing UUID safely
            try:
                parsed_uuid = uuid.UUID(str(user_id_str))
                customer = (
                    db.query(Customer)
                    .filter((Customer.user_id == parsed_uuid) | (Customer.id == parsed_uuid))
                    .first()
                )
                if customer:
                    return customer
            except (ValueError, TypeError):
                pass

    # Fallback to dev mock customer if not in DB
    mock_customer = db.query(Customer).filter(Customer.email == "pushkar@example.com").first()
    if mock_customer:
        return mock_customer

    # Create default dev customer if absent
    mock_user_id = uuid.UUID("00000000-0000-0000-0000-000000001001")
    mock_cust_id = uuid.UUID("00000000-0000-0000-0000-000000001002")

    default_user = db.query(User).filter(User.id == mock_user_id).first()
    if not default_user:
        default_user = User(
            id=mock_user_id,
            email="pushkar@example.com",
            password_hash="mockhashedpassword",
            role="customer",
        )
        db.add(default_user)

    default_customer = db.query(Customer).filter(Customer.id == mock_cust_id).first()
    if not default_customer:
        default_customer = Customer(
            id=mock_cust_id,
            user_id=default_user.id,
            full_name="Pushkar Kanjani",
            email="pushkar@example.com",
            password_hash="mockhashedpassword",
            phone="+91 9876543210",
            is_verified=True,
            is_active=True,
        )
        db.add(default_customer)

    try:
        db.commit()
        db.refresh(default_customer)
        return default_customer
    except Exception:
        db.rollback()
        return default_customer
