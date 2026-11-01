import uuid
import secrets
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.coupon import Coupon, CouponRedemption


def round_curr(val: Decimal) -> Decimal:
    """Round currency to 2 decimal places."""
    return Decimal(str(val)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def validate_coupon(
    db: Session,
    code: str,
    customer_id: uuid.UUID,
    subtotal: Decimal,
    category: Optional[str] = None,
    service_id: Optional[uuid.UUID] = None,
    service_ids: Optional[List[uuid.UUID]] = None,
) -> Tuple[bool, str, Decimal, Optional[Coupon]]:
    """
    Validate a coupon code and calculate server-side discount amount.
    Returns (is_valid, message, discount_amount, coupon_object).
    """
    if not code or not code.strip():
        return False, "Coupon code cannot be empty.", Decimal("0.00"), None

    code_norm = code.strip().upper()
    now_utc = datetime.now(timezone.utc)

    coupon = db.query(Coupon).filter(Coupon.code == code_norm).first()
    if not coupon:
        return False, f"Coupon code '{code_norm}' is invalid or does not exist.", Decimal("0.00"), None

    if not coupon.is_active:
        return False, f"Coupon '{code_norm}' is no longer active.", Decimal("0.00"), None

    # Check validity window
    if coupon.valid_from and now_utc < (coupon.valid_from if coupon.valid_from.tzinfo else coupon.valid_from.replace(tzinfo=timezone.utc)):
        return False, f"Coupon '{code_norm}' is not yet valid.", Decimal("0.00"), None

    if coupon.valid_until and now_utc > (coupon.valid_until if coupon.valid_until.tzinfo else coupon.valid_until.replace(tzinfo=timezone.utc)):
        return False, f"Coupon '{code_norm}' expired on {coupon.valid_until.strftime('%d %b %Y')}.", Decimal("0.00"), None

    # Customer-specific vouchers (e.g., spin rewards)
    if coupon.customer_id and coupon.customer_id != customer_id:
        return False, "This promotional coupon belongs to another customer account.", Decimal("0.00"), None

    # Check minimum order amount
    subtotal_dec = Decimal(str(subtotal))
    if subtotal_dec < coupon.min_order_amount:
        return (
            False,
            f"Minimum order amount of ₹{coupon.min_order_amount:.0f} is required to apply coupon '{code_norm}'. Current order: ₹{subtotal_dec:.2f}.",
            Decimal("0.00"),
            None,
        )

    # Check category restrictions
    if coupon.applicable_categories:
        cat_lower = (category or "").lower()
        allowed_cats = [c.lower() for c in coupon.applicable_categories]
        if cat_lower and not any(ac in cat_lower for ac in allowed_cats):
            return False, f"Coupon '{code_norm}' is only applicable for categories: {', '.join(coupon.applicable_categories)}.", Decimal("0.00"), None

    # Check service restrictions
    if coupon.applicable_services:
        check_ids = [str(service_id)] if service_id else ([str(sid) for sid in service_ids] if service_ids else [])
        if check_ids and not any(sid in coupon.applicable_services for sid in check_ids):
            return False, f"Coupon '{code_norm}' is not applicable to the selected service(s).", Decimal("0.00"), None

    # Check global usage limit
    if coupon.max_uses is not None:
        total_redemptions = db.query(func.count(CouponRedemption.id)).filter(CouponRedemption.coupon_id == coupon.id).scalar() or 0
        if total_redemptions >= coupon.max_uses:
            return False, f"Coupon '{code_norm}' has reached its maximum global usage limit.", Decimal("0.00"), None

    # Check per-customer usage limit
    customer_redemptions = (
        db.query(func.count(CouponRedemption.id))
        .filter(CouponRedemption.coupon_id == coupon.id, CouponRedemption.customer_id == customer_id)
        .scalar()
        or 0
    )
    if customer_redemptions >= coupon.max_uses_per_customer:
        return False, f"You have already redeemed coupon '{code_norm}' (limit {coupon.max_uses_per_customer} use per account).", Decimal("0.00"), None

    # Calculate discount
    discount = Decimal("0.00")
    if coupon.discount_type.upper() == "PERCENTAGE":
        raw_discount = round_curr(subtotal_dec * (coupon.discount_value / Decimal("100.00")))
        if coupon.max_discount_amount is not None:
            discount = min(raw_discount, coupon.max_discount_amount)
        else:
            discount = raw_discount
    else:  # FIXED
        discount = min(coupon.discount_value, subtotal_dec)

    # Ensure discount does not exceed subtotal
    discount = min(discount, subtotal_dec)
    return True, f"Coupon '{code_norm}' applied successfully! Savings: ₹{discount:.2f}", discount, coupon


def redeem_coupon(
    db: Session,
    coupon_id: uuid.UUID,
    customer_id: uuid.UUID,
    subtotal: Decimal,
    booking_id: Optional[uuid.UUID] = None,
    combined_booking_id: Optional[uuid.UUID] = None,
    category: Optional[str] = None,
    service_id: Optional[uuid.UUID] = None,
    service_ids: Optional[List[uuid.UUID]] = None,
) -> Tuple[bool, str, Decimal, Optional[CouponRedemption]]:
    """
    Safely redeem a coupon within a database transaction using row-level locking.
    Recalculates discount server-side and writes CouponRedemption audit record.
    """
    # Acquire row-level lock on coupon
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).with_for_update().first()
    if not coupon:
        return False, "Coupon not found.", Decimal("0.00"), None

    is_valid, msg, discount, _ = validate_coupon(
        db=db,
        code=coupon.code,
        customer_id=customer_id,
        subtotal=subtotal,
        category=category,
        service_id=service_id,
        service_ids=service_ids,
    )
    if not is_valid:
        return False, msg, Decimal("0.00"), None

    subtotal_dec = Decimal(str(subtotal))
    final_amount = max(Decimal("0.00"), subtotal_dec - discount)

    redemption = CouponRedemption(
        id=uuid.uuid4(),
        coupon_id=coupon.id,
        customer_id=customer_id,
        booking_id=booking_id,
        combined_booking_id=combined_booking_id,
        discount_applied=discount,
        order_amount_before_discount=subtotal_dec,
        final_amount=final_amount,
        redeemed_at=datetime.now(timezone.utc),
    )
    db.add(redemption)
    db.commit()
    db.refresh(redemption)
    return True, f"Coupon '{coupon.code}' redeemed successfully.", discount, redemption


