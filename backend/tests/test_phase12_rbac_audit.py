"""
SmartServe Phase 12: Comprehensive RBAC Audit Across All Three Roles
Validates server-side authorization enforcement, URL manipulation defense,
IDOR prevention, and cross-role boundary security for:
1. Customer: own profile/bookings/support/feedback/payments only
2. Provider: own profile/services/availability/assigned bookings/earnings + only required customer contact info
3. Admin: operational visibility into providers, slots, bookings, reports without provider-owned record tampering
"""

import uuid
import pytest
from datetime import datetime, date, time
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.database import SessionLocal
from app.models.user import User
from app.models.customer import Customer
from app.models.provider import Provider
from app.models.booking import Booking, BookingStatus, PaymentStatus
from app.models.service import Service
from app.models.support import SupportTicket
from app.core.security import create_access_token


@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture(scope="module")
def rbac_users(db_session: Session):
    # Customer 1 (Aastha Sharma)
    c1_user = db_session.query(User).filter(User.email == "customer@example.com").first()
    assert c1_user is not None, "Customer 1 user must exist"
    c1_customer = db_session.query(Customer).filter(Customer.user_id == c1_user.id).first()
    assert c1_customer is not None, "Customer 1 profile must exist"
    c1_token = create_access_token({"sub": str(c1_user.id), "role": "customer", "customer_id": str(c1_customer.id)})

    # Customer 2 (Ananya Rao)
    c2_user = db_session.query(User).filter(User.email == "ananya.rao@example.com").first()
    assert c2_user is not None, "Customer 2 user must exist"
    c2_customer = db_session.query(Customer).filter(Customer.user_id == c2_user.id).first()
    assert c2_customer is not None, "Customer 2 profile must exist"
    c2_token = create_access_token({"sub": str(c2_user.id), "role": "customer", "customer_id": str(c2_customer.id)})

    # Provider Amit Kumar
    amit_user = db_session.query(User).filter(User.email == "amit.kumar@smartserve.com").first()
    assert amit_user is not None, "Amit user must exist"
    amit_provider = db_session.query(Provider).filter(Provider.user_id == amit_user.id).first()
    amit_token = create_access_token({"sub": str(amit_user.id), "role": "provider", "email": amit_user.email})

    # Provider Pooja Sharma / Pooja Verma
    pooja_user = db_session.query(User).filter(
        (User.email == "pooja.sharma.demo@gmail.com") | (User.email == "pooja.beauty@smartserve.com")
    ).first()
    assert pooja_user is not None, "Pooja user must exist"
    pooja_provider = db_session.query(Provider).filter(Provider.user_id == pooja_user.id).first()
    pooja_token = create_access_token({"sub": str(pooja_user.id), "role": "provider", "email": pooja_user.email})

    # Admin
    admin_user = db_session.query(User).filter(User.email == "admin@smartserve.com").first()
    assert admin_user is not None, "Admin user must exist"
    admin_token = create_access_token({"sub": str(admin_user.id), "role": "admin", "email": admin_user.email})

    return {
        "c1_user": c1_user,
        "c1_customer": c1_customer,
        "c1_token": c1_token,
        "c2_user": c2_user,
        "c2_customer": c2_customer,
        "c2_token": c2_token,
        "amit_user": amit_user,
        "amit_provider": amit_provider,
        "amit_token": amit_token,
        "pooja_user": pooja_user,
        "pooja_provider": pooja_provider,
        "pooja_token": pooja_token,
        "admin_user": admin_user,
        "admin_token": admin_token,
    }


# ==============================================================================
# 1. UNAUTHENTICATED ACCESS DENIAL
# ==============================================================================

def test_unauthenticated_requests_rejected(client: TestClient):
    """Confirm server-side that protected routes require authentication (401)."""
    endpoints = [
        ("GET", "/api/v1/customer/profile"),
        ("GET", "/api/v1/customer/bookings"),
        ("GET", "/api/v1/customer/support/tickets"),
        ("GET", "/api/v1/providers/me"),
        ("GET", "/api/v1/providers/me/bookings"),
        ("GET", "/api/v1/providers/me/availability"),
        ("GET", "/api/v1/admin/bookings/"),
        ("GET", "/api/v1/admin/providers/"),
        ("GET", "/api/v1/admins/notifications"),
    ]
    for method, path in endpoints:
        if method == "GET":
            res = client.get(path)
        else:
            res = client.post(path, json={})
        assert res.status_code == 401, f"Expected 401 Unauthorized for {method} {path}, got {res.status_code}: {res.text}"
    print("\n[PASS] All 9 protected endpoints strictly reject unauthenticated requests with 401 Unauthorized.")


