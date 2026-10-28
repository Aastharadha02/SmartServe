import uuid
from decimal import Decimal
from datetime import datetime, timezone, timedelta
from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.config import settings
from app.core.database import SessionLocal
from app.core.security import create_access_token, hash_password
from app.models.user import User
from app.models.customer import Customer, Booking
from app.models.provider import Provider
from app.models.service import Service
from app.models.payment import BookingPayment, BookingOTP
from app.models.notification import NotificationLog
from app.services.booking.otp_service import generate_secure_otp, verify_and_consume_otp, get_active_otp
from app.services.notification.notification_service import notify_booking_event

client = TestClient(app)


@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def test_actors(db_session: Session):
    db_session.rollback()
    
    # 1. Customer
    cust_user = db_session.query(User).filter(User.email == "test_cod_cust@smartserve.com").first()
    if not cust_user:
        cust_user = User(
            id=uuid.uuid4(),
            email="test_cod_cust@smartserve.com",
            password_hash=hash_password("Pass123!"),
            role="customer",
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )
        db_session.add(cust_user)
        db_session.flush()

    customer = db_session.query(Customer).filter(Customer.user_id == cust_user.id).first()
    if not customer:
        customer = Customer(
            id=uuid.uuid4(),
            user_id=cust_user.id,
            full_name="COD Test Customer",
            email=cust_user.email,
            phone="+919876543210",
            is_verified=True,
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )
        db_session.add(customer)
        db_session.flush()

    # 2. Provider
    prov_user = db_session.query(User).filter(User.email == "test_cod_prov@smartserve.com").first()
    if not prov_user:
        prov_user = User(
            id=uuid.uuid4(),
            email="test_cod_prov@smartserve.com",
            password_hash=hash_password("Pass123!"),
            role="provider",
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )
        db_session.add(prov_user)
        db_session.flush()

    provider = db_session.query(Provider).filter(Provider.user_id == prov_user.id).first()
    if not provider:
        provider = Provider(
            user_id=prov_user.id,
            full_name="COD Test Provider",
            category="Plumbing",
            experience_years=5,
            is_verified=True,
            created_at=datetime.now(timezone.utc),
        )
        db_session.add(provider)
        db_session.flush()

    # 3. Admin
    admin_user = db_session.query(User).filter(User.email == "test_cod_admin@smartserve.com").first()
    if not admin_user:
        admin_user = User(
            id=uuid.uuid4(),
            email="test_cod_admin@smartserve.com",
            password_hash=hash_password("Pass123!"),
            role="super_admin",
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )
        db_session.add(admin_user)
        db_session.flush()

    # 4. Service
    srv = db_session.query(Service).first()
    if not srv:
        srv = Service(
            id=uuid.uuid4(),
            name="Emergency Pipe Repair",
            category="Plumbing",
            subcategory="Repairs",
            base_price=Decimal("799.00"),
            is_active=True,
        )
        db_session.add(srv)
        db_session.flush()

    db_session.commit()

    cust_token = create_access_token({"sub": cust_user.email, "role": "customer", "user_id": str(cust_user.id)})
    prov_token = create_access_token({"sub": prov_user.email, "role": "provider", "user_id": str(prov_user.id), "provider_id": str(provider.user_id)})
    admin_token = create_access_token({"sub": admin_user.email, "role": "super_admin", "user_id": str(admin_user.id)})

    return {
        "customer": customer,
        "provider": provider,
        "admin": admin_user,
        "service": srv,
        "cust_token": cust_token,
        "prov_token": prov_token,
        "admin_token": admin_token,
    }


def create_sample_booking(db: Session, actors, status="Requested", total_price=Decimal("850.00")):
    b_id = uuid.uuid4()
    sched = datetime.now(timezone.utc) + timedelta(hours=2)
    b = Booking(
        id=b_id,
        booking_reference=f"BK-{uuid.uuid4().hex[:8].upper()}",
        customer_id=actors["customer"].id,
        provider_id=actors["provider"].user_id,
        service_id=actors["service"].id,
        service_name=actors["service"].name,
        category=actors["service"].category,
        status=status,
        payment_method="COD",
        payment_status="Pending",
        scheduled_date=sched.strftime("%Y-%m-%d"),
        scheduled_time=sched,
        address_line1="123 Smart Road, Sector 15",
        city="Ahmedabad",
        pincode="380015",
        address="123 Smart Road, Sector 15, Ahmedabad",
        total_price=total_price,
        timeline=[],
        created_at=datetime.now(timezone.utc),
    )
    db.add(b)
    db.commit()
    db.refresh(b)
    return b


# -----------------------------------------------------------------------------
# 1. TWO-STAGE OTP GENERATION, EXPIRY, AND ATTEMPT LOCKOUT
# -----------------------------------------------------------------------------

