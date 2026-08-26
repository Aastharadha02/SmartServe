import uuid
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.repositories.db import get_db
from app.schemas.service import ServiceRead, ServiceCreate, CategorySubcategoryResponse
from app.repositories import service_repository

router = APIRouter(prefix="/services", tags=["Services"])


class ServiceListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[ServiceRead]


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
    Retrieve bookable services from PostgreSQL database with filtering and pagination.
    """
    total = service_repository.count_services(
        db=db, category=category, subcategory=subcategory, search=search
    )
    items = service_repository.get_services(
        db=db, skip=skip, limit=limit, category=category, subcategory=subcategory, search=search
    )
    return ServiceListResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=items,
    )


@router.get("/categories", response_model=List[CategorySubcategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    """
    Retrieve all service categories and subcategories.
    """
    return service_repository.get_categories(db=db)


@router.get("/{service_id}", response_model=ServiceRead)
def get_service_by_id(service_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Get service details by UUID.
    """
    service = service_repository.get_service_by_id(db=db, service_id=service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service not found"
        )
    return service
