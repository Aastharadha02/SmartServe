import uuid
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session

from app.models.customer import Booking, BookingWarranty
from app.models.service import Service

# Standardized 7-day platform warranty duration for eligible home services
DEFAULT_WARRANTY_DAYS = 7

# Zero nominal fee: warranty rework is 100% free with no unapproved inspection charges
DEFAULT_WARRANTY_NOMINAL_FEE = 0.0

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

# Recognized eligible home service categories (plumbing, electrical, carpentry, painting, appliances, cleaning)
ELIGIBLE_HOME_CATEGORIES = {
    "plumbing",
    "electrical",
    "electrician",
    "plumber",
    "carpentry",
    "carpenter",
    "painting",
    "painter",
    "appliance repair",
    "ac & appliance repair",
    "ac repair",
    "cleaning",
    "deep cleaning",
    "home maintenance",
    "handyman",
}


def get_warranty_policy(category: Optional[str], service_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Determine warranty eligibility, standardized 7-day duration, terms, and fee.
    Excludes beauty/parlour/salon services.
    All eligible home maintenance services receive a consistent 7-day guarantee with zero fees.
    """
    cat_norm = (category or "").lower().strip()
    srv_norm = (service_name or "").lower().strip()

    # 1. Check exclusions (personal grooming, salon, beauty)
    for exc in EXCLUDED_CATEGORIES:
        if exc in cat_norm or exc in srv_norm:
            return {
                "is_eligible": False,
                "duration_days": 0,
                "nominal_fee": 0.0,
                "policy_tier": "Excluded",
                "badge_label": "Warranty Not Applicable",
                "terms": "Personal grooming, salon, beauty, and consumable treatments are excluded from the 7-day home service warranty.",
            }

    # 2. Standardized 7-day quality guarantee for all eligible home services
    return {
        "is_eligible": True,
        "duration_days": DEFAULT_WARRANTY_DAYS,
        "nominal_fee": DEFAULT_WARRANTY_NOMINAL_FEE,
        "policy_tier": "7-Day Quality Guarantee",
        "badge_label": "7-Day Quality Guarantee",
        "terms": "Covers workmanship and installation defects for 7 days from service completion. 100% free rework labor with zero additional inspection charges.",
    }


def get_service_completion_time(booking: Booking, base_time: Optional[datetime] = None) -> datetime:
    """
    Determine the exact service completion timestamp from booking timeline or updated_at.
    """
    if base_time:
        return base_time if base_time.tzinfo else base_time.replace(tzinfo=timezone.utc)

    # Search timeline in reverse for the completion event timestamp
    if booking.timeline and isinstance(booking.timeline, list):
        for event in reversed(booking.timeline):
            if isinstance(event, dict):
                ev_name = str(event.get("event") or "").lower()
                ev_status = str(event.get("status") or "").lower()
                if "completed" in ev_name or "completed" in ev_status or "completion otp verified" in ev_name:
                    ts_str = event.get("timestamp")
                    if ts_str:
                        try:
                            clean_ts = ts_str.replace("Z", "+00:00")
                            dt = datetime.fromisoformat(clean_ts)
                            return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
                        except Exception:
                            pass

    # Fallback to updated_at if booking is completed
    if str(booking.status).lower() in ["completed", "paid"] and booking.updated_at:
        dt = booking.updated_at
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)

    return datetime.now(timezone.utc)


def issue_booking_warranty(
    booking: Booking,
    db: Session,
    base_time: Optional[datetime] = None,
) -> Optional[BookingWarranty]:
    """
    Issue a digital warranty card for eligible home maintenance services upon completion.
    Standardized to a consistent 7-day duration calculated from service completion.
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

    completion_time = get_service_completion_time(booking, base_time)
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
        issued_at=completion_time,
        expires_at=completion_time + timedelta(days=duration_days),
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
        return False, f"Warranty expired on {exp.strftime('%d %b %Y')}. Claims cannot be accepted after the 7-day warranty period.", 0.0

    if warranty.claim_status == "Pending":
        return False, "A warranty claim is already pending inspection for this booking.", 0.0

    if warranty.claim_status == "Resolved":
        return False, "A warranty claim for this booking has already been resolved and fulfilled.", 0.0

    return True, "Warranty claim eligible.", 0.0
