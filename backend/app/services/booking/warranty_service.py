import uuid
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session

from app.models.customer import Booking, BookingWarranty
from app.models.service import Service

# Predefined minimal platform/service fee for warranty claims (INR)
DEFAULT_WARRANTY_NOMINAL_FEE = 49.0

# Ineligible categories (consumables, personal grooming, salon/beauty)
EXCLUDED_CATEGORIES = {
    "beauty",
    "salon",
    "parlour",
    "spa",
    "women's spa",
    "men's salon",
    "personal care",
    "massage",
}

# 15-day coverage categories (critical home maintenance & core infrastructure)
FIFTEEN_DAY_CATEGORIES = {
    "plumbing",
    "electrical",
    "electrician",
    "plumber",
}

# 10-day coverage categories (carpentry, painting, appliances)
TEN_DAY_CATEGORIES = {
    "carpentry",
    "carpenter",
    "painting",
    "painter",
    "appliance repair",
    "ac & appliance repair",
    "ac repair",
}


def get_warranty_policy(category: Optional[str], service_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Determine warranty eligibility, duration (10-15 days), terms, and fee.
    Excludes beauty/parlour/salon services.
    """
    cat_norm = (category or "").lower().strip()
    srv_norm = (service_name or "").lower().strip()

    # 1. Check exclusions
    for exc in EXCLUDED_CATEGORIES:
        if exc in cat_norm or exc in srv_norm:
            return {
                "is_eligible": False,
                "duration_days": 0,
                "nominal_fee": 0.0,
                "policy_tier": "Excluded",
                "badge_label": "Warranty Not Applicable",
                "terms": "Personal grooming, salon, beauty, and consumable treatments are excluded from home maintenance warranty.",
            }

    # 2. Check 15-day critical infrastructure
    for fifteen in FIFTEEN_DAY_CATEGORIES:
        if fifteen in cat_norm or fifteen in srv_norm:
            return {
                "is_eligible": True,
                "duration_days": 15,
                "nominal_fee": DEFAULT_WARRANTY_NOMINAL_FEE,
                "policy_tier": "15-Day Premium Guarantee",
                "badge_label": "15-Day Quality Guarantee",
                "terms": "Covers pipe leakages, wiring faults, installation defects, and joint failures under standard residential usage for 15 days.",
            }

    # 3. Check 10-day maintenance & appliances
    for ten in TEN_DAY_CATEGORIES:
        if ten in cat_norm or ten in srv_norm:
            return {
                "is_eligible": True,
                "duration_days": 10,
                "nominal_fee": DEFAULT_WARRANTY_NOMINAL_FEE,
                "policy_tier": "10-Day Standard Guarantee",
                "badge_label": "10-Day Quality Guarantee",
                "terms": "Covers carpentry joints, surface peelings, and technical workmanship for 10 days.",
            }

    # Default fallback for home maintenance services: 10 days
    return {
        "is_eligible": True,
        "duration_days": 10,
        "nominal_fee": DEFAULT_WARRANTY_NOMINAL_FEE,
        "policy_tier": "10-Day Standard Guarantee",
        "badge_label": "10-Day Quality Guarantee",
        "terms": "Covers workmanship and installation defects for 10 days from service completion.",
    }


def issue_booking_warranty(
    booking: Booking,
    db: Session,
    base_time: Optional[datetime] = None,
) -> Optional[BookingWarranty]:
    """
    Issue a digital warranty card for eligible home maintenance services upon completion.
    Respects category-specific 10-15 day durations and excludes salon/beauty.
    """
    category = getattr(booking, "category", None)
    service_name = getattr(booking, "service_name", None)

    # If category not on booking, try to fetch from Service record
    if not category and booking.service_id:
        srv = db.query(Service).filter(Service.id == booking.service_id).first()
        if srv:
            category = srv.category
            if not service_name:
                service_name = srv.name

    policy = get_warranty_policy(category, service_name)
    if not policy["is_eligible"]:
        return None

    now_utc = base_time or datetime.now(timezone.utc)
    duration_days = policy["duration_days"]

    # Check if already issued
    existing = db.query(BookingWarranty).filter(BookingWarranty.booking_id == booking.id).first()
    if existing:
        return existing

    warranty = BookingWarranty(
        id=uuid.uuid4(),
        booking_id=booking.id,
        customer_id=booking.customer_id,
        provider_id=booking.provider_id,
        service_name=service_name or "Home Maintenance Service",
        issued_at=now_utc,
        expires_at=now_utc + timedelta(days=duration_days),
        is_active=True,
        claim_status="None",
    )
    db.add(warranty)
    db.commit()
    db.refresh(warranty)
    return warranty


def validate_warranty_claim(
    warranty: Optional[BookingWarranty],
    category: Optional[str] = None,
    service_name: Optional[str] = None,
) -> Tuple[bool, str, float]:
    """
    Validate whether a warranty claim can be raised.
    Returns (is_valid, message, nominal_fee).
    """
    if not warranty:
        return False, "No active warranty record found for this service.", 0.0

    policy = get_warranty_policy(category, service_name or warranty.service_name)
    if not policy["is_eligible"]:
        return False, policy["terms"], 0.0

    now_utc = datetime.now(timezone.utc)
    exp = warranty.expires_at
    if exp and exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)

    if exp and now_utc > exp:
        return False, f"Warranty expired on {exp.strftime('%d %b %Y')}. Claims cannot be accepted after expiry.", 0.0

    if warranty.claim_status == "Pending":
        return False, "A warranty claim is already pending inspection for this booking.", policy["nominal_fee"]

    if warranty.claim_status == "Resolved":
        return False, "A warranty claim for this booking has already been resolved and fulfilled.", policy["nominal_fee"]

    return True, "Warranty claim eligible.", policy["nominal_fee"]