def test_otp_service_attempt_lockout_and_expiry(db_session: Session, test_actors):
    """Verify that OTP locks after max failed attempts and rejects expired codes."""
    b = create_sample_booking(db_session, test_actors)
    
    # Generate Start OTP with 4 digits
    start_otp = generate_secure_otp(b.id, "START", db_session, expires_in_minutes=180, digits=4)
    assert len(start_otp.otp_code) == 4
    assert start_otp.is_used is False
    assert start_otp.is_locked is False

    # 1. Test invalid attempt decrements remaining
    valid, msg = verify_and_consume_otp(b.id, "START", "0000", db_session)
    assert valid is False
    assert "remaining" in msg

    # 2. Re-fetch and check attempts incremented
    db_session.refresh(start_otp)
    assert start_otp.failed_attempts == 1

    # 3. Fail up to max_attempts (5 attempts)
    for _ in range(4):
        verify_and_consume_otp(b.id, "START", "0000", db_session)

    db_session.refresh(start_otp)
    assert start_otp.is_locked is True

    # 4. Correct code now fails because OTP is locked
    valid, msg = verify_and_consume_otp(b.id, "START", start_otp.otp_code, db_session)
    assert valid is False
    assert "locked" in msg.lower()


def test_otp_service_single_use_and_expiry(db_session: Session, test_actors):
    """Verify that OTP cannot be consumed twice and cannot be used after expiration."""
    b = create_sample_booking(db_session, test_actors)
    
    otp = generate_secure_otp(b.id, "START", db_session, expires_in_minutes=180)
    code = otp.otp_code

    # 1. Successful verification
    valid, msg = verify_and_consume_otp(b.id, "START", code, db_session)
    assert valid is True
    assert "verified" in msg.lower()

    # 2. Replay attempt MUST fail
    valid2, msg2 = verify_and_consume_otp(b.id, "START", code, db_session)
    assert valid2 is False
    assert "already been used" in msg2.lower()

    # 3. Test expiration check
    expired_otp = generate_secure_otp(b.id, "COMPLETE", db_session, expires_in_minutes=-1) # expired in past
    valid3, msg3 = verify_and_consume_otp(b.id, "COMPLETE", expired_otp.otp_code, db_session)
    assert valid3 is False
    assert "expired" in msg3.lower()


# -----------------------------------------------------------------------------
# 2. PROVIDER TWO-STAGE WORKFLOW (START JOB WITH OTP -> COMPLETE JOB WITH OTP)
# -----------------------------------------------------------------------------

def test_provider_start_and_complete_workflow(db_session: Session, test_actors):
    """Verify provider advances booking from Arrived to Started (OTP 1) and Completed (OTP 2)."""
    b = create_sample_booking(db_session, test_actors, status="Arrived")
    start_otp = generate_secure_otp(b.id, "START", db_session)

    prov_headers = {"Authorization": f"Bearer {test_actors['prov_token']}"}

    # 1. Invalid start OTP fails
    res_fail = client.post(
        f"/api/v1/providers/me/bookings/{b.id}/start",
        json={"otp_code": "9999"},
        headers=prov_headers
    )
    assert res_fail.status_code == 400
    assert "otp" in res_fail.json()["detail"].lower()

    # 2. Correct start OTP succeeds and advances status to Started
    res_start = client.post(
        f"/api/v1/providers/me/bookings/{b.id}/start",
        json={"otp_code": start_otp.otp_code},
        headers=prov_headers
    )
    assert res_start.status_code == 200
    assert res_start.json()["status"] == "Started"

    # 3. Completion OTP was automatically generated
    db_session.refresh(b)
    comp_otp = get_active_otp(b.id, "COMPLETE", db_session)
    assert comp_otp is not None
    assert len(comp_otp.otp_code) == 4

    # 4. Complete job with completion OTP
    res_comp = client.post(
        f"/api/v1/providers/me/bookings/{b.id}/complete",
        json={"otp_code": comp_otp.otp_code, "notes": "Work inspected and approved by customer"},
        headers=prov_headers
    )
    assert res_comp.status_code == 200
    assert res_comp.json()["status"] == "Completed"


# -----------------------------------------------------------------------------
# 3. CASH-ON-DELIVERY REPORTING AND DISCREPANCY DETECTION
# -----------------------------------------------------------------------------

