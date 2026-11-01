import uuid
from datetime import datetime, timedelta, timezone
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.database import SessionLocal
from app.core.security import create_access_token
from app.models.user import User
from app.models.customer import Customer
from app.models.provider import Provider
from app.models.booking import Booking
from app.models.payment import BookingPayment, BookingOTP, PaymentStatus, OTPType
from app.models.service import Service
from app.services.booking.otp_service import generate_secure_otp, verify_and_consume_otp, get_active_otp

client = TestClient(app)


@pytest.fixture(scope="function")
def db():
    _db = SessionLocal()
    try:
        yield _db
    finally:
        _db.rollback()
        _db.close()


@pytest.fixture(scope="function")
def test_actors(db: Session):
    customer_user = db.query(User).filter(User.role == "customer", User.is_active == True).first()
    if not customer_user:
        customer_user = User(
            id=str(uuid.uuid4()),
            email=f"cust_{uuid.uuid4().hex[:6]}@example.com",
            full_name="Test Customer",
            role="customer",
            is_active=True,
            is_profile_complete=True,
        )
        db.add(customer_user)
        db.commit()
    else:
        customer_user.is_profile_complete = True
        db.commit()

    customer = db.query(Customer).filter(Customer.user_id == customer_user.id).first()
    if not customer:
        customer = Customer(
            id=str(uuid.uuid4()),
            user_id=customer_user.id,
            full_name=customer_user.full_name,
            phone="+919876543210",
        )
        db.add(customer)
        db.commit()

    provider_user = db.query(User).filter(User.role == "provider", User.is_active == True).first()
    if not provider_user:
        provider_user = User(
            id=str(uuid.uuid4()),
            email=f"prov_{uuid.uuid4().hex[:6]}@example.com",
            full_name="Test Provider",
            role="provider",
            is_active=True,
            is_profile_complete=True,
        )
        db.add(provider_user)
        db.commit()
    else:
        provider_user.is_profile_complete = True
        db.commit()

    provider = db.query(Provider).filter(Provider.user_id == provider_user.id).first()
    if not provider:
        provider = Provider(
            id=str(uuid.uuid4()),
            user_id=provider_user.id,
            full_name=provider_user.full_name,
            category="Cleaning",
            is_verified=True,
        )
        db.add(provider)
        db.commit()

    other_prov_user = (
        db.query(User)
        .filter(User.role == "provider", User.is_active == True, User.id != provider_user.id)
        .first()
    )
    if not other_prov_user:
        other_prov_user = User(
            id=str(uuid.uuid4()),
            email=f"otherprov_{uuid.uuid4().hex[:6]}@example.com",
            full_name="Other Provider",
            role="provider",
            is_active=True,
            is_profile_complete=True,
        )
        db.add(other_prov_user)
        db.commit()
    else:
        other_prov_user.is_profile_complete = True
        db.commit()

    other_prov = db.query(Provider).filter(Provider.user_id == other_prov_user.id).first()
    if not other_prov:
        other_prov = Provider(
            id=str(uuid.uuid4()),
            user_id=other_prov_user.id,
            full_name=other_prov_user.full_name,
            category="Cleaning",
            is_verified=True,
        )
        db.add(other_prov)
        db.commit()

    admin_user = db.query(User).filter(User.role.in_(["admin", "super_admin"]), User.is_active == True).first()
    if not admin_user:
        admin_user = User(
            id=str(uuid.uuid4()),
            email=f"admin_{uuid.uuid4().hex[:6]}@smartserve.com",
            full_name="Admin Ops",
            role="admin",
            is_active=True,
            is_profile_complete=True,
        )
        db.add(admin_user)
        db.commit()

    service = db.query(Service).filter(Service.is_active == True).first()
    if not service:
        service = Service(
            id=uuid.uuid4(),
            category="Cleaning",
            subcategory="Home Cleaning",
            name="Deep Cleaning Service",
            base_price=750.0,
            is_active=True,
        )
        db.add(service)
        db.commit()

    return {
        "customer_user": customer_user,
        "customer": customer,
        "provider_user": provider_user,
        "provider": provider,
        "other_prov_user": other_prov_user,
        "other_prov": other_prov,
        "admin_user": admin_user,
        "service": service,
        "customer_token": create_access_token({"sub": str(customer_user.id), "role": "customer"}),
        "provider_token": create_access_token({"sub": str(provider_user.id), "role": "provider"}),
        "other_prov_token": create_access_token({"sub": str(other_prov_user.id), "role": "provider"}),
        "admin_token": create_access_token({"sub": str(admin_user.id), "role": "admin"}),
    }


