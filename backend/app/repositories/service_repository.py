import uuid
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate

def get_services(
    db: Session,
    skip: int = 0,
    limit: int = 1000,
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    search: Optional[str] = None,
) -> List[Service]:
    """Retrieve services for Admin Catalog (both active and inactive)."""
    query = db.query(Service)

    if category:
        query = query.filter(Service.category.ilike(f"%{category}%"))
    if subcategory:
        query = query.filter(Service.subcategory.ilike(f"%{subcategory}%"))
    if search:
        query = query.filter(
            Service.name.ilike(f"%{search}%")
            | Service.category.ilike(f"%{search}%")
            | Service.subcategory.ilike(f"%{search}%")
        )

    return query.offset(skip).limit(limit).all()

def count_services(
    db: Session,
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    search: Optional[str] = None,
) -> int:
    query = db.query(func.count(Service.id))

    if category:
        query = query.filter(Service.category.ilike(f"%{category}%"))
    if subcategory:
        query = query.filter(Service.subcategory.ilike(f"%{subcategory}%"))
    if search:
        query = query.filter(
            Service.name.ilike(f"%{search}%")
            | Service.category.ilike(f"%{search}%")
            | Service.subcategory.ilike(f"%{search}%")
        )

    return query.scalar() or 0

def get_service_by_id(db: Session, service_id: uuid.UUID) -> Optional[Service]:
    """Retrieve service by UUID without active status filter."""
    return db.query(Service).filter(Service.id == service_id).first()

def get_categories(db: Session) -> List[Dict[str, List[str]]]:
    rows = (
        db.query(Service.category, Service.subcategory)
        .distinct()
        .all()
    )

    cat_map: Dict[str, set] = {}
    for cat, subcat in rows:
        if cat not in cat_map:
            cat_map[cat] = set()
        if subcat:
            cat_map[cat].add(subcat)

    result = []
    for cat, subcats in sorted(cat_map.items()):
        result.append({
            "category": cat,
            "subcategories": sorted(list(subcats))
        })
    return result

def create_service(
    db: Session,
    category: str,
    subcategory: str,
    name: str,
    base_price: float,
    max_demand_increase: float = 0.5,
    max_discount: float = 0.3,
    distinct_features: Optional[List[str]] = None,
    suggested_addons: Optional[List[Dict[str, Any]]] = None,
    is_active: bool = True
) -> Service:
    service = Service(
        category=category,
        subcategory=subcategory,
        name=name,
        base_price=base_price,
        max_demand_increase=max_demand_increase,
        max_discount=max_discount,
        distinct_features=distinct_features or [],
        suggested_addons=suggested_addons or [],
        is_active=is_active,
    )
    db.add(service)
    db.commit()
    db.refresh(service)
    return service

def update_service(
    db: Session,
    service: Service,
    name: Optional[str] = None,
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    base_price: Optional[float] = None,
    max_demand_increase: Optional[float] = None,
    max_discount: Optional[float] = None,
    distinct_features: Optional[List[str]] = None,
    suggested_addons: Optional[List[Dict[str, Any]]] = None,
    is_active: Optional[bool] = None
) -> Service:
    if name is not None:
        service.name = name
    if category is not None:
        service.category = category
    if subcategory is not None:
        service.subcategory = subcategory
    if base_price is not None:
        service.base_price = base_price
    if max_demand_increase is not None:
        service.max_demand_increase = max_demand_increase
    if max_discount is not None:
        service.max_discount = max_discount
    if distinct_features is not None:
        service.distinct_features = distinct_features
    if suggested_addons is not None:
        service.suggested_addons = suggested_addons
    if is_active is not None:
        service.is_active = is_active

    db.commit()
    db.refresh(service)
    return service
