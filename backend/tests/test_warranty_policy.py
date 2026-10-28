import uuid
from decimal import Decimal
from datetime import datetime, timezone, timedelta
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.database import SessionLocal
from app.core.security import create_access_token, hash_password
from app.models.user import User
from app.models.customer import Customer, Booking, BookingWarranty
from app.models.service import Service
from app.services.booking.warranty_service import (
    get_warranty_policy,
    issue_booking_warranty,
    validate_warranty_claim,
    DEFAULT_WARRANTY_NOMINAL_FEE,
)

client = TestClient(app)


@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def warranty_actors(db_session: Session):
    db_session.rollback()

    user = db_session.query(User).filter(User.email == "warranty_cust@smartserve.com").first()
    if not user:
        user = User(
            id=uuid.uuid4(),
            email="warranty_cust@smartserve.com",
            password_hash=hash_password("Pass123!"),
            role="customer",
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )
        db_session.add(user)
        db_session.flush()

    customer = db_session.query(Customer).filter(Customer.user_id == user.id).first()
    if not customer:
        customer = Customer(
            id=uuid.uuid4(),
            user_id=user.id,
            full_name="Warranty Test Customer",
            email=user.email,
            phone="+919876543219",
            is_verified=True,
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )
        db_session.add(customer)
        db_session.flush()

    db_session.commit()
    token = create_access_token({"sub": user.email, "role": "customer", "user_id": str(user.id)})
    return {"user": user, "customer": customer, "token": token}


def test_warranty_policy_category_rules():
    """Verify 15-day, 10-day, and beauty exclusion rules."""
    # 1. Plumbing & Electrical = 15 days
    plumb = get_warranty_policy("Plumbing", "Tap Leak Repair")
    assert plumb["is_eligible"] is True
    assert plumb["duration_days"] == 15
    assert plumb["nominal_fee"] == DEFAULT_WARRANTY_NOMINAL_FEE

    elec = get_warranty_policy("Electrical", "Fan Installation")
    assert elec["is_eligible"] is True
    assert elec["duration_days"] == 15

    # 2. Carpentry & Painting = 10 days
    carp = get_warranty_policy("Carpentry", "Door Hinge Fix")
    assert carp["is_eligible"] is True
    assert carp["duration_days"] == 10

    paint = get_warranty_policy("Painting", "Waterproofing Touchup")
    assert paint["is_eligible"] is True
    assert paint["duration_days"] == 10

    # 3. Beauty / Salon / Spa = Excluded
    beauty = get_warranty_policy("Salon for Women", "Facial & Glow Cleanup")
    assert beauty["is_eligible"] is False
    assert beauty["duration_days"] == 0
    assert "excluded" in beauty["terms"].lower()

    spa = get_warranty_policy("Personal Care", "Deep Tissue Spa")
    assert spa["is_eligible"] is False
    assert spa["duration_days"] == 0


def test_issue_warranty_for_plumbing_booking(db_session: Session, warranty_actors):
    """Verify plumbing booking receives 15-day warranty upon completion."""
    b = Booking(
        id=uuid.uuid4(),
        booking_reference=f"BK-{uuid.uuid4().hex[:8].upper()}",
        customer_id=warranty_actors["customer"].id,
        category="Plumbing",
        service_name="Bathroom Pipe Fitting",
        status="Completed",
        payment_method="COD",
        payment_status="Paid",
        total_price=Decimal("899.00"),
        created_at=datetime.now(timezone.utc),
    )
    db_session.add(b)
    db_session.commit()

    warranty = issue_booking_warranty(b, db_session)
    assert warranty is not None
    assert warranty.is_active is True
    assert warranty.claim_status == "None"

    # Verify duration is 15 days
    duration = (warranty.expires_at - warranty.issued_at).days
    assert duration == 15


def test_beauty_booking_does_not_receive_warranty(db_session: Session, warranty_actors):
    """Verify beauty/salon booking does not receive a warranty card."""
    b = Booking(
        id=uuid.uuid4(),
        booking_reference=f"BK-{uuid.uuid4().hex[:8].upper()}",
        customer_id=warranty_actors["customer"].id,
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


def test_customer_warranty_claim_lifecycle(db_session: Session, warranty_actors):
    """Verify customer can submit warranty claim and receive nominal inspection fee notice."""
    b = Booking(
        id=uuid.uuid4(),
        booking_reference=f"BK-{uuid.uuid4().hex[:8].upper()}",
        customer_id=warranty_actors["customer"].id,
        category="Electrical",
        service_name="Switchboard Wiring Repair",
        status="Completed",
        payment_method="COD",
        payment_status="Paid",
        total_price=Decimal("650.00"),
        created_at=datetime.now(timezone.utc),
    )
    db_session.add(b)
    db_session.commit()

    headers = {"Authorization": f"Bearer {warranty_actors['token']}"}

    # 1. Fetch warranty card
    res_card = client.get(f"/api/v1/customer/bookings/{b.id}/warranty", headers=headers)
    assert res_card.status_code == 200
    card_data = res_card.json()
    assert card_data["is_eligible"] is True
    assert card_data["duration_days"] == 15
    assert card_data["nominal_fee"] == 49.0

    # 2. Submit warranty claim
    res_claim = client.post(
        f"/api/v1/customer/bookings/{b.id}/warranty/claim",
        json={"description": "The switchboard tripped again after 2 days. Sparks observed."},
        headers=headers,
    )
    assert res_claim.status_code == 200
    claim_data = res_claim.json()
    assert claim_data["success"] is True
    assert claim_data["nominal_fee"] == 49.0
    assert "nominal" in claim_data["message"].lower() or "minimal" in claim_data["message"].lower()

    # 3. Verify duplicate claim returns already pending status
    res_dup = client.post(
        f"/api/v1/customer/bookings/{b.id}/warranty/claim",
        json={"description": "Reporting again."},
        headers=headers,
    )
    assert res_dup.status_code == 400
    assert "already pending" in res_dup.json()["detail"].lower()
