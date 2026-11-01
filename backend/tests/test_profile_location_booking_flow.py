import uuid
import pytest
from datetime import datetime, timezone, timedelta, date, time
from fastapi.testclient import TestClient
from app.main import app
from app.repositories.db import SessionLocal
from app.models.user import User
from app.models.customer import Customer
from app.models.service import Service
from app.models.provider import Provider, ProviderService, Availability
from app.models.oauth import OAuthAccount
from app.core.security import hash_password, create_access_token

client = TestClient(app)


@pytest.fixture
def test_db():
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def catalog_service_and_provider(test_db):
    # Ensure active service exists
    srv = test_db.query(Service).filter(Service.is_active == True).first()
    if not srv:
        srv = Service(
            id=uuid.uuid4(),
            name="Deep Home Cleaning",
            category="Cleaning",
            base_price=999.0,
            is_active=True,
        )
        test_db.add(srv)
        test_db.commit()
        test_db.refresh(srv)

    # Create dedicated verified provider with active slot for reliable test execution
    p_user = User(
        id=uuid.uuid4(),
        email=f"dedicated_prov_{uuid.uuid4().hex[:6]}@example.com",
        password_hash=hash_password("ProviderPass123!"),
        role="provider",
        is_active=True,
    )
    test_db.add(p_user)
    test_db.commit()
    prov = Provider(
        user_id=p_user.id,
        full_name="Dedicated Pro Cleaner",
        category=srv.category,
        is_verified=True,
    )
    test_db.add(prov)

    ps = ProviderService(
        id=uuid.uuid4(),
        provider_id=prov.user_id,
        service_id=srv.id,
        price=srv.base_price,
        active=True
    )
    test_db.add(ps)

    # 5 days in the future to avoid any test seed booking conflicts
    future_dt = datetime.now(timezone.utc) + timedelta(days=5)
    future_date = future_dt.date()
    future_str = future_date.strftime("%Y-%m-%d")

    slot = Availability(
        id=uuid.uuid4(),
        provider_id=prov.user_id,
        slot_date=future_date,
        start_time=time(9, 0),
        end_time=time(19, 0),
        status="FREE",
    )
    test_db.add(slot)
    test_db.commit()

    return srv, prov, future_str


def test_google_signup_incomplete_profile_flow(test_db):
    """A new Google user has no phone number, requiring profile completion."""
    user_id = uuid.uuid4()
    cust_id = uuid.uuid4()
    email = f"google_user_{uuid.uuid4().hex[:6]}@gmail.com"
    u = User(id=user_id, email=email, password_hash=hash_password("pw"), role="customer", is_active=True)
    c = Customer(id=cust_id, user_id=user_id, email=email, full_name="Aman Google", phone=None, is_verified=True, is_active=True)
    test_db.add(u)
    test_db.add(c)
    test_db.commit()

    # Pending profile token
    pending_token = create_access_token({
        "sub": str(user_id),
        "role": "customer",
        "customer_id": str(cust_id),
        "email": email,
        "jti": f"jwt_{uuid.uuid4().hex}",
        "pending_profile": True,
    })

    # 1. Pending token is blocked from placing orders
    blocked_res = client.post(
        "/api/v1/customer/bookings",
        headers={"Authorization": f"Bearer {pending_token}"},
        json={"service_id": str(uuid.uuid4()), "scheduled_date": "2026-10-15", "scheduled_time": "10:00"}
    )
    assert blocked_res.status_code == 403
    assert "Profile onboarding incomplete" in blocked_res.json().get("detail", "")

    # 2. Complete profile validates phone number (must be >= 10 digits)
    invalid_phone_res = client.post(
        "/api/v1/customer/auth/complete-profile",
        headers={"Authorization": f"Bearer {pending_token}"},
        json={"full_name": "Aman Google", "phone": "12345"}
    )
    assert invalid_phone_res.status_code in [400, 422]

    # 3. Successful complete profile issues unrestricted session
    valid_res = client.post(
        "/api/v1/customer/auth/complete-profile",
        headers={"Authorization": f"Bearer {pending_token}"},
        json={
            "full_name": "Aman Google Kumar",
            "phone": "+91 9876543210",
            "location": {
                "address": "101, Galaxy Tower, Bodakdev",
                "city": "Ahmedabad",
                "state": "Gujarat",
                "postal_code": "380054",
                "latitude": 23.0338,
                "longitude": 72.5850,
                "source": "geolocation"
            }
        }
    )
    assert valid_res.status_code == 200
    data = valid_res.json()
    assert data["requires_profile_completion"] is False
    assert data["is_profile_complete"] is True
    assert data["location"]["city"] == "Ahmedabad"
    assert data["phone"] == "9876543210" or data["phone"] == "+919876543210"

    # Profile in DB is updated
    test_db.refresh(c)
    assert c.phone is not None
    assert isinstance(c.preferences, dict)
    assert c.preferences["location"]["city"] == "Ahmedabad"