def test_cod_reporting_exact_amount(db_session: Session, test_actors):
    """Verify reporting exact collected cash amount sets discrepancy_flag to False."""
    b = create_sample_booking(db_session, test_actors, status="Completed", total_price=Decimal("1200.00"))
    prov_headers = {"Authorization": f"Bearer {test_actors['prov_token']}"}

    res = client.post(
        f"/api/v1/providers/me/bookings/{b.id}/cash-collected",
        json={"reported_amount": 1200.00, "notes": "Received exact cash from customer"},
        headers=prov_headers
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "Collection Reported"
    assert data["discrepancy_flag"] is False
    assert data["reported_amount"] == 1200.00

    # Verify duplicate submission is rejected
    res_dup = client.post(
        f"/api/v1/providers/me/bookings/{b.id}/cash-collected",
        json={"reported_amount": 1200.00},
        headers=prov_headers
    )
    assert res_dup.status_code == 400
    assert "already been reported" in res_dup.json()["detail"].lower()


def test_cod_reporting_discrepancy_flagged(db_session: Session, test_actors):
    """Verify reporting different cash amount flags discrepancy and computes discrepancy_amount."""
    b = create_sample_booking(db_session, test_actors, status="Completed", total_price=Decimal("1500.00"))
    prov_headers = {"Authorization": f"Bearer {test_actors['prov_token']}"}

    res = client.post(
        f"/api/v1/providers/me/bookings/{b.id}/cash-collected",
        json={"reported_amount": 1400.00, "notes": "Customer had only 1400 cash"},
        headers=prov_headers
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "Collection Reported"
    assert data["discrepancy_flag"] is True
    assert abs(data["discrepancy_amount"] - 100.00) < 0.01


# -----------------------------------------------------------------------------
# 4. ADMIN COD REVIEW QUEUE (VERIFY AND REJECT)
# -----------------------------------------------------------------------------

def test_admin_payment_review_and_verification(db_session: Session, test_actors):
    """Verify admin can view payment review queue and verify payment collection."""
    b = create_sample_booking(db_session, test_actors, status="Completed", total_price=Decimal("950.00"))
    
    # Provider reports cash
    client.post(
        f"/api/v1/providers/me/bookings/{b.id}/cash-collected",
        json={"reported_amount": 950.00, "notes": "Exact cash"},
        headers={"Authorization": f"Bearer {test_actors['prov_token']}"}
    )

    admin_headers = {"Authorization": f"Bearer {test_actors['admin_token']}"}

    # 1. Admin lists review queue
    res_list = client.get("/api/v1/admin/bookings/payments/review", headers=admin_headers)
    assert res_list.status_code == 200
    items = res_list.json()
    target_payment = next((p for p in items if p["booking_id"] == str(b.id)), None)
    assert target_payment is not None
    assert target_payment["status"] == "Collection Reported"

    # 2. Non-admin cannot verify payment (RBAC)
    cust_headers = {"Authorization": f"Bearer {test_actors['cust_token']}"}
    res_forbidden = client.post(
        f"/api/v1/admin/bookings/payments/{target_payment['id']}/verify",
        json={"notes": "Customer hacking"},
        headers=cust_headers
    )
    assert res_forbidden.status_code in (401, 403)

    # 3. Admin verifies payment
    res_verify = client.post(
        f"/api/v1/admin/bookings/payments/{target_payment['id']}/verify",
        json={"notes": "Cash settlement confirmed by ops"},
        headers=admin_headers
    )
    assert res_verify.status_code == 200
    assert res_verify.json()["status"] in ["Paid", "Verified"]

    # 4. Verify booking is now marked Paid
    db_session.refresh(b)
    assert b.payment_status == "Paid"


def test_admin_payment_rejection(db_session: Session, test_actors):
    """Verify admin can reject a suspicious or disputed cash collection report."""
    b = create_sample_booking(db_session, test_actors, status="Completed", total_price=Decimal("1000.00"))
    
    client.post(
        f"/api/v1/providers/me/bookings/{b.id}/cash-collected",
        json={"reported_amount": 500.00, "notes": "Customer paid half only"},
        headers={"Authorization": f"Bearer {test_actors['prov_token']}"}
    )

    admin_headers = {"Authorization": f"Bearer {test_actors['admin_token']}"}
    payment = db_session.query(BookingPayment).filter(BookingPayment.booking_id == b.id).first()
    assert payment is not None

    # Admin rejects payment
    res_reject = client.post(
        f"/api/v1/admin/bookings/payments/{payment.id}/reject",
        json={"reason": "Customer disputed the reported amount; investigating."},
        headers=admin_headers
    )
    assert res_reject.status_code == 200
    data = res_reject.json()
    assert data["status"] == "Rejected"
    assert "Customer disputed" in data["rejection_reason"]


# -----------------------------------------------------------------------------
# 5. AUTOMATED NOTIFICATIONS DISPATCH AUDIT LOGGING
# -----------------------------------------------------------------------------

def test_automated_notifications_logging(db_session: Session, test_actors):
    """Verify automated notifications dispatch creates audit log records in DB."""
    b = create_sample_booking(db_session, test_actors, status="Requested")

    # Trigger booking confirmation notification
    notify_booking_event(
        db=db_session,
        booking=b,
        event_type="booking.confirmed"
    )

    # Check notification audit logs
    audits = (
        db_session.query(NotificationLog)
        .filter(NotificationLog.booking_id == b.id)
        .all()
    )
    assert len(audits) >= 1
    channels = [a.channel.lower() for a in audits]
    # Check that at least email or whatsapp was logged
    assert any(c in ["email", "whatsapp"] for c in channels)
    for a in audits:
        assert a.delivery_status in ["Sent", "Delivered", "Delivered (Mock)", "Unconfigured", "Failed"]
