import uuid
from decimal import Decimal
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.dependencies import get_current_customer, require_admin
from app.models.user import User
from app.models.customer import Customer
from app.models.coupon import Coupon, CouponRedemption
from app.services.coupon_service import (
    validate_coupon,
    redeem_coupon,
    mint_spin_reward_coupon,
    round_curr,
)

router = APIRouter(prefix="/coupons", tags=["coupons"])
admin_coupons_router = APIRouter(prefix="/admin/coupons", tags=["admin-coupons"])


# Schemas
class CouponValidateRequest(BaseModel):
    code: str = Field(..., min_length=2, max_length=50)
    subtotal: Decimal = Field(..., ge=0)
    category: Optional[str] = None
    service_id: Optional[str] = None
    service_ids: Optional[List[str]] = None


class CouponValidateResponse(BaseModel):
    is_valid: bool
    code: str
    discount_amount: Decimal
    final_total: Decimal
    message: str
    discount_type: Optional[str] = None
    discount_value: Optional[Decimal] = None
    min_order_amount: Optional[Decimal] = None


class SpinRewardRequest(BaseModel):
    reward_tier: Optional[str] = "SERVE75"
    booking_id: Optional[str] = None


class SpinRewardResponse(BaseModel):
    success: bool
    code: str
    discount_value: Decimal
    discount_type: str
    min_order_amount: Decimal
    description: str
    valid_days: int
    message: str


class CouponItem(BaseModel):
    id: str
    code: str
    description: Optional[str] = None
    discount_type: str
    discount_value: Decimal
    max_discount_amount: Optional[Decimal] = None
    min_order_amount: Decimal
    is_active: bool
    is_spin_reward: bool
    valid_until: Optional[datetime] = None


class AdminCouponCreateRequest(BaseModel):
    code: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = None
    discount_type: str = "FIXED"  # "FIXED" or "PERCENTAGE"
    discount_value: Decimal = Field(..., gt=0)
    max_discount_amount: Optional[Decimal] = None
    min_order_amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    max_uses: Optional[int] = None
    max_uses_per_customer: int = 1
    valid_days: Optional[int] = 30
    applicable_categories: Optional[List[str]] = None


class AdminCouponDetail(BaseModel):
    id: str
    code: str
    description: Optional[str] = None
    discount_type: str
    discount_value: Decimal
    max_discount_amount: Optional[Decimal] = None
    min_order_amount: Decimal
    is_active: bool
    is_spin_reward: bool
    max_uses: Optional[int] = None
    max_uses_per_customer: int
    valid_from: datetime
    valid_until: Optional[datetime] = None
    redemption_count: int = 0
    total_discount_given: Decimal = Decimal("0.00")


# --- Customer Endpoints ---