def create_test_booking(db: Session, test_actors: dict, status: str = "Requested", agreed_amount: float = 750.0):
    b = Booking(
        id=str(uuid.uuid4()),
        customer_id=str(test_actors["customer"].id),
        provider_id=str(test_actors["provider_user"].id),
        service_id=str(test_actors["service"].id),
        status=status,
        payment_method="COD",
        payment_status="Pending",
        total_price=agreed_amount,
        address="123 SmartServe Lane",
        scheduled_time=datetime.now(timezone.utc) + timedelta(hours=2),
    )
    db.add(b)
    db.flush()

    payment = BookingPayment(
        id=str(uuid.uuid4()),
        booking_id=b.id,
        customer_id=b.customer_id,
        provider_id=b.provider_id,
        payment_method="COD",
        agreed_amount=agreed_amount,
        status=PaymentStatus.PENDING.value,
    )
    db.add(payment)

    start_otp_record = generate_secure_otp(b.id, OTPType.START.value, db)
    db.commit()
    db.refresh(b)
    return b, start_otp_record.otp_code


# =============================================================================
# PART 1: TWO-STAGE OTP TESTS
# =============================================================================

def test_new_booking_has_cod_and_start_otp(db: Session, test_actors: dict):
    booking, start_otp = create_test_booking(db, test_actors, status="Requested", agreed_amount=800.0)
    assert booking.payment_method == "COD"
    assert booking.payment_status == "Pending"
    assert start_otp is not None
    assert len(start_otp) == 4
    assert start_otp.isdigit()

    # Verify payment record was created
    payment = db.query(BookingPayment).filter(BookingPayment.booking_id == booking.id).first()
    assert payment is not None
    assert float(payment.agreed_amount) == 800.0
    assert payment.status == PaymentStatus.PENDING.value


def test_provider_api_never_exposes_otp(db: Session, test_actors: dict):
    booking, _ = create_test_booking(db, test_actors, status="Arrived")
    headers = {"Authorization": f"Bearer {test_actors['provider_token']}"}

    res = client.get("/api/v1/providers/me/bookings", headers=headers)
    assert res.status_code == 200
    matched = [b for b in res.json() if str(b["id"]) == str(booking.id)]
    assert len(matched) == 1
    # OTP code MUST NOT be exposed to provider
    assert matched[0].get("otp_code") is None
    assert "start_otp" not in matched[0] or matched[0].get("start_otp") is None


