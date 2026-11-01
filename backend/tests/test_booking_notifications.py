import uuid
from decimal import Decimal
from datetime import datetime, timezone, timedelta
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.customer import Customer, Booking
from app.models.provider import Provider
from app.models.service import Service
from app.models.payment import BookingPayment, BookingOTP
from app.models.user import User
from app.models.notification import NotificationLog
from app.services import email_service
from app.services.notification import (
    notify_booking_event,
    retry_notification,
    whatsapp_adapter,
    MAX_NOTIFICATION_RETRIES,
)
from app.services.demo_service import DEMO_CUSTOMER_CONFIG, DEMO_PROVIDER_CONFIG, DEMO_ADMIN_CONFIG

client = TestClient(app)


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def customer_auth():
    res = client.post(
        "/api/v1/auth/login",
        json={"email": DEMO_CUSTOMER_CONFIG["email"], "password": DEMO_CUSTOMER_CONFIG["password"]},
    )
    assert res.status_code == 200, res.text
    return {"Authorization": f"Bearer {res.json()['access_token']}"}


@pytest.fixture
def provider_auth():
    res = client.post(
        "/api/v1/auth/login",
        json={"email": DEMO_PROVIDER_CONFIG["email"], "password": DEMO_PROVIDER_CONFIG["password"]},
    )
    assert res.status_code == 200, res.text
    return {"Authorization": f"Bearer {res.json()['access_token']}"}


@pytest.fixture
def admin_auth():
    res = client.post(
        "/api/v1/auth/login",
        json={"email": DEMO_ADMIN_CONFIG["email"], "password": DEMO_ADMIN_CONFIG["password"]},
    )
    assert res.status_code == 200, res.text
    return {"Authorization": f"Bearer {res.json()['access_token']}"}


@pytest.fixture
def demo_customer(db: Session):
    cust = db.query(Customer).filter(Customer.email == DEMO_CUSTOMER_CONFIG["email"]).first()
    assert cust is not None
    return cust


@pytest.fixture
def demo_provider(db: Session):
    prov = (
        db.query(Provider)
        .join(User, Provider.user_id == User.id)
        .filter(User.email == DEMO_PROVIDER_CONFIG["email"])
        .first()
    )
    assert prov is not None
    return prov


@pytest.fixture
def demo_service(db: Session):
    svc = db.query(Service).filter(Service.name == "Bedroom Deep Cleaning").first()
    if not svc:
        svc = db.query(Service).first()
    assert svc is not None
    return svc


