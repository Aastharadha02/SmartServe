from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.models.customer import Customer
from app.models.provider import Provider
from app.models.user import User
from app.repositories import user_repository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserResponse


def register_customer(db: Session, data: RegisterRequest) -> TokenResponse:
    """Register customer user with profile and return access token."""
    existing_user = user_repository.get_user_by_email(db, data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    hashed_pw = hash_password(data.password)
    user = User(
        email=data.email,
        password_hash=hashed_pw,
        role="customer",
        is_active=True,
    )
    customer = Customer(
        full_name=data.full_name,
        phone=data.phone,
    )

    created_user = user_repository.create_user(db, user, customer=customer)
    token = create_access_token(
        data={"sub": str(created_user.id), "role": created_user.role}
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse.model_validate(created_user),
    )


def register_provider(db: Session, data: RegisterRequest) -> TokenResponse:
    """Register provider user with profile and return access token."""
    existing_user = user_repository.get_user_by_email(db, data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    hashed_pw = hash_password(data.password)
    user = User(
        email=data.email,
        password_hash=hashed_pw,
        role="provider",
        is_active=True,
    )
    provider = Provider(
        full_name=data.full_name,
        phone=data.phone,
    )

    created_user = user_repository.create_user(db, user, provider=provider)
    token = create_access_token(
        data={"sub": str(created_user.id), "role": created_user.role}
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse.model_validate(created_user),
    )


def register_user(db: Session, data: RegisterRequest) -> TokenResponse:
    """Branch registration based on data.role field."""
    role = (data.role or "customer").lower()
    if role == "provider":
        return register_provider(db, data)
    elif role == "customer":
        return register_customer(db, data)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role: '{data.role}'. Must be 'customer' or 'provider'.",
        )


def login_user(db: Session, data: LoginRequest) -> TokenResponse:
    """Authenticate user credentials and return access token."""
    user = user_repository.get_user_by_email(db, data.email)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is inactive",
        )

    token = create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )
