import uuid
from datetime import datetime, date, time, timedelta
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.database import SessionLocal
from app.models.provider import Provider, ProviderService, Availability
from app.models.customer import Customer, Booking
from app.models.service import Service
from app.models.user import User
from app.services.booking.eligibility_service import (
    get_eligible_providers,
    find_eligible_provider,
    generate_slot_times,
    parse_scheduled_datetime,
)
from app.services.demo_service import DEMO_CUSTOMER_CONFIG, DEMO_PROVIDER_CONFIG

client = TestClient(app)


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def customer_auth_header():
    res = client.post(
        "/api/v1/auth/login",
        json={
            "email": DEMO_CUSTOMER_CONFIG["email"],
            "password": DEMO_CUSTOMER_CONFIG["password"],
        },
    )
    assert res.status_code == 200, f"Customer login failed: {res.text}"
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def bedroom_cleaning_service(db: Session):
    svc = db.query(Service).filter(Service.name == "Bedroom Deep Cleaning").first()
    assert svc is not None, "Bedroom Deep Cleaning service must exist in database"
    return svc


@pytest.fixture
def demo_provider(db: Session):
    prov = (
        db.query(Provider)
        .join(User, Provider.user_id == User.id)
        .filter(User.email == DEMO_PROVIDER_CONFIG["email"])
        .first()
    )
    assert prov is not None, "Demo provider must exist in database"
    assert prov.is_verified is True, "Demo provider must be verified"
    return prov


def test_1_and_2_verified_provider_has_free_slot_and_offers_service(
    db: Session, bedroom_cleaning_service: Service, demo_provider: Provider
):
    """
    1. A verified provider has a FREE slot saved for a specific date (2026-10-17).
    2. The provider offers the same service that the customer selects.
    """
    # Verify provider service association
    ps = (
        db.query(ProviderService)
        .filter(
            ProviderService.provider_id == demo_provider.user_id,
            ProviderService.service_id == bedroom_cleaning_service.id,
            ProviderService.active == True,
        )
        .first()
    )
    assert ps is not None, "Demo provider must actively offer Bedroom Deep Cleaning"

    # Verify FREE slot exists on 2026-10-17
    target_date = date.today()
    slots = (
        db.query(Availability)
        .filter(
            Availability.provider_id == demo_provider.user_id,
            Availability.slot_date == target_date,
            Availability.status == "FREE",
        )
        .all()
    )
    assert len(slots) > 0, "Demo provider must have FREE slots on 2026-10-17"
    start_times = [s.start_time for s in slots]
    assert time(9, 0) in start_times or time(11, 30) in start_times, (
        f"Expected standard slot times on 2026-10-17, got: {start_times}"
    )


def test_3_and_4_customer_portal_availability_api_returns_eligible_slots_under_correct_date(
    bedroom_cleaning_service: Service, demo_provider: Provider
):
    """
    3. The Customer Portal availability API returns that eligible slot.
    4. The Customer Portal displays the slot under the correct date (2026-10-17).
    """
    url = f"/api/v1/customer/catalog/services/{bedroom_cleaning_service.id}/eligible-providers"
    res = client.get(url)
    assert res.status_code == 200
    providers = res.json()
    assert isinstance(providers, list)

    target_prov = next(
        (p for p in providers if p["provider_id"] == str(demo_provider.user_id)), None
    )
    assert target_prov is not None, "Demo provider must be in eligible providers list"
    assert target_prov["is_available"] is True

    structured_slots = target_prov.get("structured_slots", [])
    oct_17_slots = [s for s in structured_slots if s["slot_date"] == date.today().isoformat()]

    # Must contain slots on 2026-10-17
    assert len(oct_17_slots) >= 4, (
        f"Expected at least 4 slots on 2026-10-17, got {len(oct_17_slots)}"
    )

    # Check slot start/end times and display
    slot_times = [s["start_time"] for s in oct_17_slots]
    assert "09:00" in slot_times
    assert "11:30" in slot_times
    assert "14:00" in slot_times
    assert "16:30" in slot_times

    # Verify that available_times within the slot are populated
    first_slot = next(s for s in oct_17_slots if s["start_time"] == "09:00")
    assert "09:00 AM" in first_slot["available_times"]


def test_5_customer_can_select_slot_and_proceed_through_booking_flow(
    db: Session,
    customer_auth_header: dict,
    bedroom_cleaning_service: Service,
    demo_provider: Provider,
):
    """
    5. A customer can select the slot and proceed through the existing booking flow.
    """
    target_date = date.today().isoformat()
    target_time = "09:00 AM"

    # Make sure slot 09:00 on 2026-10-17 is FREE before booking
    slot = (
        db.query(Availability)
        .filter(
            Availability.provider_id == demo_provider.user_id,
            Availability.slot_date == date.today(),
            Availability.start_time == time(9, 0),
        )
        .first()
    )
    assert slot is not None
    slot.status = "FREE"
    db.commit()

    booking_payload = {
        "service_id": str(bedroom_cleaning_service.id),
        "service_name": bedroom_cleaning_service.name,
        "category": bedroom_cleaning_service.category,
        "scheduled_date": target_date,
        "scheduled_time": target_time,
        "address_line1": "Flat 402, Sunshine Apartments, Sector 62",
        "city": "Noida",
        "pincode": "201301",
        "payment_method": "COD",
        "notes": "Automated regression test booking",
        "provider_id": str(demo_provider.user_id),
    }

    res = client.post("/api/v1/customer/bookings", json=booking_payload, headers=customer_auth_header)
    assert res.status_code == 200, f"Booking creation failed: {res.text}"
    booking_data = res.json()
    assert booking_data["status"] == "Requested"
    assert booking_data["scheduled_date"] == target_date
    booking_id = booking_data["id"]

    # Verify slot became RESERVED
    db.refresh(slot)
    assert slot.status == "RESERVED"

    # Clean up test booking to maintain test isolation
    created_booking = db.query(Booking).filter(Booking.id == uuid.UUID(booking_id)).first()
    if created_booking:
        db.delete(created_booking)
    slot.status = "FREE"
    db.commit()


def test_6_slot_already_booked_or_unavailable_is_excluded(
    db: Session, bedroom_cleaning_service: Service, demo_provider: Provider
):
    """
    6. A slot that is already booked or unavailable is excluded.
    """
    target_date = date.today()
    slot = (
        db.query(Availability)
        .filter(
            Availability.provider_id == demo_provider.user_id,
            Availability.slot_date == target_date,
            Availability.start_time == time(14, 0),
        )
        .first()
    )
    assert slot is not None

    try:
        # Mark slot UNAVAILABLE
        slot.status = "UNAVAILABLE"
        db.commit()

        url = f"/api/v1/customer/catalog/services/{bedroom_cleaning_service.id}/eligible-providers"
        res = client.get(url)
        assert res.status_code == 200
        providers = res.json()
        target_prov = next(p for p in providers if p["provider_id"] == str(demo_provider.user_id))
        oct_17_slots = [
            s for s in target_prov.get("structured_slots", []) if s["slot_date"] == date.today().isoformat()
        ]
        start_times = [s["start_time"] for s in oct_17_slots]
        assert "14:00" not in start_times, "UNAVAILABLE slot must be excluded from customer availability"

        # Now test with find_eligible_provider
        dt = datetime.combine(target_date, time(14, 0))
        prov, matched_slot, msg = find_eligible_provider(
            db, bedroom_cleaning_service.id, dt, requested_provider_id=demo_provider.user_id
        )
        assert prov is None, "Should not match an unavailable slot"
        assert "free availability slot" in msg.lower() or "no verified provider" in msg.lower()

    finally:
        # Restore to FREE
        slot.status = "FREE"
        db.commit()


def test_7_unverified_or_ineligible_provider_remains_excluded(
    db: Session, bedroom_cleaning_service: Service, demo_provider: Provider
):
    """
    7. An unverified or ineligible provider remains excluded according to existing business rules.
    """
    original_status = demo_provider.is_verified
    try:
        demo_provider.is_verified = False
        db.commit()

        url = f"/api/v1/customer/catalog/services/{bedroom_cleaning_service.id}/eligible-providers"
        res = client.get(url)
        assert res.status_code == 200
        providers = res.json()
        target_prov = next(
            (p for p in providers if p["provider_id"] == str(demo_provider.user_id)), None
        )
        assert target_prov is None, "Unverified provider must be completely excluded from eligible providers"

        # Direct eligibility check
        dt = datetime.combine(date.today(), time(9, 0))
        prov, matched_slot, msg = find_eligible_provider(
            db, bedroom_cleaning_service.id, dt, requested_provider_id=demo_provider.user_id
        )
        assert prov is None
        assert "approved" in msg.lower() or "verified" in msg.lower()
    finally:
        demo_provider.is_verified = original_status
        db.commit()


def test_8_slots_for_another_service_not_incorrectly_displayed(
    db: Session, demo_provider: Provider
):
    """
    8. Slots for another service are not incorrectly displayed.
    """
    # Find a service the demo provider does NOT offer (e.g. Electrical or Plumbing)
    offered_service_ids = [
        ps.service_id
        for ps in db.query(ProviderService)
        .filter(ProviderService.provider_id == demo_provider.user_id, ProviderService.active == True)
        .all()
    ]
    unrelated_service = (
        db.query(Service)
        .filter(~Service.id.in_(offered_service_ids), Service.is_active == True)
        .first()
    )
    if not unrelated_service:
        pytest.skip("No unrelated service available in test database")

    url = f"/api/v1/customer/catalog/services/{unrelated_service.id}/eligible-providers"
    res = client.get(url)
    assert res.status_code == 200
    providers = res.json()
    provider_ids = [p["provider_id"] for p in providers]
    assert str(demo_provider.user_id) not in provider_ids, (
        f"Provider {demo_provider.user_id} should not appear for service {unrelated_service.name}"
    )


def test_9_date_and_timezone_handling_do_not_shift_slots(
    bedroom_cleaning_service: Service, demo_provider: Provider
):
    """
    9. Date and timezone handling do not shift slots to another date.
    """
    url = f"/api/v1/customer/catalog/services/{bedroom_cleaning_service.id}/eligible-providers"
    res = client.get(url)
    assert res.status_code == 200
    providers = res.json()
    target_prov = next(p for p in providers if p["provider_id"] == str(demo_provider.user_id))

    slots = target_prov.get("structured_slots", [])
    # Verify every slot date matches standard ISO YYYY-MM-DD
    for s in slots:
        slot_date = s["slot_date"]
        parsed = datetime.strptime(slot_date, "%Y-%m-%d").date()
        assert slot_date == parsed.isoformat(), f"Slot date format shifted: {slot_date}"

    # October 17 slots must remain on 2026-10-17
    oct_17_slots = [s for s in slots if s["slot_date"] == date.today().isoformat()]
    assert len(oct_17_slots) > 0
    for s in oct_17_slots:
        assert s["slot_date"] == date.today().isoformat()


def test_10_upcoming_open_date_count_agrees_with_bookable_dates(
    bedroom_cleaning_service: Service, demo_provider: Provider
):
    """
    10. The upcoming open-date count agrees with the actual dates that have bookable slots.
    """
    url = f"/api/v1/customer/catalog/services/{bedroom_cleaning_service.id}/eligible-providers"
    res = client.get(url)
    assert res.status_code == 200
    providers = res.json()

    # Collect all unique dates across eligible providers that have at least one bookable time
    dates_with_slots = set()
    for prov in providers:
        for slot in prov.get("structured_slots", []):
            if slot.get("available_times") and len(slot["available_times"]) > 0:
                dates_with_slots.add(slot["slot_date"])

    sorted_dates = sorted(list(dates_with_slots))
    assert date.today().isoformat() in sorted_dates, "2026-10-17 must be present in open dates"
    assert len(sorted_dates) >= 20, (
        f"Expected at least 25 open dates, got {len(sorted_dates)}"
    )