@pytest.fixture
def clean_booking(db: Session, demo_customer: Customer, demo_provider: Provider, demo_service: Service):
    """Create a temporary booking for notification lifecycle testing and clean up afterwards."""
    booking_id = uuid.uuid4()
    ref_code = f"BK-TEST-{uuid.uuid4().hex[:6].upper()}"
    booking = Booking(
        id=booking_id,
        booking_reference=ref_code,
        customer_id=demo_customer.id,
        provider_id=demo_provider.user_id,
        service_id=demo_service.id,
        service_name=demo_service.name,
        category=demo_service.category,
        status="Requested",
        payment_method="COD",
        payment_status="Pending",
        scheduled_date="2026-10-25",
        scheduled_time=datetime.now(timezone.utc) + timedelta(days=5),
        address_line1="123 Test Street, Sector 1",
        city="Noida",
        pincode="201301",
        total_price=Decimal("899.00"),
        timeline=[{"event": "Created for test", "timestamp": datetime.now(timezone.utc).isoformat()}],
        created_at=datetime.now(timezone.utc),
    )
    db.add(booking)

    payment = BookingPayment(
        id=uuid.uuid4(),
        booking_id=booking.id,
        customer_id=demo_customer.id,
        provider_id=demo_provider.user_id,
        payment_method="COD",
        agreed_amount=Decimal("899.00"),
        status="Pending",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(payment)
    db.commit()
    db.refresh(booking)

    yield booking

    # Cleanup notification logs, payment, and booking
    db.query(NotificationLog).filter(NotificationLog.booking_id == booking_id).delete()
    db.query(BookingPayment).filter(BookingPayment.booking_id == booking_id).delete()
    db.query(BookingOTP).filter(BookingOTP.booking_id == booking_id).delete()
    db.query(Booking).filter(Booking.id == booking_id).delete()
    db.commit()


# =============================================================================
# SCENARIO 1: Booking confirmation triggers expected email & WhatsApp attempts
# =============================================================================
def test_scenario_1_booking_confirmation_triggers_email_and_whatsapp(
    db: Session, clean_booking: Booking, demo_customer: Customer
):
    email_service.clear_sent_test_emails()
    whatsapp_adapter.clear_sent_test_whatsapp_messages()

    res = notify_booking_event(db, clean_booking, "booking.confirmed")
    assert res["email"] is not None
    assert res["email"]["status"] == "Sent"
    assert res["whatsapp"] is not None
    assert res["whatsapp"]["status"] == "Sent"

    # Verify email outbox
    emails = email_service.get_sent_test_emails()
    assert len(emails) >= 1
    confirm_email = next((e for e in emails if clean_booking.booking_reference in e["subject"]), None)
    assert confirm_email is not None
    assert confirm_email["recipient_email"] == demo_customer.email
    assert clean_booking.booking_reference in confirm_email["body_text"]
    assert "password" not in confirm_email["body_text"].lower()

    # Verify WhatsApp outbox
    wa_msgs = whatsapp_adapter.get_sent_test_whatsapp_messages()
    assert len(wa_msgs) >= 1
    confirm_wa = next((m for m in wa_msgs if clean_booking.booking_reference in m["body"]), None)
    assert confirm_wa is not None
    assert confirm_wa["event_type"] == "booking.confirmed"

    # Verify notification_logs table in database
    logs = (
        db.query(NotificationLog)
        .filter(NotificationLog.booking_id == clean_booking.id, NotificationLog.event_type == "booking.confirmed")
        .all()
    )
    assert len(logs) == 2  # One email, one whatsapp
    channels = {l.channel for l in logs}
    assert channels == {"email", "whatsapp"}
    for l in logs:
        assert l.delivery_status == "Sent"
        assert l.booking_reference == clean_booking.booking_reference


# =============================================================================
# SCENARIO 2: Cancellation triggers correct notification
# =============================================================================
def test_scenario_2_cancellation_triggers_correct_notification(
    db: Session, clean_booking: Booking, customer_auth: dict
):
    email_service.clear_sent_test_emails()
    whatsapp_adapter.clear_sent_test_whatsapp_messages()

    # Cancel booking via customer API
    res = client.post(
        f"/api/v1/customer/bookings/{clean_booking.id}/cancel",
        json={"reason": "Customer schedule conflict"},
        headers=customer_auth,
    )
    assert res.status_code == 200, res.text
    assert res.json()["status"].upper() == "CANCELLED"

    # Check notification logs for cancellation
    cancel_logs = (
        db.query(NotificationLog)
        .filter(NotificationLog.booking_id == clean_booking.id, NotificationLog.event_type == "booking.cancelled")
        .all()
    )
    assert len(cancel_logs) == 2
    for l in cancel_logs:
        assert l.delivery_status == "Sent"

    # Verify email outbox received cancellation email
    emails = email_service.get_sent_test_emails()
    cancel_email = next((e for e in emails if "Cancelled" in e["subject"]), None)
    assert cancel_email is not None
    assert clean_booking.booking_reference in cancel_email["body_text"]


# =============================================================================
# SCENARIO 3: Service completion triggers correct notification
# =============================================================================
def test_scenario_3_service_completion_triggers_correct_notification(
    db: Session, clean_booking: Booking
):
    from app.services.booking.state_machine import transition_booking_status
    from app.core.dependencies import AuthUser
    from app.services.booking.otp_service import get_active_otp

    admin_user = AuthUser(
        id=uuid.uuid4(),
        email="admin@smartserve.com",
        role="admin",
        full_name="Admin User",
    )

    # Transition to Started then Completed
    transition_booking_status(db, clean_booking.id, "Accepted", admin_user)
    transition_booking_status(db, clean_booking.id, "On The Way", admin_user)
    transition_booking_status(db, clean_booking.id, "Arrived", admin_user)
    transition_booking_status(db, clean_booking.id, "Started", admin_user)

    email_service.clear_sent_test_emails()
    whatsapp_adapter.clear_sent_test_whatsapp_messages()

    # Complete service
    transition_booking_status(db, clean_booking.id, "Completed", admin_user)

    comp_logs = (
        db.query(NotificationLog)
        .filter(NotificationLog.booking_id == clean_booking.id, NotificationLog.event_type == "service.completed")
        .all()
    )
    assert len(comp_logs) == 2
    for l in comp_logs:
        assert l.delivery_status == "Sent"

    emails = email_service.get_sent_test_emails()
    comp_email = next((e for e in emails if "Completed" in e["subject"]), None)
    assert comp_email is not None


# =============================================================================
# SCENARIO 4: Payment collection reported and verified produce distinct events
# =============================================================================
def test_scenario_4_payment_reported_and_verified_produce_distinct_events(
    db: Session, clean_booking: Booking, provider_auth: dict, admin_auth: dict
):
    from app.services.booking.state_machine import transition_booking_status
    from app.core.dependencies import AuthUser

    admin_user = AuthUser(
        id=uuid.uuid4(),
        email="admin@smartserve.com",
        role="admin",
        full_name="Admin User",
    )
    transition_booking_status(db, clean_booking.id, "Accepted", admin_user)
    transition_booking_status(db, clean_booking.id, "On The Way", admin_user)
    transition_booking_status(db, clean_booking.id, "Arrived", admin_user)
    transition_booking_status(db, clean_booking.id, "Started", admin_user)

    email_service.clear_sent_test_emails()

    # 1. Provider reports cash collection
    res_rep = client.post(
        f"/api/v1/providers/me/bookings/{clean_booking.id}/cash-collected",
        json={"reported_amount": 899.00, "notes": "Received exact cash from customer"},
        headers=provider_auth,
    )
    assert res_rep.status_code == 200, res_rep.text

    rep_logs = (
        db.query(NotificationLog)
        .filter(NotificationLog.booking_id == clean_booking.id, NotificationLog.event_type == "payment.collection_reported")
        .all()
    )
    assert len(rep_logs) == 2, "Must produce email and whatsapp for payment.collection_reported"

    # 2. Admin verifies payment
    res_ver = client.post(
        f"/api/v1/admin/payments/{clean_booking.id}/verify",
        json={"notes": "Audited and verified cash in hand"},
        headers=admin_auth,
    )
    assert res_ver.status_code == 200, res_ver.text

    ver_logs = (
        db.query(NotificationLog)
        .filter(NotificationLog.booking_id == clean_booking.id, NotificationLog.event_type == "payment.verified")
        .all()
    )
    assert len(ver_logs) == 2, "Must produce distinct email and whatsapp for payment.verified"

    # Ensure events are distinct in type and logs
    rep_types = {l.event_type for l in rep_logs}
    ver_types = {l.event_type for l in ver_logs}
    assert rep_types == {"payment.collection_reported"}
    assert ver_types == {"payment.verified"}


# =============================================================================
# SCENARIO 5: Payment rejection produces appropriate notification event
# =============================================================================
def test_scenario_5_payment_rejection_produces_notification_event(
    db: Session, clean_booking: Booking, provider_auth: dict, admin_auth: dict
):
    from app.services.booking.state_machine import transition_booking_status
    from app.core.dependencies import AuthUser

    admin_user = AuthUser(
        id=uuid.uuid4(),
        email="admin@smartserve.com",
        role="admin",
        full_name="Admin User",
    )
    transition_booking_status(db, clean_booking.id, "Accepted", admin_user)
    transition_booking_status(db, clean_booking.id, "On The Way", admin_user)
    transition_booking_status(db, clean_booking.id, "Arrived", admin_user)
    transition_booking_status(db, clean_booking.id, "Started", admin_user)

    # Provider reports payment
    res_p = client.post(
        f"/api/v1/providers/me/bookings/{clean_booking.id}/cash-collected",
        json={"reported_amount": 500.00, "notes": "Partial cash"},
        headers=provider_auth,
    )
    assert res_p.status_code == 200, res_p.text

    email_service.clear_sent_test_emails()

    # Admin rejects payment
    res_rej = client.post(
        f"/api/v1/admin/payments/{clean_booking.id}/reject",
        json={"reason": "Amount collected does not match invoice total. Shortage of Rs 399."},
        headers=admin_auth,
    )
    assert res_rej.status_code == 200, res_rej.text

    rej_logs = (
        db.query(NotificationLog)
        .filter(NotificationLog.booking_id == clean_booking.id, NotificationLog.event_type == "payment.rejected")
        .all()
    )
    assert len(rej_logs) == 2
    for l in rej_logs:
        assert l.delivery_status == "Sent"


# =============================================================================
# SCENARIO 6: Recipients are resolved from the registered customer account
# =============================================================================
def test_scenario_6_recipients_resolved_from_registered_customer_account(
    db: Session, clean_booking: Booking, demo_customer: Customer
):
    res = notify_booking_event(db, clean_booking, "booking.confirmed")
    logs = (
        db.query(NotificationLog)
        .filter(NotificationLog.booking_id == clean_booking.id)
        .all()
    )
    email_log = next(l for l in logs if l.channel == "email")
    wa_log = next(l for l in logs if l.channel == "whatsapp")

    assert email_log.recipient == demo_customer.email, (
        f"Recipient must match registered customer email: {demo_customer.email}"
    )
    assert demo_customer.phone.replace(" ", "").replace("-", "") in wa_log.recipient.replace(" ", ""), (
        f"Recipient must match registered customer phone: {demo_customer.phone}"
    )


# =============================================================================
# SCENARIO 7: Missing email or phone information is handled safely
# =============================================================================
def test_scenario_7_missing_email_or_phone_handled_safely(
    db: Session, demo_provider: Provider, demo_service: Service
):
    test_user_id = uuid.uuid4()
    test_user = User(
        id=test_user_id,
        email="invalid-email-format",
        password_hash="mock_hash_for_test",
        role="customer",
        is_active=True,
    )
    db.add(test_user)
    db.flush()

    # Customer with no phone and dummy invalid email
    test_cust = Customer(
        id=uuid.uuid4(),
        user_id=test_user_id,
        full_name="No Contact Customer",
        email="invalid-email-format",
        phone=None,
        role="customer",
        created_at=datetime.now(timezone.utc),
    )
    db.add(test_cust)

    booking = Booking(
        id=uuid.uuid4(),
        booking_reference=f"BK-NOCONTACT-{uuid.uuid4().hex[:4].upper()}",
        customer_id=test_cust.id,
        provider_id=demo_provider.user_id,
        service_id=demo_service.id,
        status="Requested",
        total_price=Decimal("100.00"),
        created_at=datetime.now(timezone.utc),
    )
    db.add(booking)
    db.commit()

    try:
        # Must execute safely without raising unhandled exceptions
        results = notify_booking_event(db, booking, "booking.confirmed")
        assert results["email"]["status"] == "Failed"
        assert results["whatsapp"]["status"] == "Failed"

        logs = db.query(NotificationLog).filter(NotificationLog.booking_id == booking.id).all()
        assert len(logs) == 2
        for l in logs:
            assert l.delivery_status == "Failed"
            assert l.error_message is not None
            assert "missing" in l.error_message.lower() or "invalid" in l.error_message.lower()
    finally:
        db.query(NotificationLog).filter(NotificationLog.booking_id == booking.id).delete()
        db.query(Booking).filter(Booking.id == booking.id).delete()
        db.query(Customer).filter(Customer.id == test_cust.id).delete()
        db.query(User).filter(User.id == test_user_id).delete()
        db.commit()


# =============================================================================
# SCENARIO 8: Unavailable WhatsApp provider reported as unconfigured or failed
# =============================================================================
def test_scenario_8_unavailable_whatsapp_provider_reported_as_unconfigured(
    db: Session, clean_booking: Booking
):
    # Override WhatsApp backend to 'unconfigured'
    with patch("app.services.notification.whatsapp_adapter.settings.WHATSAPP_BACKEND", "unconfigured"), \
         patch.dict("os.environ", {"WHATSAPP_BACKEND": "unconfigured"}):
        from app.services.notification.whatsapp_adapter import get_whatsapp_adapter
        adapter = get_whatsapp_adapter()
        result = adapter.send_notification(
            recipient_phone="+919876500001",
            event_type="booking.confirmed",
            template_name="test_tmpl",
            parameters={},
            fallback_text="Test fallback",
        )
        assert result.success is False
        assert result.status == "Unconfigured"
        assert "unconfigured" in result.error_message.lower()


# =============================================================================
# SCENARIO 9: SMTP or WhatsApp provider failures recorded correctly
# =============================================================================
def test_scenario_9_provider_failures_recorded_correctly(
    db: Session, clean_booking: Booking
):
    # Force SMTP failure
    with patch("app.services.email_service.settings.EMAIL_BACKEND", "smtp"), \
         patch("app.services.email_service.settings.SMTP_HOST", "invalid.smtp.host"), \
         patch("app.services.email_service._is_safe_smtp_recipient", return_value=True), \
         patch("app.services.email_service._dispatch_via_smtp", side_effect=ConnectionError("SMTP connection timed out")):
        res = notify_booking_event(db, clean_booking, "booking.rescheduled")
        assert res["email"]["status"] == "Failed"

        log = (
            db.query(NotificationLog)
            .filter(NotificationLog.booking_id == clean_booking.id, NotificationLog.channel == "email", NotificationLog.event_type == "booking.rescheduled")
            .first()
        )
        assert log is not None
        assert log.delivery_status == "Failed"
        assert "failed" in log.error_message.lower()


# =============================================================================
# SCENARIO 10: Repeated event processing does not create duplicate sends
# =============================================================================
def test_scenario_10_repeated_event_processing_does_not_create_duplicates(
    db: Session, clean_booking: Booking
):
    email_service.clear_sent_test_emails()
    whatsapp_adapter.clear_sent_test_whatsapp_messages()

    # First event trigger
    res1 = notify_booking_event(db, clean_booking, "booking.confirmed")
    assert res1["email"]["status"] == "Sent"
    assert res1["whatsapp"]["status"] == "Sent"
    initial_email_count = len(email_service.get_sent_test_emails())
    initial_wa_count = len(whatsapp_adapter.get_sent_test_whatsapp_messages())

    # Second event trigger with exact same event type (e.g. double click or retry)
    res2 = notify_booking_event(db, clean_booking, "booking.confirmed")
    assert res2["email"]["status"] == "AlreadySent"
    assert res2["whatsapp"]["status"] == "AlreadySent"

    # Outbox counts must NOT increase
    assert len(email_service.get_sent_test_emails()) == initial_email_count
    assert len(whatsapp_adapter.get_sent_test_whatsapp_messages()) == initial_wa_count

    # Database logs must remain exactly 2 (one per channel), not 4
    logs = (
        db.query(NotificationLog)
        .filter(NotificationLog.booking_id == clean_booking.id, NotificationLog.event_type == "booking.confirmed")
        .all()
    )
    assert len(logs) == 2


# =============================================================================
# SCENARIO 11: Retries follow the configured policy
# =============================================================================
def test_scenario_11_retries_follow_configured_policy(
    db: Session, clean_booking: Booking
):
    log = NotificationLog(
        id=uuid.uuid4(),
        booking_id=clean_booking.id,
        booking_reference=clean_booking.booking_reference,
        customer_id=clean_booking.customer_id,
        event_type="booking.rescheduled",
        channel="email",
        recipient="demo.customer@smartserve.com",
        delivery_status="Failed",
        idempotency_key=f"test-retry-{uuid.uuid4()}",
        retry_count=0,
        last_attempt_at=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
    )
    db.add(log)
    db.commit()

    # Retry 1
    updated = retry_notification(db, log.id, max_retries=MAX_NOTIFICATION_RETRIES)
    assert updated.retry_count == 1
    assert updated.delivery_status == "Sent"

    # Reset status to Failed and artificially set retry_count to max
    log.delivery_status = "Failed"
    log.retry_count = MAX_NOTIFICATION_RETRIES
    db.commit()

    # Retry when max reached must be rejected
    with pytest.raises(ValueError) as exc:
        retry_notification(db, log.id, max_retries=MAX_NOTIFICATION_RETRIES)
    assert "maximum retry limit" in str(exc.value).lower()


# =============================================================================
# SCENARIO 12: Notification failures do not corrupt booking or payment state
# =============================================================================
def test_scenario_12_notification_failures_do_not_corrupt_booking_or_payment(
    db: Session, clean_booking: Booking, customer_auth: dict
):
    # Simulate catastrophic failure in notification service
    with patch("app.services.notification.notify_booking_event", side_effect=RuntimeError("Kafka/Network Down")):
        # Customer cancel booking should still succeed cleanly
        res = client.post(
            f"/api/v1/customer/bookings/{clean_booking.id}/cancel",
            json={"reason": "Customer emergency"},
            headers=customer_auth,
        )
        assert res.status_code == 200, res.text
        db.refresh(clean_booking)
        assert clean_booking.status.upper() == "CANCELLED"


# =============================================================================
# SCENARIO 13: Customers cannot retrieve another customer's notification history
# =============================================================================
def test_scenario_13_customers_cannot_retrieve_another_customers_notifications(
    db: Session, clean_booking: Booking
):
    # Register an alternate second customer
    alt_res = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Second Customer",
            "email": f"cust2_{uuid.uuid4().hex[:6]}@smartserve.com",
            "password": "Password123!",
            "phone": "+919876543210",
        },
    )
    assert alt_res.status_code in (200, 201), alt_res.text
    token2 = alt_res.json()["access_token"]
    auth2 = {"Authorization": f"Bearer {token2}"}

    # Attempt to access clean_booking (owned by Demo Customer) with Customer 2's token
    res = client.get(
        f"/api/v1/customer/bookings/{clean_booking.id}/notifications",
        headers=auth2,
    )
    assert res.status_code == 403, "Must forbid customer from viewing another customer's notifications"
    assert "forbidden" in res.text.lower() or "another customer" in res.text.lower()