@router.post("/validate", response_model=CouponValidateResponse)
def validate_customer_coupon(
    payload: CouponValidateRequest,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    """
    Validate a coupon code and calculate authentic server-side discount.
    Never trusts client calculations; enforces order thresholds and usage caps.
    """
    s_id = None
    if payload.service_id:
        try:
            s_id = uuid.UUID(payload.service_id)
        except ValueError:
            pass

    s_ids = None
    if payload.service_ids:
        s_ids = []
        for sid in payload.service_ids:
            try:
                s_ids.append(uuid.UUID(sid))
            except ValueError:
                pass

    is_valid, msg, discount, coupon = validate_coupon(
        db=db,
        code=payload.code,
        customer_id=current_customer.id,
        subtotal=payload.subtotal,
        category=payload.category,
        service_id=s_id,
        service_ids=s_ids,
    )

    final_total = max(Decimal("0.00"), payload.subtotal - discount)
    if not is_valid:
        return CouponValidateResponse(
            is_valid=False,
            code=payload.code.strip().upper(),
            discount_amount=Decimal("0.00"),
            final_total=payload.subtotal,
            message=msg,
        )

    return CouponValidateResponse(
        is_valid=True,
        code=coupon.code,
        discount_amount=discount,
        final_total=final_total,
        message=msg,
        discount_type=coupon.discount_type,
        discount_value=coupon.discount_value,
        min_order_amount=coupon.min_order_amount,
    )


@router.post("/spin-reward", response_model=SpinRewardResponse)
def claim_spin_wheel_reward(
    payload: SpinRewardRequest,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    """
    Mint a legitimate, tamper-proof, single-use coupon for a customer's spin-the-wheel win.
    """
    coupon = mint_spin_reward_coupon(
        db=db,
        customer_id=current_customer.id,
        reward_tier=payload.reward_tier,
    )

    return SpinRewardResponse(
        success=True,
        code=coupon.code,
        discount_value=coupon.discount_value,
        discount_type=coupon.discount_type,
        min_order_amount=coupon.min_order_amount,
        description=coupon.description or "Spin & Win Promotional Reward",
        valid_days=30,
        message=f"Congratulations! You unlocked code '{coupon.code}'. Apply at checkout for discount.",
    )


@router.get("", response_model=List[CouponItem])
def list_available_coupons(
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    """
    List active public platform coupons and exclusive spin coupons for the authenticated customer.
    """
    now_utc = datetime.now(timezone.utc)
    coupons = (
        db.query(Coupon)
        .filter(
            Coupon.is_active == True,
            (Coupon.customer_id == None) | (Coupon.customer_id == current_customer.id),
            (Coupon.valid_until == None) | (Coupon.valid_until > now_utc),
        )
        .order_by(Coupon.created_at.desc())
        .limit(20)
        .all()
    )

    result = []
    for c in coupons:
        # Check if customer already reached max uses
        used_count = (
            db.query(func.count(CouponRedemption.id))
            .filter(CouponRedemption.coupon_id == c.id, CouponRedemption.customer_id == current_customer.id)
            .scalar()
            or 0
        )
        if used_count < c.max_uses_per_customer:
            result.append(
                CouponItem(
                    id=str(c.id),
                    code=c.code,
                    description=c.description,
                    discount_type=c.discount_type,
                    discount_value=c.discount_value,
                    max_discount_amount=c.max_discount_amount,
                    min_order_amount=c.min_order_amount,
                    is_active=c.is_active,
                    is_spin_reward=c.is_spin_reward,
                    valid_until=c.valid_until,
                )
            )
    return result


# --- Admin Endpoints ---

@admin_coupons_router.get("", response_model=List[AdminCouponDetail])
def list_admin_coupons(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Admin view: List all platform and reward coupons with redemption audit metrics."""
    coupons = db.query(Coupon).order_by(Coupon.created_at.desc()).all()

    out = []
    for c in coupons:
        redemptions = db.query(CouponRedemption).filter(CouponRedemption.coupon_id == c.id).all()
        redemption_count = len(redemptions)
        total_discount = sum((r.discount_applied for r in redemptions), Decimal("0.00"))

        out.append(
            AdminCouponDetail(
                id=str(c.id),
                code=c.code,
                description=c.description,
                discount_type=c.discount_type,
                discount_value=c.discount_value,
                max_discount_amount=c.max_discount_amount,
                min_order_amount=c.min_order_amount,
                is_active=c.is_active,
                is_spin_reward=c.is_spin_reward,
                max_uses=c.max_uses,
                max_uses_per_customer=c.max_uses_per_customer,
                valid_from=c.valid_from,
                valid_until=c.valid_until,
                redemption_count=redemption_count,
                total_discount_given=total_discount,
            )
        )
    return out


@admin_coupons_router.post("", response_model=AdminCouponDetail, status_code=status.HTTP_201_CREATED)
def create_admin_coupon(
    payload: AdminCouponCreateRequest,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Admin view: Create a new platform promotion or marketing campaign coupon."""
    code_clean = payload.code.strip().upper()
    existing = db.query(Coupon).filter(Coupon.code == code_clean).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Coupon code '{code_clean}' already exists.")

    disc_type = payload.discount_type.upper().strip()
    if disc_type not in ["FIXED", "PERCENTAGE"]:
        raise HTTPException(status_code=400, detail="Discount type must be 'FIXED' or 'PERCENTAGE'.")

    now_utc = datetime.now(timezone.utc)
    valid_until = now_utc + timedelta(days=payload.valid_days) if payload.valid_days else None

    coupon = Coupon(
        id=uuid.uuid4(),
        code=code_clean,
        description=payload.description.strip() if payload.description else None,
        discount_type=disc_type,
        discount_value=payload.discount_value,
        max_discount_amount=payload.max_discount_amount,
        min_order_amount=payload.min_order_amount,
        is_active=True,
        valid_from=now_utc,
        valid_until=valid_until,
        max_uses=payload.max_uses,
        max_uses_per_customer=payload.max_uses_per_customer,
        applicable_categories=payload.applicable_categories,
        is_spin_reward=False,
    )
    db.add(coupon)
    db.commit()
    db.refresh(coupon)

    return AdminCouponDetail(
        id=str(coupon.id),
        code=coupon.code,
        description=coupon.description,
        discount_type=coupon.discount_type,
        discount_value=coupon.discount_value,
        max_discount_amount=coupon.max_discount_amount,
        min_order_amount=coupon.min_order_amount,
        is_active=coupon.is_active,
        is_spin_reward=coupon.is_spin_reward,
        max_uses=coupon.max_uses,
        max_uses_per_customer=coupon.max_uses_per_customer,
        valid_from=coupon.valid_from,
        valid_until=coupon.valid_until,
        redemption_count=0,
        total_discount_given=Decimal("0.00"),
    )


@admin_coupons_router.patch("/{coupon_id}/toggle", response_model=Dict[str, Any])
def toggle_admin_coupon(
    coupon_id: str,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Admin view: Activate or deactivate a coupon instantly."""
    try:
        c_uuid = uuid.UUID(coupon_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid coupon ID format.")

    coupon = db.query(Coupon).filter(Coupon.id == c_uuid).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found.")

    coupon.is_active = not coupon.is_active
    coupon.updated_at = datetime.now(timezone.utc)
    db.add(coupon)
    db.commit()
    db.refresh(coupon)

    return {
        "success": True,
        "coupon_id": str(coupon.id),
        "code": coupon.code,
        "is_active": coupon.is_active,
        "message": f"Coupon '{coupon.code}' is now {'active' if coupon.is_active else 'inactive'}.",
    }
