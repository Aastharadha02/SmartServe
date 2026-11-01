import uuid
from decimal import Decimal
from datetime import datetime, timezone, timedelta
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.database import get_db
from app.models.user import User
from app.models.customer import Customer, Booking, BookingWarranty
from app.models.service import Service
from app.services.booking.warranty_service import (
    get_warranty_policy,
    issue_booking_warranty,
    validate_warranty_claim,
    DEFAULT_WARRANTY_DAYS,
    DEFAULT_WARRANTY_NOMINAL_FEE,
)
from app.core.security import create_access_token

client = TestClient(app)



@pytest.fixture
def db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def warranty_actors(db_session: Session):
    """Create test customer and tokens for warranty testing."""
    user = db_session.query(User).filter(User.email == "warranty_cust@smartserve.com").first()
    if not user:
        user = User(
            id=uuid.uuid4(),
            email="warranty_cust@smartserve.com",
            hashed_password="TestPassword123!",
            role="customer",
            is_active=True,
            
        )
        db_session.add(user)
        db_session.commit()

    customer = db_session.query(Customer).filter(Customer.user_id == user.id).first()
    if not customer:
        customer = Customer(
            id=uuid.uuid4(),
            user_id=user.id,
            full_name="Warranty Test Customer",
            email="warranty_cust@smartserve.com",
            phone="9876543210",
        )
        db_session.add(customer)
        db_session.commit()

    # Another customer to test unauthorized access
    other_user = db_session.query(User).filter(User.email == "other_cust@smartserve.com").first()
    if not other_user:
        other_user = User(
            id=uuid.uuid4(),
            email="other_cust@smartserve.com",
            hashed_password="TestPassword123!",
            role="customer",
            is_active=True,
            
        )
        db_session.add(other_user)
        db_session.commit()

    other_customer = db_session.query(Customer).filter(Customer.user_id == other_user.id).first()
    if not other_customer:
        other_customer = Customer(
            id=uuid.uuid4(),
            user_id=other_user.id,
            full_name="Other Customer",
            email="other_cust@smartserve.com",
            phone="9876543211",
        )
        db_session.add(other_customer)
        db_session.commit()

    token = create_access_token({"sub": user.email, "role": "customer", "user_id": str(user.id)})
    other_token = create_access_token({"sub": other_user.email, "role": "customer", "user_id": str(other_user.id)})

    service = db_session.query(Service).first()
    return {
        "user": user,
        "customer": customer,
        "token": token,
        "other_user": other_user,
        "other_customer": other_customer,
        "other_token": other_token,
        "service_id": service.id if service else uuid.uuid4(),
    }


def test_warranty_policy_standardized_7_days():
    """Verify that all eligible home maintenance services receive a standardized 7-day warranty."""
    # Plumbing
    plumb = get_warranty_policy("Plumbing", "Tap Leak Repair")
    assert plumb["is_eligible"] is True
    assert plumb["duration_days"] == DEFAULT_WARRANTY_DAYS == 7
    assert plumb["nominal_fee"] == 0.0

    # Electrical
    elec = get_warranty_policy("Electrical", "Fan Installation")
    assert elec["is_eligible"] is True
    assert elec["duration_days"] == 7
    assert elec["nominal_fee"] == 0.0

    # Carpentry
    carp = get_warranty_policy("Carpentry", "Door Hinge Fix")
    assert carp["is_eligible"] is True
    assert carp["duration_days"] == 7
    assert carp["nominal_fee"] == 0.0

    # Painting
    paint = get_warranty_policy("Painting", "Waterproofing Touchup")
    assert paint["is_eligible"] is True
    assert paint["duration_days"] == 7
    assert paint["nominal_fee"] == 0.0

    # Cleaning
    cleaning = get_warranty_policy("Cleaning", "Deep Bathroom Cleaning")
    assert cleaning["is_eligible"] is True
    assert cleaning["duration_days"] == 7
    assert cleaning["nominal_fee"] == 0.0


def test_warranty_policy_beauty_salon_exclusions():
    """Verify beauty/salon/spa personal care services are legitimately excluded from warranty."""
    beauty = get_warranty_policy("Salon for Women", "Facial & Glow Cleanup")
    assert beauty["is_eligible"] is False
    assert beauty["duration_days"] == 0
    assert "excluded" in beauty["terms"].lower()

    spa = get_warranty_policy("Personal Care", "Deep Tissue Spa")
    assert spa["is_eligible"] is False
    assert spa["duration_days"] == 0
    assert spa["nominal_fee"] == 0.0


def test_issue_warranty_calculated_from_completion_time(db_session: Session, warranty_actors):
    """Verify 7-day warranty is accurately calculated from the service completion timestamp."""
    completion_ts = datetime.now(timezone.utc) - timedelta(hours=2)

    b = Booking(
        id=uuid.uuid4(),
        booking_reference=f"BK-{uuid.uuid4().hex[:8].upper()}",
        customer_id=warranty_actors["customer"].id,
        service_id=warranty_actors["service_id"],
        category="Plumbing",
        service_name="Bathroom Pipe Fitting",
        status="Completed",
        payment_method="COD",
        payment_status="Paid",
        total_price=Decimal("899.00"),
        timeline=[
            {"event": "Service Completion OTP Verified", "timestamp": completion_ts.isoformat()},
            {"event": "Job status updated to Completed", "status": "Completed", "timestamp": completion_ts.isoformat()},
        ],
        created_at=completion_ts - timedelta(hours=3),
        updated_at=completion_ts,
    )
    db_session.add(b)
    db_session.commit()

    warranty = issue_booking_warranty(b, db_session)
    assert warranty is not None
    assert warranty.is_active is True
    assert warranty.claim_status == "None"

    # Verify duration is exactly 7 days
    duration = (warranty.expires_at - warranty.issued_at).days
    assert duration == 7
    # Issued at matches completion timestamp within 1 second tolerance
    assert abs(warranty.issued_at.timestamp() - completion_ts.timestamp()) < 5