def test_customer_can_view_start_otp(db: Session, test_actors: dict):
    booking, start_otp = create_test_booking(db, test_actors, status="Arrived")
    headers = {"Authorization": f"Bearer {test_actors['customer_token']}"}

    res = client.get(f"/api/v1/customer/bookings/{booking.id}", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["start_otp"] == start_otp
    assert data["payment_method"] == "COD"
    assert data["payment_status"] == "Pending"


def test_correct_start_otp_permits_service_start(db: Session, test_actors: dict):
    booking, start_otp = create_test_booking(db, test_actors, status="Arrived")
    headers = {"Authorization": f"Bearer {test_actors['provider_token']}"}

    res = client.post(
        f"/api/v1/providers/me/bookings/{booking.id}/start",
        json={"otp_code": start_otp},
        headers=headers,
    )
    assert res.status_code == 200
    assert res.json()["status"] == "Started"

    db.refresh(booking)
    assert booking.status == "Started"

    # Start OTP is now marked as used
    active_start = get_active_otp(booking.id, OTPType.START.value, db)
    assert active_start is None

    # Completion OTP was automatically generated
    active_complete = get_active_otp(booking.id, OTPType.COMPLETE.value, db)
    assert active_complete is not None
    assert len(active_complete.otp_code) == 4


def test_invalid_start_otp_is_rejected(db: Session, test_actors: dict):
    booking, _ = create_test_booking(db, test_actors, status="Arrived")
    headers = {"Authorization": f"Bearer {test_actors['provider_token']}"}

    res = client.post(
        f"/api/v1/providers/me/bookings/{booking.id}/start",
        json={"otp_code": "0000"},
        headers=headers,
    )
    assert res.status_code == 400
    assert "incorrect" in res.json()["detail"].lower() or "invalid" in res.json()["detail"].lower() or "verification" in res.json()["detail"].lower()

    db.refresh(booking)
    assert booking.status == "Arrived"


def test_expired_start_otp_is_rejected(db: Session, test_actors: dict):
    booking, _ = create_test_booking(db, test_actors, status="Arrived")
    # Expire the OTP in DB
    otp_record = (
        db.query(BookingOTP)
        .filter(BookingOTP.booking_id == booking.id, BookingOTP.otp_type == OTPType.START.value)
        .first()
    )
    otp_record.expires_at = datetime.now(timezone.utc) - timedelta(minutes=10)
    db.commit()

    headers = {"Authorization": f"Bearer {test_actors['provider_token']}"}
    res = client.post(
        f"/api/v1/providers/me/bookings/{booking.id}/start",
        json={"otp_code": otp_record.otp_code},
        headers=headers,
    )
    assert res.status_code == 400
    assert "expired" in res.json()["detail"].lower()


def test_start_otp_cannot_be_reused(db: Session, test_actors: dict):
    booking, start_otp = create_test_booking(db, test_actors, status="Arrived")
    headers = {"Authorization": f"Bearer {test_actors['provider_token']}"}

    # First start: success
    res1 = client.post(
        f"/api/v1/providers/me/bookings/{booking.id}/start",
        json={"otp_code": start_otp},
        headers=headers,
    )
    assert res1.status_code == 200

    # Second start with same OTP: rejected
    res2 = client.post(
        f"/api/v1/providers/me/bookings/{booking.id}/start",
        json={"otp_code": start_otp},
        headers=headers,
    )
    assert res2.status_code in [400, 422]


def test_otp_attempt_limits_enforced(db: Session, test_actors: dict):
    booking, start_otp = create_test_booking(db, test_actors, status="Arrived")
    headers = {"Authorization": f"Bearer {test_actors['provider_token']}"}

    # Submit 5 incorrect OTP attempts
    for _ in range(5):
        res = client.post(
            f"/api/v1/providers/me/bookings/{booking.id}/start",
            json={"otp_code": "9999"},
            headers=headers,
        )
        assert res.status_code == 400

    # 6th attempt (even with CORRECT OTP) is rejected due to lockout
    res_locked = client.post(
        f"/api/v1/providers/me/bookings/{booking.id}/start",
        json={"otp_code": start_otp},
        headers=headers,
    )
    assert res_locked.status_code == 400
    assert "maximum" in res_locked.json()["detail"].lower() or "locked" in res_locked.json()["detail"].lower()


def test_completion_requires_own_distinct_otp(db: Session, test_actors: dict):
    booking, start_otp = create_test_booking(db, test_actors, status="Arrived")
    headers = {"Authorization": f"Bearer {test_actors['provider_token']}"}

    # Start service with start OTP
    res_start = client.post(
        f"/api/v1/providers/me/bookings/{booking.id}/start",
        json={"otp_code": start_otp},
        headers=headers,
    )
    assert res_start.status_code == 200

    # Attempting complete without OTP is rejected
    res_no_otp = client.post(
        f"/api/v1/providers/me/bookings/{booking.id}/complete",
        json={},
        headers=headers,
    )
    assert res_no_otp.status_code in [400, 422]

    # Attempting complete with START OTP is rejected
    res_start_otp = client.post(
        f"/api/v1/providers/me/bookings/{booking.id}/complete",
        json={"otp_code": start_otp},
        headers=headers,
    )
    assert res_start_otp.status_code == 400

    # Customer accesses completion OTP
    cust_res = client.get(
        f"/api/v1/customer/bookings/{booking.id}",
        headers={"Authorization": f"Bearer {test_actors['customer_token']}"},
    )
    completion_otp = cust_res.json()["completion_otp"]
    assert completion_otp is not None
    assert completion_otp != start_otp

    # Complete with valid completion OTP: success
    res_complete = client.post(
        f"/api/v1/providers/me/bookings/{booking.id}/complete",
        json={"otp_code": completion_otp},
        headers=headers,
    )
    assert res_complete.status_code == 200
    assert res_complete.json()["status"] == "Completed"

    db.refresh(booking)
    assert booking.status == "Completed"


def test_completion_otp_from_other_booking_rejected(db: Session, test_actors: dict):
    b1, start_otp1 = create_test_booking(db, test_actors, status="Arrived")
    b2, start_otp2 = create_test_booking(db, test_actors, status="Arrived")
    headers = {"Authorization": f"Bearer {test_actors['provider_token']}"}

    # Start both
    client.post(f"/api/v1/providers/me/bookings/{b1.id}/start", json={"otp_code": start_otp1}, headers=headers)
    client.post(f"/api/v1/providers/me/bookings/{b2.id}/start", json={"otp_code": start_otp2}, headers=headers)

    b2_otp = get_active_otp(b2.id, OTPType.COMPLETE.value, db)

    # Try completing b1 with b2's completion OTP
    res = client.post(
        f"/api/v1/providers/me/bookings/{b1.id}/complete",
        json={"otp_code": b2_otp.otp_code},
        headers=headers,
    )
    assert res.status_code == 400


# =============================================================================
# PART 2: CASH ON DELIVERY & PAYMENT REVIEW TESTS
# =============================================================================

def test_provider_reports_cash_collection(db: Session, test_actors: dict):
    booking, start_otp = create_test_booking(db, test_actors, status="Arrived", agreed_amount=950.0)
    headers = {"Authorization": f"Bearer {test_actors['provider_token']}"}

    # Start service
    client.post(f"/api/v1/providers/me/bookings/{booking.id}/start", json={"otp_code": start_otp}, headers=headers)

    # Report cash collection
    res = client.post(
        f"/api/v1/providers/me/bookings/{booking.id}/cash-collected",
        json={"reported_amount": 950.0, "notes": "Exact cash received"},
        headers=headers,
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "Collection Reported"
    assert data["reported_amount"] == 950.0
    assert data["discrepancy_flag"] is False

    # Check booking payment status in DB
    db.refresh(booking)
    assert booking.payment_status == "Collection Reported"
    # Booking must NOT be auto-marked as Paid
    assert booking.payment_status != "Paid"


def test_provider_cannot_report_collection_for_unassigned_booking(db: Session, test_actors: dict):
    booking, start_otp = create_test_booking(db, test_actors, status="Arrived")
    # Start service by assigned provider
    client.post(
        f"/api/v1/providers/me/bookings/{booking.id}/start",
        json={"otp_code": start_otp},
        headers={"Authorization": f"Bearer {test_actors['provider_token']}"},
    )

    # Other provider attempts to report cash
    other_headers = {"Authorization": f"Bearer {test_actors['other_prov_token']}"}
    res = client.post(
        f"/api/v1/providers/me/bookings/{booking.id}/cash-collected",
        json={"reported_amount": 750.0},
        headers=other_headers,
    )
    assert res.status_code in [403, 404]


def test_duplicate_cash_collection_reports_prevented(db: Session, test_actors: dict):
    booking, start_otp = create_test_booking(db, test_actors, status="Arrived", agreed_amount=600.0)
    headers = {"Authorization": f"Bearer {test_actors['provider_token']}"}

    client.post(f"/api/v1/providers/me/bookings/{booking.id}/start", json={"otp_code": start_otp}, headers=headers)

    # First report
    res1 = client.post(
        f"/api/v1/providers/me/bookings/{booking.id}/cash-collected",
        json={"reported_amount": 600.0},
        headers=headers,
    )
    assert res1.status_code == 200

    # Second duplicate report
    res2 = client.post(
        f"/api/v1/providers/me/bookings/{booking.id}/cash-collected",
        json={"reported_amount": 600.0},
        headers=headers,
    )
    assert res2.status_code == 400
    assert "already" in res2.json()["detail"].lower() or "duplicate" in res2.json()["detail"].lower()


def test_amount_discrepancy_flagged(db: Session, test_actors: dict):
    booking, start_otp = create_test_booking(db, test_actors, status="Arrived", agreed_amount=1000.0)
    headers = {"Authorization": f"Bearer {test_actors['provider_token']}"}

    client.post(f"/api/v1/providers/me/bookings/{booking.id}/start", json={"otp_code": start_otp}, headers=headers)

    # Report different amount (₹900 instead of ₹1000)
    res = client.post(
        f"/api/v1/providers/me/bookings/{booking.id}/cash-collected",
        json={"reported_amount": 900.0, "notes": "Customer gave ₹900 only"},
        headers=headers,
    )
    assert res.status_code == 200
    data = res.json()
    assert data["discrepancy_flag"] is True
    assert data["discrepancy_amount"] == 100.0


def test_admin_can_verify_reported_collection(db: Session, test_actors: dict):
    booking, start_otp = create_test_booking(db, test_actors, status="Arrived", agreed_amount=1200.0)
    headers = {"Authorization": f"Bearer {test_actors['provider_token']}"}

    client.post(f"/api/v1/providers/me/bookings/{booking.id}/start", json={"otp_code": start_otp}, headers=headers)
    client.post(
        f"/api/v1/providers/me/bookings/{booking.id}/cash-collected",
        json={"reported_amount": 1200.0},
        headers=headers,
    )

    payment = db.query(BookingPayment).filter(BookingPayment.booking_id == booking.id).first()
    assert payment.status == PaymentStatus.COLLECTION_REPORTED.value

    # Admin verifies payment
    admin_headers = {"Authorization": f"Bearer {test_actors['admin_token']}"}
    res = client.post(
        f"/api/v1/admin/bookings/payments/{payment.id}/verify",
        json={"notes": "Cash audited and reconciled with ops desk"},
        headers=admin_headers,
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "Paid"
    assert data["reviewed_by_name"] is not None

    db.refresh(booking)
    assert booking.payment_status == "Paid"


def test_admin_can_reject_reported_collection_with_reason(db: Session, test_actors: dict):
    booking, start_otp = create_test_booking(db, test_actors, status="Arrived", agreed_amount=1500.0)
    headers = {"Authorization": f"Bearer {test_actors['provider_token']}"}

    client.post(f"/api/v1/providers/me/bookings/{booking.id}/start", json={"otp_code": start_otp}, headers=headers)
    client.post(
        f"/api/v1/providers/me/bookings/{booking.id}/cash-collected",
        json={"reported_amount": 1000.0},
        headers=headers,
    )

    payment = db.query(BookingPayment).filter(BookingPayment.booking_id == booking.id).first()

    # Rejection requires reason
    admin_headers = {"Authorization": f"Bearer {test_actors['admin_token']}"}
    res_no_reason = client.post(
        f"/api/v1/admin/bookings/payments/{payment.id}/reject",
        json={"reason": ""},
        headers=admin_headers,
    )
    assert res_no_reason.status_code == 422

    # Reject with valid reason
    res = client.post(
        f"/api/v1/admin/bookings/payments/{payment.id}/reject",
        json={"reason": "Customer confirms paying full amount, provider discrepancy investigation opened"},
        headers=admin_headers,
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "Rejected"
    assert "Customer confirms" in data["rejection_reason"]

    db.refresh(booking)
    assert booking.payment_status == "Rejected"


def test_unauthorized_user_cannot_verify_payment(db: Session, test_actors: dict):
    booking, _ = create_test_booking(db, test_actors, status="Completed")
    payment = db.query(BookingPayment).filter(BookingPayment.booking_id == booking.id).first()

    # Customer tries to verify
    res_cust = client.post(
        f"/api/v1/admin/bookings/payments/{payment.id}/verify",
        json={},
        headers={"Authorization": f"Bearer {test_actors['customer_token']}"},
    )
    assert res_cust.status_code in [401, 403]

    # Provider tries to verify
    res_prov = client.post(
        f"/api/v1/admin/bookings/payments/{payment.id}/verify",
        json={},
        headers={"Authorization": f"Bearer {test_actors['provider_token']}"},
    )
    assert res_prov.status_code in [401, 403]


def test_admin_payment_review_queue(db: Session, test_actors: dict):
    admin_headers = {"Authorization": f"Bearer {test_actors['admin_token']}"}
    res = client.get("/api/v1/admin/bookings/payments/review", headers=admin_headers)
    assert res.status_code == 200
    records = res.json()
    assert isinstance(records, list)
    if records:
        first = records[0]
        assert "agreed_amount" in first
        assert "payment_method" in first
        assert "status" in first
        assert "discrepancy_flag" in first