def test_skip_profile_retains_incomplete_status_and_allows_browsing(test_db):
    """Skipping profile completion allows browsing dashboard/catalog but keeps is_profile_complete False."""
    user_id = uuid.uuid4()
    cust_id = uuid.uuid4()
    email = f"skip_user_{uuid.uuid4().hex[:6]}@gmail.com"
    u = User(id=user_id, email=email, password_hash=hash_password("pw"), role="customer", is_active=True)
    c = Customer(id=cust_id, user_id=user_id, email=email, full_name="Skip Customer", phone=None, is_verified=True, is_active=True)
    test_db.add(u)
    test_db.add(c)
    test_db.commit()

    pending_token = create_access_token({
        "sub": str(user_id),
        "role": "customer",
        "customer_id": str(cust_id),
        "email": email,
        "jti": f"jwt_{uuid.uuid4().hex}",
        "pending_profile": True,
    })

    # Call POST /customer/auth/skip-profile
    skip_res = client.post(
        "/api/v1/customer/auth/skip-profile",
        headers={"Authorization": f"Bearer {pending_token}"},
        json={
            "location": {
                "address": "Near Alpha Mall",
                "city": "Ahmedabad",
                "postal_code": "380054"
            }
        }
    )
    assert skip_res.status_code == 200
    skip_data = skip_res.json()
    assert skip_data["requires_profile_completion"] is False
    assert skip_data["is_profile_complete"] is False
    assert "phone" in skip_data["missing_profile_fields"]
    assert skip_data["location"]["city"] == "Ahmedabad"

    browsing_token = skip_data["access_token"]

    # Permitted to browse dashboard and get /auth/me
    me_res = client.get("/api/v1/customer/auth/me", headers={"Authorization": f"Bearer {browsing_token}"})
    assert me_res.status_code == 200
    me_data = me_res.json()
    assert me_data["is_profile_complete"] is False
    assert "phone" in me_data["missing_profile_fields"]
    assert me_data["location"]["city"] == "Ahmedabad"

    dash_res = client.get("/api/v1/customer/dashboard", headers={"Authorization": f"Bearer {browsing_token}"})
    assert dash_res.status_code == 200
    dash_data = dash_res.json()
    assert dash_data["is_profile_complete"] is False
    assert dash_data["saved_location"]["city"] == "Ahmedabad"


def test_blocking_order_creation_for_incomplete_profile(test_db, catalog_service_and_provider):
    """A customer with an incomplete profile (e.g. skipped) is strictly blocked from placing orders at backend."""
    srv, prov, tomorrow_str = catalog_service_and_provider

    user_id = uuid.uuid4()
    cust_id = uuid.uuid4()
    email = f"blocked_cust_{uuid.uuid4().hex[:6]}@example.com"
    u = User(id=user_id, email=email, password_hash=hash_password("pw"), role="customer", is_active=True)
    c = Customer(id=cust_id, user_id=user_id, email=email, full_name="Blocked Cust", phone=None, is_verified=True, is_active=True)
    test_db.add(u)
    test_db.add(c)
    test_db.commit()

    token = create_access_token({
        "sub": str(user_id),
        "role": "customer",
        "customer_id": str(cust_id),
        "email": email,
        "jti": f"jwt_{uuid.uuid4().hex}",
        "pending_profile": False,
    })

    # Attempt to place order via /customer/bookings
    order_res = client.post(
        "/api/v1/customer/bookings",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "service_id": str(srv.id),
            "scheduled_date": tomorrow_str,
            "scheduled_time": "10:00:00",
            "address_line1": "104 Sunrise Heights, SG Highway",
            "city": "Ahmedabad",
            "pincode": "380054"
        }
    )
    assert order_res.status_code == 403
    err_detail = order_res.json().get("detail", {})
    assert err_detail.get("code") == "PROFILE_INCOMPLETE"
    assert "phone" in err_detail.get("missing_fields", [])