# =============================================================================
# SCENARIO 14: Provider and admin authorization remains unchanged
# =============================================================================
def test_scenario_14_provider_and_admin_authorization_remains_unchanged(
    clean_booking: Booking, provider_auth: dict, customer_auth: dict, admin_auth: dict
):
    # Customer cannot access admin notifications
    res_cust = client.get("/api/v1/admins/notifications", headers=customer_auth)
    assert res_cust.status_code in (401, 403), "Customer must not access admin notifications"

    # Provider cannot access admin notifications
    res_prov = client.get("/api/v1/admins/notifications", headers=provider_auth)
    assert res_prov.status_code in (401, 403), "Provider must not access admin notifications"

    # Admin CAN access admin notifications
    res_admin = client.get("/api/v1/admins/notifications", headers=admin_auth)
    assert res_admin.status_code == 200
    assert isinstance(res_admin.json(), list)


# =============================================================================
# SCENARIO 15: Existing password-reset email functionality continues to work
# =============================================================================
def test_scenario_15_password_reset_email_functionality_unaffected(
    db: Session
):
    email_service.clear_sent_test_emails()

    # Request password reset for demo customer
    res = client.post(
        "/api/v1/customer/auth/forgot-password",
        json={"email": DEMO_CUSTOMER_CONFIG["email"]},
    )
    assert res.status_code in (200, 202), res.text

    emails = email_service.get_sent_test_emails()
    reset_email = next((e for e in emails if "Password" in e["subject"] or "Reset" in e["subject"]), None)
    assert reset_email is not None, "Password reset email must be generated and queued"
    assert reset_email["recipient_email"] == DEMO_CUSTOMER_CONFIG["email"]