def test_beauty_booking_does_not_receive_warranty(db_session: Session, warranty_actors):
    """Verify beauty/salon booking does not receive a warranty card."""
    b = Booking(
        id=uuid.uuid4(),
        booking_reference=f"BK-{uuid.uuid4().hex[:8].upper()}",
        customer_id=warranty_actors["customer"].id,
        service_id=warranty_actors["service_id"],
        category="Women's Spa & Salon",
        service_name="Herbal Hair Treatment",
        status="Completed",
        payment_method="COD",
        payment_status="Paid",
        total_price=Decimal("1299.00"),
        created_at=datetime.now(timezone.utc),
    )
    db_session.add(b)
    db_session.commit()

    warranty = issue_booking_warranty(b, db_session)
    assert warranty is None


def test_customer_warranty_claim_valid_lifecycle(db_session: Session, warranty_actors):
    """Verify customer can view 7-day card and submit claim without unapproved fees."""
    completion_ts = datetime.now(timezone.utc)
    b = Booking(
        id=uuid.uuid4(),
        booking_reference=f"BK-{uuid.uuid4().hex[:8].upper()}",
        customer_id=warranty_actors["customer"].id,
        service_id=warranty_actors["service_id"],
        category="Electrical",
        service_name="Switchboard Wiring Repair",
        status="Completed",
        payment_method="COD",
        payment_status="Paid",
        total_price=Decimal("650.00"),
        created_at=completion_ts,
        updated_at=completion_ts,
    )
    db_session.add(b)
    db_session.commit()

    headers = {"Authorization": f"Bearer {warranty_actors['token']}"}

    # 1. Fetch warranty card
    res_card = client.get(f"/api/v1/customer/bookings/{b.id}/warranty", headers=headers)
    assert res_card.status_code == 200
    card_data = res_card.json()
    assert card_data["is_eligible"] is True
    assert card_data["duration_days"] == 7
    assert card_data["nominal_fee"] == 0.0

    # 2. Submit warranty claim
    res_claim = client.post(
        f"/api/v1/customer/bookings/{b.id}/warranty/claim",
        json={"description": "The switchboard tripped again after 2 days. Sparks observed."},
        headers=headers,
    )
    assert res_claim.status_code == 200
    claim_data = res_claim.json()
    assert claim_data["success"] is True
    assert claim_data["nominal_fee"] == 0.0
    assert "free rework" in claim_data["message"].lower()

    # 3. Duplicate pending claim is rejected
    res_dup = client.post(
        f"/api/v1/customer/bookings/{b.id}/warranty/claim",
        json={"description": "Reporting again."},
        headers=headers,
    )
    assert res_dup.status_code == 400
    assert "already pending" in res_dup.json()["detail"].lower()


def test_expired_warranty_claim_rejected(db_session: Session, warranty_actors):
    """Verify that claims on expired warranties (older than 7 days) are rejected."""
    expired_completion = datetime.now(timezone.utc) - timedelta(days=9)
    b = Booking(
        id=uuid.uuid4(),
        booking_reference=f"BK-{uuid.uuid4().hex[:8].upper()}",
        customer_id=warranty_actors["customer"].id,
        service_id=warranty_actors["service_id"],
        category="Plumbing",
        service_name="Drain Unclogging",
        status="Completed",
        payment_method="COD",
        payment_status="Paid",
        total_price=Decimal("499.00"),
        created_at=expired_completion,
        updated_at=expired_completion,
    )
    db_session.add(b)
    db_session.commit()

    # Manually issue expired warranty (expired 2 days ago)
    w = BookingWarranty(
        id=uuid.uuid4(),
        booking_id=b.id,
        customer_id=b.customer_id,
        service_name=b.service_name,
        issued_at=expired_completion,
        expires_at=expired_completion + timedelta(days=7),
        is_active=False,
        claim_status="None",
    )
    db_session.add(w)
    db_session.commit()

    headers = {"Authorization": f"Bearer {warranty_actors['token']}"}
    res = client.post(
        f"/api/v1/customer/bookings/{b.id}/warranty/claim",
        json={"description": "Pipe leaking again after 9 days."},
        headers=headers,
    )
    assert res.status_code == 400
    assert "expired" in res.json()["detail"].lower()


def test_unauthorized_warranty_access(db_session: Session, warranty_actors):
    """Verify that one customer cannot view or raise a claim on another customer's warranty."""
    b = Booking(
        id=uuid.uuid4(),
        booking_reference=f"BK-{uuid.uuid4().hex[:8].upper()}",
        customer_id=warranty_actors["customer"].id,
        service_id=warranty_actors["service_id"],
        category="Carpentry",
        service_name="Cabinet Hinge Fixing",
        status="Completed",
        payment_method="COD",
        payment_status="Paid",
        total_price=Decimal("450.00"),
        created_at=datetime.now(timezone.utc),
    )
    db_session.add(b)
    db_session.commit()

    other_headers = {"Authorization": f"Bearer {warranty_actors['other_token']}"}

    # Fetching another customer's warranty must return 403 Forbidden
    res_get = client.get(f"/api/v1/customer/bookings/{b.id}/warranty", headers=other_headers)
    assert res_get.status_code == 403

    # Claiming another customer's warranty must return 403 Forbidden
    res_claim = client.post(
        f"/api/v1/customer/bookings/{b.id}/warranty/claim",
        json={"description": "Unauthorized claim attempt."},
        headers=other_headers,
    )
    assert res_claim.status_code == 403