def test_order_creation_allowed_once_mandatory_fields_complete(test_db, catalog_service_and_provider):
    """Once mandatory profile details are completed, customer can successfully create orders."""
    srv, prov, tomorrow_str = catalog_service_and_provider

    user_id = uuid.uuid4()
    cust_id = uuid.uuid4()
    email = f"ready_cust_{uuid.uuid4().hex[:6]}@example.com"
    u = User(id=user_id, email=email, password_hash=hash_password("pw"), role="customer", is_active=True)
    c = Customer(
        id=cust_id,
        user_id=user_id,
        email=email,
        full_name="Priya Patel",
        phone="9876543210",
        is_verified=True,
        is_active=True,
        preferences={"location": {"address": "202 Orchid Whitefield", "city": "Ahmedabad"}}
    )
    test_db.add(u)
    test_db.add(c)
    test_db.commit()

    token = create_access_token({
        "sub": str(user_id),
        "role": "customer",
        "customer_id": str(cust_id),
        "email": email,
        "jti": f"jwt_{uuid.uuid4().hex}",
        "pending_profile": False,
    })

    order_res = client.post(
        "/api/v1/customer/bookings",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "service_id": str(srv.id),
            "scheduled_date": tomorrow_str,
            "scheduled_time": "10:00:00",
            "address_line1": "202 Orchid Whitefield, SG Road",
            "city": "Ahmedabad",
            "pincode": "380054"
        }
    )
    if order_res.status_code != 200:
        print("ORDER_RES ERROR:", order_res.status_code, order_res.json())
    assert order_res.status_code == 200
    data = order_res.json()
    assert data["booking_reference"].startswith("BK-")
    assert data["status"] == "Requested"


def test_location_persistence_and_update(test_db):
    """Updating location persists to customer preferences and reflects on dashboard."""
    user_id = uuid.uuid4()
    cust_id = uuid.uuid4()
    email = f"loc_cust_{uuid.uuid4().hex[:6]}@example.com"
    u = User(id=user_id, email=email, password_hash=hash_password("pw"), role="customer", is_active=True)
    c = Customer(id=cust_id, user_id=user_id, email=email, full_name="Location Cust", phone="9876543210", is_verified=True, is_active=True)
    test_db.add(u)
    test_db.add(c)
    test_db.commit()

    token = create_access_token({
        "sub": str(user_id),
        "role": "customer",
        "customer_id": str(cust_id),
        "email": email,
        "jti": f"jwt_{uuid.uuid4().hex}",
    })

    # Update location
    loc_res = client.post(
        "/api/v1/customer/profile/location",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "address": "402, Shivalik Highstreet, Keshavbaug",
            "city": "Ahmedabad",
            "state": "Gujarat",
            "postal_code": "380015",
            "latitude": 23.0258,
            "longitude": 72.5312,
            "source": "geolocation"
        }
    )
    assert loc_res.status_code == 200
    assert loc_res.json()["location"]["city"] == "Ahmedabad"

    # Check dashboard shows actual saved location (not hardcoded)
    dash_res = client.get("/api/v1/customer/dashboard", headers={"Authorization": f"Bearer {token}"})
    assert dash_res.status_code == 200
    assert dash_res.json()["saved_location"]["city"] == "Ahmedabad"
    assert dash_res.json()["saved_location"]["postal_code"] == "380015"


def test_customer_isolation_and_cross_tenant_prevention(test_db):
    """One customer cannot modify or access another customer's profile or location."""
    user1 = User(id=uuid.uuid4(), email=f"cust1_{uuid.uuid4().hex[:6]}@example.com", password_hash=hash_password("pw"), role="customer", is_active=True)
    cust1 = Customer(id=uuid.uuid4(), user_id=user1.id, email=user1.email, full_name="Customer One", phone="9876543210", is_verified=True, is_active=True)

    user2 = User(id=uuid.uuid4(), email=f"cust2_{uuid.uuid4().hex[:6]}@example.com", password_hash=hash_password("pw"), role="customer", is_active=True)
    cust2 = Customer(id=uuid.uuid4(), user_id=user2.id, email=user2.email, full_name="Customer Two", phone="9876543211", is_verified=True, is_active=True)

    test_db.add_all([user1, cust1, user2, cust2])
    test_db.commit()

    token1 = create_access_token({"sub": str(user1.id), "role": "customer", "customer_id": str(cust1.id), "email": user1.email, "jti": f"jwt_{uuid.uuid4().hex}"})

    # When user1 updates location, it only updates cust1
    client.post(
        "/api/v1/customer/profile/location",
        headers={"Authorization": f"Bearer {token1}"},
        json={"city": "Ahmedabad", "address": "Address 1"}
    )

    test_db.refresh(cust1)
    test_db.refresh(cust2)
    assert cust1.preferences["location"]["city"] == "Ahmedabad"
    assert cust2.preferences is None
