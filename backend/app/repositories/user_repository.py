import uuid
from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.user import User
from app.models.customer import Customer
from app.models.provider import Provider


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Fetch user by email using SQLAlchemy 2.x select with eager loading."""
    stmt = (
        select(User)
        .options(joinedload(User.customer), joinedload(User.provider))
        .where(User.email == email)
    )
    return db.execute(stmt).scalar_one_or_none()


def get_user_by_id(db: Session, user_id: uuid.UUID | str) -> Optional[User]:
    """Fetch user by UUID using SQLAlchemy 2.x select with eager loading."""
    if isinstance(user_id, str):
        user_id = uuid.UUID(user_id)
    stmt = (
        select(User)
        .options(joinedload(User.customer), joinedload(User.provider))
        .where(User.id == user_id)
    )
    return db.execute(stmt).scalar_one_or_none()


def create_user(
    db: Session,
    user: User,
    customer: Optional[Customer] = None,
    provider: Optional[Provider] = None,
) -> User:
    """Persist user and associated profile to database."""
    db.add(user)
    if customer:
        customer.user = user
        db.add(customer)
    if provider:
        provider.user = user
        db.add(provider)
    db.commit()
    db.refresh(user)
    return user
