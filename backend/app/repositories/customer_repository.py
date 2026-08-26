import uuid
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.customer import Customer

def get_customer_by_id(db: Session, customer_id: uuid.UUID) -> Optional[Customer]:
    return db.query(Customer).filter(Customer.id == customer_id).first()

def get_customer_by_email(db: Session, email: str) -> Optional[Customer]:
    return db.query(Customer).filter(Customer.email == email).first()

def get_customers(db: Session, skip: int = 0, limit: int = 50) -> List[Customer]:
    return db.query(Customer).offset(skip).limit(limit).all()
