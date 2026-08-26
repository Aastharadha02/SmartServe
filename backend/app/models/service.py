import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import String, Float, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Service(Base):
    __tablename__ = "services"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    category: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True
    )
    subcategory: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True
    )
    base_price: Mapped[float] = mapped_column(Float, nullable=False)
    max_demand_increase: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.0
    )
    max_discount: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.0
    )
    distinct_features: Mapped[Optional[List[str]]] = mapped_column(
        JSONB, nullable=True
    )
    suggested_addons: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(
        JSONB, nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