# ==============================================================================
# 2. CUSTOMER DATA ISOLATION & IDOR DEFENSE
# ==============================================================================

def test_customer_own_profile_and_bookings(client: TestClient, rbac_users: dict):
    """Customer can access own profile and own bookings list."""
    token = rbac_users["c1_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Profile
    res = client.get("/api/v1/customer/profile", headers=headers)
    assert res.status_code == 200, f"Customer profile failed: {res.text}"
    data = res.json()
    assert data["email"] == "customer@example.com"

    # Bookings list
    res_b = client.get("/api/v1/customer/bookings", headers=headers)
    assert res_b.status_code == 200, f"Customer bookings failed: {res_b.text}"
    print("\n[PASS] Customer successfully retrieves own profile and bookings.")


def test_customer_idor_booking_read_forbidden(client: TestClient, db_session: Session, rbac_users: dict):
    """Customer 2 cannot read Customer 1's booking by URL ID manipulation."""
    c1 = rbac_users["c1_customer"]
    c2_token = rbac_users["c2_token"]

    # Find or create a booking for Customer 1
    c1_booking = db_session.query(Booking).filter(Booking.customer_id == c1.id).first()
    if not c1_booking:
        service = db_session.query(Service).filter(Service.is_active == True).first()
        c1_booking = Booking(
            id=uuid.uuid4(),
            booking_reference=f"BK-{uuid.uuid4().hex[:8].upper()}",
            customer_id=c1.id,
            service_id=service.id,
            service_name=service.name,
            category=service.category,
            status=BookingStatus.REQUESTED,
            payment_status=PaymentStatus.PENDING,
            total_price=599.0,
            address="Customer 1 Residence",
            scheduled_date=date.today(),
            scheduled_time=datetime.now(),
        )
        db_session.add(c1_booking)
        db_session.commit()

    # Customer 2 attempts to read Customer 1's booking
    res = client.get(
        f"/api/v1/customer/bookings/{c1_booking.id}",
        headers={"Authorization": f"Bearer {c2_token}"},
    )
    assert res.status_code == 403, f"Expected 403 Forbidden on IDOR read attempt, got {res.status_code}: {res.text}"
    assert "Forbidden" in res.json().get("detail", "")
    print(f"\n[PASS] Customer IDOR read defense verified: Customer 2 blocked (403) from accessing Customer 1 booking {c1_booking.booking_reference}.")


def test_customer_idor_booking_cancel_forbidden(client: TestClient, db_session: Session, rbac_users: dict):
    """Customer 2 cannot cancel Customer 1's booking by URL ID manipulation."""
    c1 = rbac_users["c1_customer"]
    c2_token = rbac_users["c2_token"]

    c1_booking = db_session.query(Booking).filter(Booking.customer_id == c1.id, Booking.status != BookingStatus.CANCELLED).first()
    assert c1_booking is not None, "Customer 1 must have an active booking"
    original_status = c1_booking.status

    # Customer 2 attempts to cancel Customer 1's booking
    res = client.post(
        f"/api/v1/customer/bookings/{c1_booking.id}/cancel",
        headers={"Authorization": f"Bearer {c2_token}"},
        json={"reason": "Malicious cancellation attempt"},
    )
    assert res.status_code == 403, f"Expected 403 Forbidden on IDOR cancel attempt, got {res.status_code}: {res.text}"

    # Verify status in DB was NOT changed
    db_session.refresh(c1_booking)
    assert c1_booking.status == original_status, "Booking status must remain unchanged after unauthorized cancellation attempt"
    print(f"\n[PASS] Customer IDOR cancel defense verified: Unauthorized cancellation rejected with 403, status preserved.")


def test_customer_idor_feedback_forbidden(client: TestClient, db_session: Session, rbac_users: dict):
    """Customer 2 cannot submit feedback for Customer 1's booking."""
    c1 = rbac_users["c1_customer"]
    c2_token = rbac_users["c2_token"]

    c1_booking = db_session.query(Booking).filter(Booking.customer_id == c1.id).first()
    assert c1_booking is not None

    res = client.post(
        f"/api/v1/customer/bookings/{c1_booking.id}/feedback",
        headers={"Authorization": f"Bearer {c2_token}"},
        json={"rating": 1, "review_text": "Unauthorized review"},
    )
    assert res.status_code == 403, f"Expected 403 Forbidden on feedback attempt, got {res.status_code}: {res.text}"
    print("\n[PASS] Customer IDOR feedback defense verified: Rejected with 403 Forbidden.")


def test_customer_support_ticket_isolation(client: TestClient, db_session: Session, rbac_users: dict):
    """Customer 2 cannot view Customer 1's support tickets via URL ID manipulation."""
    c1 = rbac_users["c1_customer"]
    c2_token = rbac_users["c2_token"]

    # Create a test ticket for Customer 1
    t1 = SupportTicket(
        id=uuid.uuid4(),
        customer_id=c1.id,
        subject="Private Support Inquiry C1",
        description="Confidential ticket details",
        category="General",
        status="Open",
        priority="Normal",
        created_at=datetime.utcnow(),
    )
    db_session.add(t1)
    db_session.commit()

    # Customer 2 attempts to read it
    res = client.get(
        f"/api/v1/customer/support/tickets/{t1.id}",
        headers={"Authorization": f"Bearer {c2_token}"},
    )
    assert res.status_code == 404, f"Expected 404 Not Found for cross-customer ticket read, got {res.status_code}: {res.text}"
    print("\n[PASS] Customer support ticket isolation verified: Customer 2 receives 404 Not Found on Customer 1 ticket.")


def test_customer_cannot_escalate_to_provider_endpoints(client: TestClient, rbac_users: dict):
    """Customer role cannot access provider workspace endpoints (403)."""
    c1_token = rbac_users["c1_token"]
    headers = {"Authorization": f"Bearer {c1_token}"}

    endpoints = [
        ("GET", "/api/v1/providers/me"),
        ("GET", "/api/v1/providers/me/services"),
        ("GET", "/api/v1/providers/me/availability"),
        ("GET", "/api/v1/providers/me/bookings"),
        ("GET", "/api/v1/providers/me/dashboard-stats"),
        ("POST", "/api/v1/providers/me/services"),
    ]
    for method, path in endpoints:
        if method == "GET":
            res = client.get(path, headers=headers)
        else:
            res = client.post(path, headers=headers, json={"service_id": str(uuid.uuid4()), "base_price": 500})
        assert res.status_code == 403, f"Expected 403 Forbidden for customer on provider endpoint {path}, got {res.status_code}: {res.text}"
    print("\n[PASS] Customer role strictly prohibited from all provider workspace endpoints (403 Forbidden).")


def test_customer_cannot_escalate_to_admin_endpoints(client: TestClient, rbac_users: dict):
    """Customer role cannot access admin operations or management endpoints (403)."""
    c1_token = rbac_users["c1_token"]
    headers = {"Authorization": f"Bearer {c1_token}"}

    endpoints = [
        ("GET", "/api/v1/admin/bookings/"),
        ("GET", "/api/v1/admin/providers/"),
        ("GET", "/api/v1/admin/customers/"),
        ("GET", "/api/v1/admin/reports/summary"),
        ("POST", "/api/v1/admin/catalog/services"),
    ]
    for method, path in endpoints:
        if method == "GET":
            res = client.get(path, headers=headers)
        else:
            res = client.post(path, headers=headers, json={"name": "Exploit Service", "category": "Test"})
        assert res.status_code == 403, f"Expected 403 Forbidden for customer on admin endpoint {path}, got {res.status_code}: {res.text}"
    print("\n[PASS] Customer role strictly prohibited from all admin management endpoints (403 Forbidden).")


# ==============================================================================
# 3. PROVIDER DATA ISOLATION & RBAC AUDIT
# ==============================================================================

def test_provider_cross_profile_access_forbidden(client: TestClient, rbac_users: dict):
    """Amit Kumar cannot view Pooja Sharma's profile via URL ID manipulation (403)."""
    amit_token = rbac_users["amit_token"]
    pooja_user = rbac_users["pooja_user"]

    res = client.get(
        f"/api/v1/providers/{pooja_user.id}",
        headers={"Authorization": f"Bearer {amit_token}"},
    )
    assert res.status_code == 403, f"Expected 403 Forbidden for cross-provider profile access, got {res.status_code}: {res.text}"
    print("\n[PASS] Provider cross-profile URL tampering blocked: Amit blocked (403) from accessing Pooja's profile.")


def test_provider_cross_availability_access_forbidden(client: TestClient, rbac_users: dict):
    """Amit Kumar cannot view Pooja Sharma's availability schedule via URL ID manipulation (403)."""
    amit_token = rbac_users["amit_token"]
    pooja_user = rbac_users["pooja_user"]

    res = client.get(
        f"/api/v1/providers/{pooja_user.id}/availability",
        headers={"Authorization": f"Bearer {amit_token}"},
    )
    assert res.status_code == 403, f"Expected 403 Forbidden for cross-provider availability access, got {res.status_code}: {res.text}"
    print("\n[PASS] Provider cross-availability schedule URL tampering blocked: Amit blocked (403) from Pooja's availability.")


def test_provider_cross_services_access_forbidden(client: TestClient, rbac_users: dict):
    """Amit Kumar cannot view Pooja Sharma's customized services via URL ID manipulation (403)."""
    amit_token = rbac_users["amit_token"]
    pooja_user = rbac_users["pooja_user"]

    res = client.get(
        f"/api/v1/providers/{pooja_user.id}/services",
        headers={"Authorization": f"Bearer {amit_token}"},
    )
    assert res.status_code == 403, f"Expected 403 Forbidden for cross-provider services access, got {res.status_code}: {res.text}"
    print("\n[PASS] Provider cross-services URL tampering blocked: Amit blocked (403) from Pooja's services.")


def test_provider_cross_booking_access_and_transition_forbidden(client: TestClient, db_session: Session, rbac_users: dict):
    """Amit Kumar cannot view or transition a booking assigned strictly to Pooja Sharma (403)."""
    amit_token = rbac_users["amit_token"]
    pooja_user = rbac_users["pooja_user"]

    # Find a booking assigned to Pooja
    pooja_booking = (
        db_session.query(Booking)
        .filter(Booking.provider_id == pooja_user.id)
        .first()
    )
    assert pooja_booking is not None, "Pooja must have an assigned booking from prior phases"

    # 1. Amit attempts to read Pooja's booking
    res_read = client.get(
        f"/api/v1/providers/me/bookings/{pooja_booking.id}",
        headers={"Authorization": f"Bearer {amit_token}"},
    )
    assert res_read.status_code == 403, f"Expected 403 Forbidden on reading other provider's booking, got {res_read.status_code}: {res_read.text}"

    # 2. Amit attempts to accept Pooja's booking
    res_accept = client.post(
        f"/api/v1/providers/me/bookings/{pooja_booking.id}/accept",
        headers={"Authorization": f"Bearer {amit_token}"},
    )
    assert res_accept.status_code == 403, f"Expected 403 Forbidden on accepting other provider's booking, got {res_accept.status_code}: {res_accept.text}"

    # 3. Amit attempts to start Pooja's booking
    res_start = client.post(
        f"/api/v1/providers/me/bookings/{pooja_booking.id}/start",
        headers={"Authorization": f"Bearer {amit_token}"},
    )
    assert res_start.status_code == 403, f"Expected 403 Forbidden on starting other provider's booking, got {res_start.status_code}: {res_start.text}"

    # 4. Amit attempts to complete Pooja's booking
    res_complete = client.post(
        f"/api/v1/providers/me/bookings/{pooja_booking.id}/complete",
        headers={"Authorization": f"Bearer {amit_token}"},
    )
    assert res_complete.status_code == 403, f"Expected 403 Forbidden on completing other provider's booking, got {res_complete.status_code}: {res_complete.text}"

    print(f"\n[PASS] Provider cross-booking tampering defense verified: Amit blocked (403) from reading or transitioning Pooja's booking {pooja_booking.booking_reference}.")


def test_provider_booking_data_minimization(client: TestClient, db_session: Session, rbac_users: dict):
    """Assigned booking exposes only customer info required for the job (name, phone, address)."""
    amit_token = rbac_users["amit_token"]
    amit_user = rbac_users["amit_user"]

    amit_booking = (
        db_session.query(Booking)
        .filter(Booking.provider_id == amit_user.id)
        .first()
    )
    assert amit_booking is not None, "Amit must have an assigned booking"

    res = client.get(
        f"/api/v1/providers/me/bookings/{amit_booking.id}",
        headers={"Authorization": f"Bearer {amit_token}"},
    )
    assert res.status_code == 200, f"Failed to get assigned booking: {res.text}"
    data = res.json()

    # Allowed operational customer fields
    assert "customer_name" in data
    assert "customer_phone" in data
    assert "address" in data

    # Ensure sensitive user fields are NOT leaked in response
    assert "password" not in data
    assert "hashed_password" not in data
    assert "token" not in data
    assert "user" not in data
    print("\n[PASS] Provider booking view enforces data minimization: only job-required customer info exposed.")


def test_provider_cannot_access_customer_endpoints(client: TestClient, rbac_users: dict):
    """Provider role cannot access customer endpoints (403)."""
    amit_token = rbac_users["amit_token"]
    headers = {"Authorization": f"Bearer {amit_token}"}

    endpoints = [
        ("GET", "/api/v1/customer/profile"),
        ("GET", "/api/v1/customer/bookings"),
        ("GET", "/api/v1/customer/support/tickets"),
        ("POST", "/api/v1/customer/sessions/revoke-all"),
    ]
    for method, path in endpoints:
        if method == "GET":
            res = client.get(path, headers=headers)
        else:
            res = client.post(path, headers=headers)
        assert res.status_code == 403, f"Expected 403 Forbidden for provider on customer endpoint {path}, got {res.status_code}: {res.text}"
        assert "Customer role required" in res.json().get("detail", "")
    print("\n[PASS] Provider strictly prohibited from customer endpoints (403 Forbidden - Customer role required).")


def test_provider_cannot_modify_admin_catalog(client: TestClient, rbac_users: dict):
    """Provider role cannot access admin routes or alter master catalog (403)."""
    amit_token = rbac_users["amit_token"]
    headers = {"Authorization": f"Bearer {amit_token}"}

    endpoints = [
        ("GET", "/api/v1/admin/bookings/"),
        ("POST", "/api/v1/admin/catalog/services"),
        ("PUT", f"/api/v1/admin/catalog/services/{uuid.uuid4()}"),
        ("GET", "/api/v1/admin/reports/summary"),
    ]
    for method, path in endpoints:
        if method == "GET":
            res = client.get(path, headers=headers)
        elif method == "POST":
            res = client.post(path, headers=headers, json={"name": "Hacked Service"})
        else:
            res = client.put(path, headers=headers, json={"name": "Hacked Service"})
        assert res.status_code == 403, f"Expected 403 Forbidden for provider on admin endpoint {path}, got {res.status_code}: {res.text}"
    print("\n[PASS] Provider strictly prohibited from admin operations & catalog modification (403 Forbidden).")


# ==============================================================================
# 4. ADMIN OPERATIONAL VISIBILITY & GOVERNANCE
# ==============================================================================

def test_admin_full_operational_visibility(client: TestClient, rbac_users: dict):
    """Admin has full operational visibility into providers, slots, bookings, and reports."""
    admin_token = rbac_users["admin_token"]
    headers = {"Authorization": f"Bearer {admin_token}"}
    amit_provider = rbac_users["amit_provider"]

    # 1. Admin can list all bookings
    res_b = client.get("/api/v1/admin/bookings/", headers=headers)
    assert res_b.status_code == 200, f"Admin list bookings failed: {res_b.text}"
    assert len(res_b.json()) > 0

    # 2. Admin can view provider detail
    res_p = client.get(f"/api/v1/admin/providers/{amit_provider.user_id}", headers=headers)
    assert res_p.status_code == 200, f"Admin view provider failed: {res_p.text}"
    p_data = res_p.json()
    assert p_data["full_name"] == "Amit Kumar"

    # 3. Admin can view provider availability slots
    res_s = client.get(f"/api/v1/admin/providers/{amit_provider.user_id}/slots", headers=headers)
    assert res_s.status_code == 200, f"Admin view provider slots failed: {res_s.text}"

    # 4. Admin can access system reports
    res_rep = client.get("/api/v1/admin/reports/summary", headers=headers)
    assert res_rep.status_code == 200, f"Admin reports failed: {res_rep.text}"

    print("\n[PASS] Admin has complete operational visibility into bookings, providers, slots, and system reports.")