def mint_spin_reward_coupon(
    db: Session,
    customer_id: uuid.UUID,
    reward_tier: Optional[str] = "SERVE75",
) -> Coupon:
    """
    Mint an authenticated, tamper-proof coupon record for a spin-the-wheel reward.
    Produced coupons are unique per spin, tied directly to the customer, and expire in 30 days.
    """
    tier = (reward_tier or "SERVE75").upper().strip()

    if tier == "SERVE100":
        discount_type = "FIXED"
        discount_val = Decimal("100.00")
        min_order = Decimal("399.00")
        max_disc = None
        desc = "Spin & Win Reward: ₹100 OFF on next booking"
        code_prefix = "SPIN100"
    elif tier == "SERVE20PCT":
        discount_type = "PERCENTAGE"
        discount_val = Decimal("20.00")
        min_order = Decimal("499.00")
        max_disc = Decimal("200.00")
        desc = "Spin & Win Reward: 20% OFF (up to ₹200) on next booking"
        code_prefix = "SPIN20"
    elif tier == "SERVE50":
        discount_type = "FIXED"
        discount_val = Decimal("50.00")
        min_order = Decimal("299.00")
        max_disc = None
        desc = "Spin & Win Reward: ₹50 OFF on next booking"
        code_prefix = "SPIN50"
    else:  # Default SERVE75
        discount_type = "FIXED"
        discount_val = Decimal("75.00")
        min_order = Decimal("349.00")
        max_disc = None
        desc = "Spin & Win Reward: ₹75 OFF on next booking"
        code_prefix = "SPIN75"

    random_suffix = secrets.token_hex(2).upper()
    unique_code = f"{code_prefix}-{random_suffix}"

    now_utc = datetime.now(timezone.utc)
    coupon = Coupon(
        id=uuid.uuid4(),
        code=unique_code,
        description=desc,
        discount_type=discount_type,
        discount_value=discount_val,
        max_discount_amount=max_disc,
        min_order_amount=min_order,
        is_active=True,
        valid_from=now_utc,
        valid_until=now_utc + timedelta(days=30),
        max_uses=1,
        max_uses_per_customer=1,
        is_spin_reward=True,
        customer_id=customer_id,
    )
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon

