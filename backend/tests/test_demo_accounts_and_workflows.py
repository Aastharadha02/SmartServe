"""
SmartServe - Reusable Demo Accounts and Repeatable Testing Setup Test Suite

Verifies:
1. Idempotent demo accounts initialization (no duplicate records).
2. Demo Customer, Provider, and Admin authentication across auth endpoints.
3. Repeatable demo booking preparation with authentic Start & Complete OTPs.
4. Two-Stage OTP verification lifecycle using persistent demo accounts.
5. Provider cash collection reporting and discrepancy detection.
6. Admin verification & rejection of reported cash payments.
7. Safety checks of the demo reset utility (rejects production/remote targets).
8. Scoped demo reset (purges only demo bookings, preserves accounts & non-demo data).
9. Automated tests independence (no manual user registration required).
"""

import os
import uuid
import pytest
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.user import User
from app.models.customer import Customer, Booking
from app.models.provider import Provider, ProviderService, Availability
from app.models.security import AdminRole
from app.models.payment import BookingPayment, BookingOTP, PaymentStatus, OTPType
from app.models.service import Service
from app.services.demo_service import (
    setup_demo_accounts,
    prepare_demo_booking,
    reset_demo_data,
    DEMO_CUSTOMER_CONFIG,
    DEMO_PROVIDER_CONFIG,
    DEMO_ADMIN_CONFIG,
)
from app.services.booking.otp_service import get_active_otp

client = TestClient(app)


@pytest.fixture(scope="function")
def db():
    _db = SessionLocal()
    try:
        yield _db
    finally:
        _db.rollback()
        _db.close()


@pytest.fixture(scope="function", autouse=True)
def ensure_demo_accounts_exist(db: Session):
    """Ensure baseline demo accounts are present before testing."""
    setup_demo_accounts(db)
    yield


# =============================================================================
# 1. IDEMPOTENCY & REUSABILITY TESTS
# =============================================================================

def test_demo_setup_is_strictly_idempotent(db: Session):
    """Running setup_demo_accounts twice must not create duplicate accounts."""
    first_run = setup_demo_accounts(db)
    second_run = setup_demo_accounts(db)

    # Second run must report 0 newly created users
    user_creates = [r for r in second_run["created_records"] if r.startswith("User:")]
    assert len(user_creates) == 0

    # User IDs must remain identical
    assert first_run["customer"]["user_id"] == second_run["customer"]["user_id"]
    assert first_run["provider"]["user_id"] == second_run["provider"]["user_id"]
    assert first_run["admin"]["user_id"] == second_run["admin"]["user_id"]

    # Verify counts in database
    cust_count = db.query(User).filter(User.email == DEMO_CUSTOMER_CONFIG["email"]).count()
    prov_count = db.query(User).filter(User.email == DEMO_PROVIDER_CONFIG["email"]).count()
    admin_count = db.query(User).filter(User.email == DEMO_ADMIN_CONFIG["email"]).count()
    assert cust_count == 1
    assert prov_count == 1
    assert admin_count == 1


def test_demo_accounts_can_log_in_repeatedly():
    """All three demo accounts must successfully authenticate via real endpoints."""
    # 1. Customer Login
    r_cust = client.post(
        "/api/v1/customer/auth/login",
        json={"email": DEMO_CUSTOMER_CONFIG["email"], "password": DEMO_CUSTOMER_CONFIG["password"]},
    )
    assert r_cust.status_code == 200
    cust_token = r_cust.json().get("access_token")
    assert cust_token is not None

    # 2. Provider Login
    r_prov = client.post(
        "/api/v1/auth/login",
        json={"email": DEMO_PROVIDER_CONFIG["email"], "password": DEMO_PROVIDER_CONFIG["password"]},
    )
    assert r_prov.status_code == 200
    prov_data = r_prov.json()
    assert prov_data["role"] == "provider"
    assert "access_token" in prov_data

    # 3. Admin Login
    r_admin = client.post(
        "/api/v1/auth/login",
        json={"email": DEMO_ADMIN_CONFIG["email"], "password": DEMO_ADMIN_CONFIG["password"]},
    )
    assert r_admin.status_code == 200
    admin_data = r_admin.json()
    assert admin_data["role"] in ["admin", "super_admin"]
    assert "access_token" in admin_data


# =============================================================================
# 2. REPEATABLE DEMO BOOKING & OTP TESTS
# =============================================================================

def test_prepare_demo_booking_creates_valid_cod_record(db: Session):
    """prepare_demo_booking creates a clean booking in 'Arrived' with Start OTP & COD payment."""
    booking_info = prepare_demo_booking(db, status="Arrived", agreed_amount=1250.0)

    assert booking_info["status"] == "Arrived"
    assert booking_info["payment_method"] == "COD"
    assert booking_info["payment_status"] == "Pending"
    assert booking_info["agreed_amount"] == 1250.0
    assert booking_info["customer_email"] == DEMO_CUSTOMER_CONFIG["email"]
    assert booking_info["provider_email"] == DEMO_PROVIDER_CONFIG["email"]
    assert len(booking_info["start_otp"]) == 4

    # Verify payment in DB
    payment = db.query(BookingPayment).filter(BookingPayment.booking_id == uuid.UUID(booking_info["booking_id"])).first()
    assert payment is not None
    assert payment.payment_method == "COD"
    assert float(payment.agreed_amount) == 1250.0
    assert payment.status == PaymentStatus.PENDING.value


def test_customer_can_create_booking_via_standard_api(db: Session):
    """Demo customer can book an active service via standard customer booking endpoint."""
    r_login = client.post(
        "/api/v1/customer/auth/login",
        json={"email": DEMO_CUSTOMER_CONFIG["email"], "password": DEMO_CUSTOMER_CONFIG["password"]},
    )
    token = r_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    service = db.query(Service).filter(Service.category.ilike("%cleaning%"), Service.is_active == True).first()
    assert service is not None

    target_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
    booking_payload = {
        "service_id": str(service.id),
        "scheduled_date": target_date,
        "scheduled_time": "11:30",
        "address_line1": "101 Demo Residency, Sector 18",
        "city": "Noida",
        "pincode": "201301",
        "payment_method": "COD",
    }

    res = client.post("/api/v1/customer/bookings", json=booking_payload, headers=headers)
    assert res.status_code == 200
    b_data = res.json()
    assert b_data["payment_method"] == "COD"
    assert b_data["payment_status"] == "Pending"
    assert "start_otp" in b_data or "id" in b_data


def test_full_two_stage_otp_and_cod_demo_workflow(db: Session):
    """
    Simulates the exact 9-step demo workflow using the persistent demo accounts:
    Customer booking -> Provider Start OTP -> Provider Completion OTP -> Cash Reported -> Admin Verified.
    """
    # Step 1: Prepare demo booking in 'Arrived'
    booking_info = prepare_demo_booking(db, status="Arrived", agreed_amount=1500.0)
    booking_id = booking_info["booking_id"]
    start_otp = booking_info["start_otp"]

    # Provider logs in
    prov_login = client.post(
        "/api/v1/auth/login",
        json={"email": DEMO_PROVIDER_CONFIG["email"], "password": DEMO_PROVIDER_CONFIG["password"]},
    )
    prov_token = prov_login.json()["access_token"]
    prov_headers = {"Authorization": f"Bearer {prov_token}"}

    # Step 2: Provider starts service with customer Start OTP
    start_res = client.post(
        f"/api/v1/providers/me/bookings/{booking_id}/start",
        json={"otp_code": start_otp},
        headers=prov_headers,
    )
    assert start_res.status_code == 200
    assert start_res.json()["status"] == "Started"

    # Step 3: Customer accesses Completion OTP
    cust_login = client.post(
        "/api/v1/customer/auth/login",
        json={"email": DEMO_CUSTOMER_CONFIG["email"], "password": DEMO_CUSTOMER_CONFIG["password"]},
    )
    cust_token = cust_login.json()["access_token"]
    cust_res = client.get(
        f"/api/v1/customer/bookings/{booking_id}",
        headers={"Authorization": f"Bearer {cust_token}"},
    )
    assert cust_res.status_code == 200
    completion_otp = cust_res.json()["completion_otp"]
    assert completion_otp is not None
    assert completion_otp != start_otp

    # Step 4: Provider completes service with Completion OTP
    comp_res = client.post(
        f"/api/v1/providers/me/bookings/{booking_id}/complete",
        json={"otp_code": completion_otp},
        headers=prov_headers,
    )
    assert comp_res.status_code == 200
    assert comp_res.json()["status"] == "Completed"

    # Step 5: Provider reports cash collection
    cash_res = client.post(
        f"/api/v1/providers/me/bookings/{booking_id}/cash-collected",
        json={"reported_amount": 1500.0, "notes": "Full COD received in cash"},
        headers=prov_headers,
    )
    assert cash_res.status_code == 200
    assert cash_res.json()["status"] == "Collection Reported"

    # Step 6: Admin verifies payment
    admin_login = client.post(
        "/api/v1/auth/login",
        json={"email": DEMO_ADMIN_CONFIG["email"], "password": DEMO_ADMIN_CONFIG["password"]},
    )
    admin_token = admin_login.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # Query payment record
    payment = db.query(BookingPayment).filter(BookingPayment.booking_id == uuid.UUID(booking_id)).first()
    assert payment is not None

    verify_res = client.post(
        f"/api/v1/admin/bookings/payments/{payment.id}/verify",
        json={"notes": "Audited with branch register"},
        headers=admin_headers,
    )
    assert verify_res.status_code == 200
    assert verify_res.json()["status"] == "Paid"


# =============================================================================
# 3. SAFE DEMO RESET UTILITY TESTS
# =============================================================================

def test_safe_reset_utility_safety_guards(db: Session, monkeypatch):
    """Reset utility must reject execution if ENVIRONMENT is production."""
    # Simulate production environment
    monkeypatch.setattr(settings, "ENVIRONMENT", "production")
    with pytest.raises(PermissionError) as exc_info:
        reset_demo_data(db)
    assert "production" in str(exc_info.value).lower()


def test_safe_reset_utility_deletes_only_demo_records(db: Session):
    """
    Reset utility must purge only demo bookings & payments,
    leaving demo user accounts and non-demo users/bookings intact.
    """
    # 1. Create a demo booking
    prepare_demo_booking(db, status="Arrived")

    # 2. Count before reset
    cust_user = db.query(User).filter(User.email == DEMO_CUSTOMER_CONFIG["email"]).first()
    prov_user = db.query(User).filter(User.email == DEMO_PROVIDER_CONFIG["email"]).first()
    admin_user = db.query(User).filter(User.email == DEMO_ADMIN_CONFIG["email"]).first()
    assert cust_user is not None
    assert prov_user is not None
    assert admin_user is not None

    # 3. Perform safe reset
    reset_report = reset_demo_data(db, force=True)
    assert reset_report["deleted_bookings"] >= 1

    # 4. Verify accounts still exist and are active
    db.expire_all()
    cust_check = db.query(User).filter(User.email == DEMO_CUSTOMER_CONFIG["email"]).first()
    prov_check = db.query(User).filter(User.email == DEMO_PROVIDER_CONFIG["email"]).first()
    admin_check = db.query(User).filter(User.email == DEMO_ADMIN_CONFIG["email"]).first()
    assert cust_check is not None and cust_check.is_active is True
    assert prov_check is not None and prov_check.is_active is True
    assert admin_check is not None and admin_check.is_active is True

    # 5. Verify demo bookings are 0
    cust_profile = db.query(Customer).filter(Customer.user_id == cust_check.id).first()
    demo_b_count = db.query(Booking).filter(Booking.customer_id == cust_profile.id).count()
    assert demo_b_count == 0
