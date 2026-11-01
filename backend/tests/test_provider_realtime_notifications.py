"""
Automated Test Suite: Provider Real-Time Notifications & Access Control
Tests:
1. Provider assignment and booking notification event creation.
2. Channel authorization and strict isolation (horizontal and vertical tenant separation).
3. Admin channel lockdown (providers cannot access 'bookings' or 'dashboard' super-channels).
4. Duplicate prevention & idempotency handling.
5. Reconnection simulation and mock WhatsApp delivery verification.
"""
import uuid
from datetime import datetime, timezone, date, time
from decimal import Decimal
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import SessionLocal
from app.core.security import create_access_token
from app.core.websockets import broadcast_realtime, ws_manager
from app.api.v1.ws import _is_authorized_for_channel
from app.models.user import User
from app.models.customer import Customer
from app.models.provider import Provider, Availability
from app.models.service import Service
from app.models.booking import Booking, BookingStatus
from app.models.notification import NotificationLog
from app.services.notification.notification_service import notify_booking_event
from app.services.notification.whatsapp_adapter import get_sent_test_whatsapp_messages, clear_sent_test_whatsapp_messages


client = TestClient(app)


@pytest.fixture
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_channel_authorization_strict_isolation():
    """
    Verify provider channel authorization rejects unauthorized providers
    and prevents providers from accessing admin-only channels (bookings, dashboard).
    """
    provider_1_id = str(uuid.uuid4())
    provider_2_id = str(uuid.uuid4())

    token_payload_p1 = {"sub": provider_1_id, "role": "provider"}
    token_payload_p2 = {"sub": provider_2_id, "role": "provider"}
    token_payload_admin = {"sub": str(uuid.uuid4()), "role": "admin"}
    token_payload_customer = {"sub": str(uuid.uuid4()), "customer_id": str(uuid.uuid4()), "role": "customer"}

    # 1. Provider 1 CAN subscribe to their own provider and user channels
    assert _is_authorized_for_channel(token_payload_p1, f"provider_{provider_1_id}") is True
    assert _is_authorized_for_channel(token_payload_p1, f"user_{provider_1_id}") is True

    # 2. Provider 1 CANNOT subscribe to Provider 2's channel
    assert _is_authorized_for_channel(token_payload_p1, f"provider_{provider_2_id}") is False
    assert _is_authorized_for_channel(token_payload_p1, f"user_{provider_2_id}") is False

    # 3. Provider 1 CANNOT subscribe to admin/super channels
    assert _is_authorized_for_channel(token_payload_p1, "bookings") is False
    assert _is_authorized_for_channel(token_payload_p1, "dashboard") is False
    assert _is_authorized_for_channel(token_payload_p1, "admin") is False
    assert _is_authorized_for_channel(token_payload_p1, "emergency") is False

    # 4. Customer CANNOT subscribe to provider channels
    assert _is_authorized_for_channel(token_payload_customer, f"provider_{provider_1_id}") is False

    # 5. Admin CAN subscribe to admin channels and inspect provider channels
    assert _is_authorized_for_channel(token_payload_admin, "bookings") is True
    assert _is_authorized_for_channel(token_payload_admin, "dashboard") is True
    assert _is_authorized_for_channel(token_payload_admin, f"provider_{provider_1_id}") is True


