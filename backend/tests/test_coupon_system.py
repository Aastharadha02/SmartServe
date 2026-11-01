import uuid
from decimal import Decimal
from datetime import datetime, timezone, timedelta
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.database import get_db
from app.models.user import User
from app.models.customer import Customer, Booking, CombinedBooking
from app.models.service import Service
from app.models.coupon import Coupon, CouponRedemption
from app.services.coupon_service import (
    validate_coupon,
    redeem_coupon,
    mint_spin_reward_coupon,
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
def coupon_actors(db_session: Session):
    """Fixture creating test customers, admin, and active service with unique emails per test."""
    sfx = uuid.uuid4().hex[:8]
    email1 = f"c1_{sfx}@smartserve.com"
    email2 = f"c2_{sfx}@smartserve.com"
    admin_email = f"adm_{sfx}@smartserve.com"

    u1 = User(
        id=uuid.uuid4(),
        email=email1,
        hashed_password="TestPassword123!",
        role="customer",
        is_active=True,
    )
    db_session.add(u1)
    db_session.commit()

    c1 = Customer(
        id=uuid.uuid4(),
        user_id=u1.id,
        email=email1,
        full_name="Coupon Test User One",
        phone=f"91{uuid.uuid4().int % 100000000:08d}",
    )
    db_session.add(c1)
    db_session.commit()

    u2 = User(
        id=uuid.uuid4(),
        email=email2,
        hashed_password="TestPassword123!",
        role="customer",
        is_active=True,
    )
    db_session.add(u2)
    db_session.commit()

    c2 = Customer(
        id=uuid.uuid4(),
        user_id=u2.id,
        email=email2,
        full_name="Coupon Test User Two",
        phone=f"92{uuid.uuid4().int % 100000000:08d}",
    )
    db_session.add(c2)
    db_session.commit()

    admin_u = User(
        id=uuid.uuid4(),
        email=admin_email,
        hashed_password="AdminPassword123!",
        role="super_admin",
        is_active=True,
    )
    db_session.add(admin_u)
    db_session.commit()

    t1 = create_access_token({"sub": u1.email, "role": "customer", "user_id": str(u1.id)})
    t2 = create_access_token({"sub": u2.email, "role": "customer", "user_id": str(u2.id)})
    admin_t = create_access_token({"sub": admin_u.email, "role": "super_admin", "user_id": str(admin_u.id)})

    svc = db_session.query(Service).first()
    return {
        "u1": u1,
        "c1": c1,
        "t1": t1,
        "u2": u2,
        "c2": c2,
        "t2": t2,
        "admin": admin_u,
        "admin_token": admin_t,
        "service": svc,
    }


def test_fixed_discount_validation(db_session: Session, coupon_actors):
    """Verify fixed-amount coupon calculation via API."""
    headers = {"Authorization": f"Bearer {coupon_actors['t1']}"}
    res = client.post(
        "/api/v1/coupons/validate",
        json={"code": "WELCOME50", "subtotal": 500.00},
        headers=headers,
    )
    assert res.status_code == 200
    data = res.json()
    assert data["is_valid"] is True
    assert float(data["discount_amount"]) == 50.00
    assert float(data["final_total"]) == 450.00
    assert data["code"] == "WELCOME50"


def test_percentage_discount_and_max_cap(db_session: Session, coupon_actors):
    """Verify percentage coupon and cap enforcement via API."""
    headers = {"Authorization": f"Bearer {coupon_actors['t1']}"}

    # Order under cap: 10% of 600 = 60
    res1 = client.post(
        "/api/v1/coupons/validate",
        json={"code": "FESTIVE10", "subtotal": 600.00},
        headers=headers,
    )
    assert res1.status_code == 200
    assert float(res1.json()["discount_amount"]) == 60.00
    assert float(res1.json()["final_total"]) == 540.00

    # Order exceeding cap: 10% of 2500 = 250, capped at max_discount_amount 150
    res2 = client.post(
        "/api/v1/coupons/validate",
        json={"code": "FESTIVE10", "subtotal": 2500.00},
        headers=headers,
    )
    assert res2.status_code == 200
    assert float(res2.json()["discount_amount"]) == 150.00
    assert float(res2.json()["final_total"]) == 2350.00


def test_minimum_order_amount_enforcement(db_session: Session, coupon_actors):
    """Verify that orders below min_order_amount are rejected."""
    headers = {"Authorization": f"Bearer {coupon_actors['t1']}"}
    # WELCOME50 min order is 299
    res = client.post(
        "/api/v1/coupons/validate",
        json={"code": "WELCOME50", "subtotal": 199.00},
        headers=headers,
    )
    assert res.status_code == 200
    data = res.json()
    assert data["is_valid"] is False
    assert "minimum order" in data["message"].lower()
    assert float(data["discount_amount"]) == 0.00


def test_expired_coupon_rejected(db_session: Session, coupon_actors):
    """Verify expired coupons cannot be validated."""
    past_date = datetime.now(timezone.utc) - timedelta(days=5)
    exp_c = Coupon(
        id=uuid.uuid4(),
        code=f"EXPIRED_{uuid.uuid4().hex[:6].upper()}",
        description="Expired Coupon",
        discount_type="FIXED",
        discount_value=Decimal("50.00"),
        min_order_amount=Decimal("100.00"),
        is_active=True,
        valid_from=past_date - timedelta(days=10),
        valid_until=past_date,
    )
    db_session.add(exp_c)
    db_session.commit()

    headers = {"Authorization": f"Bearer {coupon_actors['t1']}"}
    res = client.post(
        "/api/v1/coupons/validate",
        json={"code": exp_c.code, "subtotal": 500.00},
        headers=headers,
    )
    assert res.status_code == 200
    assert res.json()["is_valid"] is False
    assert "expired" in res.json()["message"].lower()


def test_spin_reward_minting_and_customer_exclusivity(db_session: Session, coupon_actors):
    """Verify spin-the-wheel reward creates valid coupon tied exclusively to recipient."""
    headers_c1 = {"Authorization": f"Bearer {coupon_actors['t1']}"}
    headers_c2 = {"Authorization": f"Bearer {coupon_actors['t2']}"}

    # 1. Customer 1 spins the wheel and claims a reward
    res_spin = client.post(
        "/api/v1/coupons/spin-reward",
        json={"reward_tier": "SERVE75"},
        headers=headers_c1,
    )
    assert res_spin.status_code == 200
    spin_data = res_spin.json()
    assert spin_data["success"] is True
    spin_code = spin_data["code"]
    assert spin_code.startswith("SPIN75-")

    # 2. Customer 1 validates their personal spin reward -> Valid
    res_val1 = client.post(
        "/api/v1/coupons/validate",
        json={"code": spin_code, "subtotal": 450.00},
        headers=headers_c1,
    )
    assert res_val1.status_code == 200
    assert res_val1.json()["is_valid"] is True
    assert float(res_val1.json()["discount_amount"]) == 75.00

    # 3. Customer 2 attempts to use Customer 1's spin reward -> Rejected
    res_val2 = client.post(
        "/api/v1/coupons/validate",
        json={"code": spin_code, "subtotal": 450.00},
        headers=headers_c2,
    )
    assert res_val2.status_code == 200
    assert res_val2.json()["is_valid"] is False
    assert "another customer" in res_val2.json()["message"].lower()


def test_per_customer_usage_limit_and_prevent_duplicate_redemption(db_session: Session, coupon_actors):
    """Verify that a customer cannot redeem a single-use coupon multiple times."""
    c1 = coupon_actors["c1"]

    coupon = Coupon(
        id=uuid.uuid4(),
        code=f"SINGLE_{uuid.uuid4().hex[:6].upper()}",
        description="Single use test coupon",
        discount_type="FIXED",
        discount_value=Decimal("40.00"),
        min_order_amount=Decimal("100.00"),
        is_active=True,
        max_uses_per_customer=1,
    )
    db_session.add(coupon)
    db_session.commit()

    # 1. First redemption succeeds
    ok1, msg1, disc1, red1 = redeem_coupon(
        db=db_session,
        coupon_id=coupon.id,
        customer_id=c1.id,
        subtotal=Decimal("300.00"),
    )
    assert ok1 is True
    assert disc1 == Decimal("40.00")
    assert red1 is not None

    # 2. Second redemption is rejected
    ok2, msg2, disc2, red2 = redeem_coupon(
        db=db_session,
        coupon_id=coupon.id,
        customer_id=c1.id,
        subtotal=Decimal("300.00"),
    )
    assert ok2 is False
    assert "already redeemed" in msg2.lower()
    assert disc2 == Decimal("0.00")


def test_combined_booking_coupon_integration(db_session: Session, coupon_actors):
    """Verify combined booking applies bundle discount and coupon without double counting."""
    headers = {"Authorization": f"Bearer {coupon_actors['t1']}"}
    services = db_session.query(Service).filter(Service.is_active == True).limit(2).all()
    if len(services) < 2:
        pytest.skip("Requires at least 2 services for combined booking test")

    s1, s2 = services[0], services[1]
    combined_subtotal = Decimal(str(s1.base_price)) + Decimal(str(s2.base_price))
    bundle_discount = (combined_subtotal * Decimal("0.05")).quantize(Decimal("0.01"))
    net_after_bundle = combined_subtotal - bundle_discount

    payload = {
        "service_ids": [str(s1.id), str(s2.id)],
        "scheduled_date": "2026-11-05",
        "scheduled_time": "11:00",
        "address_line1": "Flat 402, Lotus Arena, Sector 79",
        "coupon_code": "WELCOME50",
    }

    res = client.post("/api/v1/customer/combined-bookings", json=payload, headers=headers)
    assert res.status_code == 200
    cb_data = res.json()
    assert cb_data["coupon_code"] == "WELCOME50"
    assert float(cb_data["coupon_discount"]) == 50.00
    expected_final = float(max(Decimal("0.00"), net_after_bundle - Decimal("50.00")))
    assert abs(float(cb_data["final_price"]) - expected_final) < 0.05


def test_admin_coupon_management_and_toggle(db_session: Session, coupon_actors):
    """Verify admin can list, create, and toggle coupons, while customer is restricted."""
    admin_headers = {"Authorization": f"Bearer {coupon_actors['admin_token']}"}
    cust_headers = {"Authorization": f"Bearer {coupon_actors['t1']}"}

    # 1. Customer cannot access admin coupons
    res_unauth = client.get("/api/v1/admin/coupons", headers=cust_headers)
    assert res_unauth.status_code == 403

    # 2. Admin creates a new promo coupon
    new_code = f"PROMO{uuid.uuid4().hex[:4].upper()}"
    res_create = client.post(
        "/api/v1/admin/coupons",
        json={
            "code": new_code,
            "description": "Admin Created Flash Sale",
            "discount_type": "FIXED",
            "discount_value": 100.00,
            "min_order_amount": 499.00,
            "valid_days": 15,
        },
        headers=admin_headers,
    )
    assert res_create.status_code == 201
    created_id = res_create.json()["id"]

    # 3. Admin toggles coupon inactive
    res_toggle = client.patch(f"/api/v1/admin/coupons/{created_id}/toggle", headers=admin_headers)
    assert res_toggle.status_code == 200
    assert res_toggle.json()["is_active"] is False

    # 4. Inactive coupon cannot be used
    res_val = client.post(
        "/api/v1/coupons/validate",
        json={"code": new_code, "subtotal": 600.00},
        headers=cust_headers,
    )
    assert res_val.status_code == 200
    assert res_val.json()["is_valid"] is False
    assert "no longer active" in res_val.json()["message"].lower()
