import uuid
from datetime import datetime, date, time, timedelta
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.provider import Provider, ProviderService, Availability
from app.models.customer import Booking
from app.models.user import User


def parse_scheduled_datetime(scheduled_date: str, scheduled_time: str) -> datetime:
    """
    Robustly parse scheduled date and time into a datetime object.
    Supports ISO formats, 12-hour AM/PM formats, and standard variations.
    """
    cleaned_date = str(scheduled_date).strip()
    cleaned_time = str(scheduled_time).strip()

    combos = [
        f"{cleaned_date} {cleaned_time}",
        f"{cleaned_date}T{cleaned_time}",
    ]
    formats = [
        "%Y-%m-%d %I:%M %p",
        "%Y-%m-%d %I:%M%p",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M",
        "%d/%m/%Y %I:%M %p",
        "%d-%m-%Y %I:%M %p",
    ]
    for combo in combos:
        for fmt in formats:
            try:
                return datetime.strptime(combo, fmt)
            except ValueError:
                continue

    # Fallback to date only with 10:00 AM default
    try:
        parsed_d = datetime.strptime(cleaned_date, "%Y-%m-%d").date()
        return datetime.combine(parsed_d, time(10, 0))
    except Exception:
        return datetime.utcnow()


def generate_slot_times(slot: Availability, active_bookings: List[Booking]) -> List[str]:
    """
    Generate non-conflicting time intervals within a provider's availability window.
    Strictly filters out past dates and active booking overlaps.
    """
    slot_date = slot.slot_date
    if slot_date < date.today():
        return []

    curr_hour = slot.start_time.hour
    curr_min = slot.start_time.minute
    end_hour = slot.end_time.hour
    end_min = slot.end_time.minute

    total_start_mins = curr_hour * 60 + curr_min
    total_end_mins = end_hour * 60 + end_min

    if total_end_mins <= total_start_mins:
        return []

    # Generate candidate time points (every 2 hours, or hourly if window is small)
    step_mins = 60 if (total_end_mins - total_start_mins) <= 180 else 120
    candidates = []
    t = total_start_mins
    while t < total_end_mins:
        h = t // 60
        m = t % 60
        candidates.append(time(h, m))
        t += step_mins

    valid_times = []
    for cand in candidates:
        cand_dt = datetime.combine(slot_date, cand)

        # Conflict check against active bookings (60-minute window)
        has_conflict = False
        for b in active_bookings:
            if not b.scheduled_time:
                continue
            b_dt = b.scheduled_time
            if hasattr(b_dt, "tzinfo") and b_dt.tzinfo is not None:
                b_dt = b_dt.replace(tzinfo=None)
            diff_secs = abs((b_dt - cand_dt).total_seconds())
            if diff_secs < 3600:
                has_conflict = True
                break

        if not has_conflict:
            valid_times.append(cand.strftime("%I:%M %p"))

    return valid_times