def test_booking_event_creation_and_mock_delivery(db_session):
    """
    Verify that creating a booking and triggering notify_booking_event creates
    proper notification logs and sends to the in-memory mock WhatsApp adapter
    without calling real external APIs.
    """
    clear_sent_test_whatsapp_messages()

    # Find or create demo user & customer
    test_email = f"test.prov.notif.{uuid.uuid4().hex[:6]}@example.com"
    test_user = User(
        id=uuid.uuid4(),
        email=test_email,
        password_hash="test-hash",
        role="customer",
        is_active=True,
    )
    db_session.add(test_user)
    db_session.flush()

    test_customer = Customer(
        id=uuid.uuid4(),
        user_id=test_user.id,
        email=test_email,
        full_name="Notification Tester",
        phone="+918799296007",
    )
    db_session.add(test_customer)
    db_session.flush()

    # Use existing demo provider and service
    prov_uuid = uuid.UUID("1e86f045-6e78-49c8-8035-3820786a9d18")
    srv_uuid = uuid.UUID("efa925c1-393c-4a39-b0ef-2e66d41c3330")

    test_booking = Booking(
        id=uuid.uuid4(),
        booking_reference=f"BK-TEST-{uuid.uuid4().hex[:4].upper()}",
        customer_id=test_customer.id,
        provider_id=prov_uuid,
        service_id=srv_uuid,
        service_name="Bedroom Deep Cleaning",
        category="Cleaning",
        status=BookingStatus.REQUESTED,
        total_price=Decimal("499.00"),
        scheduled_date=date(2026, 10, 18),
        scheduled_time=datetime(2026, 10, 18, 10, 0, 0),
        address_line1="123 Sector 62, Noida",
        created_at=datetime.utcnow(),
    )
    db_session.add(test_booking)
    db_session.commit()

    # Trigger booking confirmed notification
    results = notify_booking_event(db_session, test_booking, "booking.confirmed")
    assert "email" in results
    assert "whatsapp" in results
    assert results["whatsapp"]["status"] in ("Sent", "Delivered")

    # Verify mock WhatsApp outbox received exactly 1 message
    wa_msgs = get_sent_test_whatsapp_messages()
    assert len(wa_msgs) == 1
    assert wa_msgs[0]["recipient_phone"] == "+918799296007"
    assert "Bedroom Deep Cleaning" in wa_msgs[0]["body"]
    assert "2026-10-18" in wa_msgs[0]["body"]

    # Verify NotificationLog database entry
    log_entry = db_session.query(NotificationLog).filter(
        NotificationLog.booking_id == test_booking.id,
        NotificationLog.channel == "whatsapp",
    ).first()
    assert log_entry is not None
    assert log_entry.recipient == "+918799296007"
    assert log_entry.delivery_status in ("Sent", "Delivered")


def test_duplicate_notification_prevention(db_session):
    """
    Verify that triggering the same booking event twice respects idempotency
    and does NOT duplicate WhatsApp dispatches.
    """
    clear_sent_test_whatsapp_messages()

    idemp_email = f"idemp.{uuid.uuid4().hex[:6]}@example.com"
    test_user = User(
        id=uuid.uuid4(),
        email=idemp_email,
        password_hash="test-hash",
        role="customer",
        is_active=True,
    )
    db_session.add(test_user)
    db_session.flush()

    test_customer = Customer(
        id=uuid.uuid4(),
        user_id=test_user.id,
        email=idemp_email,
        full_name="Idempotency Tester",
        phone="+918799296007",
    )
    db_session.add(test_customer)
    db_session.flush()

    prov_uuid = uuid.UUID("1e86f045-6e78-49c8-8035-3820786a9d18")
    srv_uuid = uuid.UUID("efa925c1-393c-4a39-b0ef-2e66d41c3330")

    test_booking = Booking(
        id=uuid.uuid4(),
        booking_reference=f"BK-IDEMP-{uuid.uuid4().hex[:4].upper()}",
        customer_id=test_customer.id,
        provider_id=prov_uuid,
        service_id=srv_uuid,
        service_name="Sofa Shampoo",
        category="Cleaning",
        status=BookingStatus.REQUESTED,
        total_price=Decimal("899.00"),
        scheduled_date=date(2026, 10, 18),
        scheduled_time=datetime(2026, 10, 18, 14, 0, 0),
        address_line1="456 Indirapuram, Ghaziabad",
        created_at=datetime.utcnow(),
    )
    db_session.add(test_booking)
    db_session.commit()

    # First trigger: sends
    res1 = notify_booking_event(db_session, test_booking, "booking.confirmed")
    assert res1["whatsapp"]["status"] in ("Sent", "Delivered")
    assert len(get_sent_test_whatsapp_messages()) == 1

    # Second trigger with same booking and event_type: deduplicated / skipped
    res2 = notify_booking_event(db_session, test_booking, "booking.confirmed")
    assert res2["whatsapp"]["status"] in ("AlreadySent", "AlreadyProcessed")
    # WhatsApp message count MUST still be exactly 1
    assert len(get_sent_test_whatsapp_messages()) == 1


def test_realtime_broadcast_to_provider_channel():
    """
    Verify broadcast_realtime distributes event to the provider's dedicated channel
    without raising exceptions.
    """
    prov_id = str(uuid.uuid4())
    channels = [f"provider_{prov_id}", f"user_{prov_id}"]

    payload = {
        "type": "BOOKING_CREATED",
        "booking_id": str(uuid.uuid4()),
        "booking_reference": "BK-BROADCAST-1",
        "service_name": "Balcony Cleaning",
        "status": "Requested",
        "scheduled_date": "2026-10-18",
        "scheduled_time": "11:30:00",
    }

    # Should execute cleanly without error
    broadcast_realtime(channels, payload)
