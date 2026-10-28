import uuid
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.repositories.db import get_db
from app.schemas.service import ServiceRead, ServiceCreate, CategorySubcategoryResponse
from app.repositories import service_repository
from app.core.cache import get_cache

router = APIRouter(prefix="/services", tags=["Services"])


class ServiceListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[ServiceRead]


@router.get("/metrics/cache", summary="Get service catalog cache performance telemetry")
def get_catalog_cache_stats():
    """Retrieve live cache telemetry including hit ratio and active keys."""
    return get_cache().get_stats()


@router.get("/", response_model=ServiceListResponse)
def list_services(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    category: Optional[str] = Query(None, description="Filter by category"),
    subcategory: Optional[str] = Query(None, description="Filter by subcategory"),
    search: Optional[str] = Query(None, description="Search by name or category"),
    db: Session = Depends(get_db),
):
    """
    Retrieve bookable services from database with caching, filtering, and pagination.
    """
    cache = get_cache()
    cache_key = f"catalog:services:{skip}:{limit}:{category}:{subcategory}:{search}"
    cached_res = cache.get(cache_key)
    if cached_res is not None:
        return cached_res

    total = service_repository.count_services(
        db=db, category=category, subcategory=subcategory, search=search
    )
    items = service_repository.get_services(
        db=db, skip=skip, limit=limit, category=category, subcategory=subcategory, search=search
    )
    res = ServiceListResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=items,
    )
    cache.set(cache_key, res, ttl_seconds=180)
    return res


@router.get("/categories", response_model=List[CategorySubcategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    """
    Retrieve all service categories and subcategories with in-memory TTL caching.
    """
    cache = get_cache()
    cache_key = "catalog:categories"
    cached_cats = cache.get(cache_key)
    if cached_cats is not None:
        return cached_cats

    data = service_repository.get_categories(db=db)
    cache.set(cache_key, data, ttl_seconds=300)
    return data


@router.get("/{service_id}", response_model=ServiceRead)
def get_service_by_id(service_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Get service details by UUID with caching.
    """
    cache = get_cache()
    cache_key = f"catalog:service:{service_id}"
    cached_srv = cache.get(cache_key)
    if cached_srv is not None:
        return cached_srv

    service = service_repository.get_service_by_id(db=db, service_id=service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service not found"
        )
    cache.set(cache_key, service, ttl_seconds=300)
    return service