def find_eligible_provider(
    db: Session,
    service_id: uuid.UUID,
    scheduled_datetime: datetime,
    requested_provider_id: Optional[uuid.UUID] = None,
) -> Tuple[Optional[Provider], Optional[Availability], str]:
    """
    Determine the most eligible provider for a requested service and time slot.

    Strict eligibility rules:
    1. Past Date Guard: Requested date must not be in the past (before today).
    2. Service Association: Provider must actively offer the specific catalog service.
    3. Verification & Active Status: Provider must be approved (is_verified == True) and user account active.
    4. Availability Window: Provider must have an active, FREE slot covering requested date and time.
    5. Conflict Prevention: Provider must not have an active booking overlapping the requested slot.
    """
    check_dt = scheduled_datetime
    if hasattr(check_dt, "tzinfo") and check_dt.tzinfo is not None:
        check_dt = check_dt.replace(tzinfo=None)

    req_date = check_dt.date()
    req_time = check_dt.time()

    if req_date < date.today():
        return None, None, "Cannot schedule a booking in the past. Please select an upcoming date and time."

    # Step 1: Filter by Service Association
    active_services = (
        db.query(ProviderService)
        .filter(
            ProviderService.service_id == service_id,
            ProviderService.active == True
        )
        .all()
    )
    if not active_services:
        return None, None, "No active provider offers this catalog service"

    associated_provider_ids = [ps.provider_id for ps in active_services]
    if requested_provider_id and requested_provider_id not in associated_provider_ids:
        return None, None, "The selected provider does not offer this specific catalog service"

    # Step 2: Filter by Approved / Verified Status AND Active User Status
    verified_providers = (
        db.query(Provider)
        .join(User, Provider.user_id == User.id)
        .filter(
            Provider.user_id.in_(associated_provider_ids),
            Provider.is_verified == True,
            User.is_active == True,
        )
        .all()
    )
    if not verified_providers:
        return None, None, "No verified, approved providers currently offer this catalog service"

    verified_ids = [p.user_id for p in verified_providers]
    if requested_provider_id and requested_provider_id not in verified_ids:
        return None, None, "The selected provider is not currently approved and verified by admin"

    # Step 3: Filter by Availability Slot (Matching Requested Date & Time)
    matching_slots = (
        db.query(Availability)
        .filter(
            Availability.provider_id.in_(verified_ids),
            Availability.slot_date == req_date,
            Availability.start_time <= req_time,
            Availability.end_time >= req_time,
            func.upper(Availability.status) == "FREE"
        )
        .all()
    )
    if not matching_slots:
        return None, None, f"No verified provider has an available free slot on {req_date} at {req_time.strftime('%I:%M %p')}"

    # Map provider to their matching slot
    provider_slot_map = {slot.provider_id: slot for slot in matching_slots}
    available_providers = [p for p in verified_providers if p.user_id in provider_slot_map]

    if requested_provider_id and requested_provider_id not in provider_slot_map:
        return None, None, f"The selected provider does not have a free availability slot on {req_date} at {req_time.strftime('%I:%M %p')}"

    # Step 4: Conflict Check (Exclude providers with an existing booking overlapping this window)
    eligible_candidates = []
    for prov in available_providers:
        conflicting_booking = (
            db.query(Booking)
            .filter(
                Booking.provider_id == prov.user_id,
                Booking.status.in_(["Requested", "Assigned", "Accepted", "Started"]),
                Booking.scheduled_time.isnot(None),
                func.abs(func.extract("epoch", Booking.scheduled_time - scheduled_datetime)) < 3600
            )
            .first()
        )
        if not conflicting_booking:
            eligible_candidates.append(prov)

    if not eligible_candidates:
        return None, None, "All available providers have conflicting booking commitments for this slot"

    # If customer selected a specific provider, confirm they are conflict-free
    if requested_provider_id:
        chosen = next((p for p in eligible_candidates if p.user_id == requested_provider_id), None)
        if not chosen:
            return None, None, "The selected provider has an active conflicting booking at this scheduled time"
        matched_slot = provider_slot_map.get(chosen.user_id)
        return chosen, matched_slot, "Selected provider assigned"

    # Step 5: Auto-assign best candidate (highest reliability score, acceptance rate)
    eligible_candidates.sort(
        key=lambda p: (
            float(p.reliability_score or 100.0),
            float(p.acceptance_rate or 100.0),
            float(p.experience_years or 0)
        ),
        reverse=True
    )

    selected_provider = eligible_candidates[0]
    matched_slot = provider_slot_map.get(selected_provider.user_id)
    return selected_provider, matched_slot, "Eligible provider assigned"


def get_eligible_providers(
    db: Session,
    service_id: uuid.UUID,
) -> List[dict]:
    """
    Retrieve all verified providers offering this service with their skills,
    metrics, and genuine upcoming non-conflicting availability slots.
    Never exposes past, reserved, or conflicting slots.
    """
    active_services = (
        db.query(ProviderService)
        .filter(
            ProviderService.service_id == service_id,
            ProviderService.active == True
        )
        .all()
    )
    if not active_services:
        return []

    associated_provider_ids = [ps.provider_id for ps in active_services]
    verified_providers = (
        db.query(Provider)
        .join(User, Provider.user_id == User.id)
        .filter(
            Provider.user_id.in_(associated_provider_ids),
            Provider.is_verified == True,
            User.is_active == True,
        )
        .all()
    )

    today = date.today()
    results = []
    for p in verified_providers:
        # Get active bookings for conflict checking
        active_bookings = (
            db.query(Booking)
            .filter(
                Booking.provider_id == p.user_id,
                Booking.status.in_(["Requested", "Assigned", "Accepted", "Started"]),
                Booking.scheduled_time.isnot(None),
            )
            .all()
        )

        # Get upcoming free slots for provider
        slots = (
            db.query(Availability)
            .filter(
                Availability.provider_id == p.user_id,
                func.upper(Availability.status) == "FREE",
                Availability.slot_date >= today,
            )
            .order_by(Availability.slot_date.asc(), Availability.start_time.asc())
            .all()
        )

        structured_slots = []
        slot_list = []

        for s in slots:
            valid_times = generate_slot_times(s, active_bookings)
            if not valid_times:
                continue

            disp_time = f"{s.start_time.strftime('%I:%M %p')} - {s.end_time.strftime('%I:%M %p')}"
            structured_slots.append({
                "slot_id": str(s.id),
                "slot_date": s.slot_date.isoformat(),
                "start_time": s.start_time.strftime("%H:%M"),
                "end_time": s.end_time.strftime("%H:%M"),
                "display_time": disp_time,
                "is_available": True,
                "available_times": valid_times,
            })
            slot_list.append(f"{s.slot_date.isoformat()} ({disp_time})")

        results.append({
            "provider_id": str(p.user_id),
            "full_name": p.full_name,
            "category": p.category,
            "skills": p.skills or "",
            "experience_years": p.experience_years or 0,
            "reliability_score": float(p.reliability_score or 100.0),
            "acceptance_rate": float(p.acceptance_rate or 100.0),
            "service_area": p.service_area or "Citywide",
            "available_slots": slot_list,
            "structured_slots": structured_slots,
            "is_available": len(structured_slots) > 0,
        })

    results.sort(
        key=lambda x: (x["reliability_score"], x["acceptance_rate"], x["experience_years"]),
        reverse=True
    )
    return results

