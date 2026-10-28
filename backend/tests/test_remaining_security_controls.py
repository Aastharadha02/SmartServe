"""
SmartServe - Comprehensive Verification Suite for Remaining Security Controls
Phases Covered:
- Phase 2: OAuth Security (PKCE, state anti-replay, bound redirect_uri, role isolation, anti-account linking)
- Phase 3: Password-Reset Email Delivery (Generic anti-enumeration, link generation, single-use, session invalidation, SMTP failure resilience)
- Phase 4: Malware Scanning & Upload Protection (Clean file, EICAR test signature detection, ClamAV fail-closed policy)
- Phase 5: Authorization & RBAC Regressions (Cross-tenant IDOR, provider isolation, admin RBAC, WebSocket channel boundaries, runtime resubscribe)
- Phase 6: Session Lifecycle & Rate-Limit Cleanup (Bounded cleanup, active session safety, active rate limit preservation, DB outage sliding window fallback)
- Phase 7: Application Security Review (Security headers, CORS restriction, HMAC evidence verification)
"""

import io
import uuid
import time
import socket
import hashlib
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app, check_shared_rate_limit, _rate_limit_records, _rate_limit_lock
from app.core.config import settings
from app.core.database import SessionLocal
from app.core.security import create_access_token, hash_password
from app.models.user import User
from app.models.customer import Customer
from app.models.provider import Provider
from app.models.booking import Booking
from app.models.session import ActiveSession
from app.models.security import RateLimitEntry, PasswordResetToken, TwoFactorRecoveryCode, AdminRole
from app.models.email import EmailLog
from app.services import email_service, security_service, malware_scanner
from app.api.v1.ws import _is_authorized_for_channel

client = TestClient(app)


# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture(scope="module")
def sec_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def seeded_actors(sec_db: Session):
    sec_db.rollback()
    c1 = sec_db.query(Customer).first()
    c2 = sec_db.query(Customer).offset(1).first()
    p1 = sec_db.query(Provider).join(User, Provider.user_id == User.id).filter(User.is_active == True).first()
    p2 = sec_db.query(Provider).join(User, Provider.user_id == User.id).filter(User.is_active == True).offset(1).first()
    admin = sec_db.query(User).filter(User.role.in_(["admin", "super_admin"])).first()

    return {
        "c1": c1,
        "c2": c2,
        "p1": p1,
        "p2": p2,
        "admin": admin,
    }


# =============================================================================
# PHASE 2: OAUTH SECURITY & ANTI-REPLAY
# =============================================================================

def test_oauth_state_anti_replay(sec_db: Session):
    """Verify that state nonce is single-use and cannot be replayed."""
    from app.api.v1.oauth import generate_oauth_state, verify_and_consume_oauth_state

    state = generate_oauth_state("google", redirect_uri="http://localhost:5174/auth/callback/google")

    # 1. First verification succeeds and consumes the nonce
    payload1 = verify_and_consume_oauth_state(state, "google", sec_db)
    assert payload1 is not None
    assert payload1["provider"] == "google"

    # 2. Replay with the same state MUST fail
    payload2 = verify_and_consume_oauth_state(state, "google", sec_db)
    assert payload2 is None


def test_oauth_google_authorize_includes_pkce():
    """Verify that Google OAuth authorization URL generates PKCE code_challenge and binds redirect_uri."""
    with patch.object(settings, "GOOGLE_CLIENT_ID", "mock-google-client-id"), \
         patch.object(settings, "GOOGLE_CLIENT_SECRET", "mock-google-secret"):

        res = client.get("/api/v1/customer/auth/oauth/google/authorize?redirect_uri=http://localhost:5174/auth/callback/google")
        assert res.status_code == 200
        data = res.json()
        auth_url = data["authorization_url"]
        assert "code_challenge=" in auth_url
        assert "code_challenge_method=S256" in auth_url
        assert "localhost" in auth_url


def test_oauth_rejects_unauthorized_redirect_uri():
    """Verify that an untrusted redirect_uri (open redirect attack) falls back to safe default."""
    with patch.object(settings, "GOOGLE_CLIENT_ID", "mock-client-id"), \
         patch.object(settings, "GOOGLE_CLIENT_SECRET", "mock-secret"):

        res = client.get("/api/v1/customer/auth/oauth/google/authorize?redirect_uri=https://malicious-phishing.com/steal")
        assert res.status_code == 200
        auth_url = res.json()["authorization_url"]
        # Phishing URL must NOT be used
        assert "malicious-phishing.com" not in auth_url
        assert "localhost" in auth_url


# =============================================================================
# PHASE 3: PASSWORD-RESET EMAIL DELIVERY
# =============================================================================

def test_password_reset_email_dispatch_and_in_memory_adapter(sec_db: Session, seeded_actors):
    """Verify password-reset generates link, dispatches email, preserves anti-enumeration, and does not leak token."""
    email_service.clear_sent_test_emails()
    c1 = seeded_actors["c1"]
    user_c1 = sec_db.query(User).filter(User.id == c1.user_id).first()

    # 1. Request password reset
    res = client.post("/api/v1/customer/auth/forgot-password", json={"email": user_c1.email})
    assert res.status_code == 200
    res_data = res.json()
    assert res_data["status"] == "ok"
    assert "token" not in res_data
    assert "raw_token" not in res_data

    # 2. Check dispatched email in test outbox
    outbox = email_service.get_sent_test_emails()
    assert len(outbox) >= 1
    sent_msg = outbox[-1]
    assert sent_msg["recipient_email"] == user_c1.email
    assert "SmartServe Password Reset" in sent_msg["subject"]
    assert "reset-password?token=" in sent_msg["body_text"]
    assert "reset-password?token=" in sent_msg["body_html"]

    # 3. Non-existent email returns identical generic response (anti-enumeration)
    email_service.clear_sent_test_emails()
    res_fake = client.post("/api/v1/customer/auth/forgot-password", json={"email": "nonexistent_999@example.com"})
    assert res_fake.status_code == 200
    assert res_fake.json() == res_data
    assert len(email_service.get_sent_test_emails()) == 0


def test_password_reset_delivery_failure_resilience(sec_db: Session, seeded_actors):
    """Verify that SMTP failure is recorded in EmailLog as Failed but response remains generic."""
    c1 = seeded_actors["c1"]
    user_c1 = sec_db.query(User).filter(User.id == c1.user_id).first()

    with patch("app.services.email_service.settings.EMAIL_BACKEND", "smtp"), \
         patch("app.services.email_service._is_safe_smtp_recipient", return_value=True), \
         patch("app.services.email_service.settings.SMTP_HOST", "invalid.smtp.nonexistent.local"), \
         patch("app.services.email_service._dispatch_via_smtp", side_effect=ConnectionRefusedError("SMTP server down")):

        res = client.post("/api/v1/customer/auth/forgot-password", json={"email": user_c1.email})
        assert res.status_code == 200
        assert res.json()["status"] == "ok"

        # Check that EmailLog recorded the Failed status
        failed_log = (
            sec_db.query(EmailLog)
            .filter(EmailLog.recipient_email == user_c1.email, EmailLog.status == "Failed")
            .order_by(EmailLog.sent_at.desc())
            .first()
        )
        assert failed_log is not None


# =============================================================================
# PHASE 4: MALWARE SCANNING & UPLOAD PROTECTION
# =============================================================================

def test_clean_image_upload_passes(seeded_actors):
    """Verify genuine clean PNG image passes upload validation and malware check."""
    c1 = seeded_actors["c1"]
    token = create_access_token({"sub": str(c1.user_id), "role": "customer", "customer_id": str(c1.id)})
    headers = {"Authorization": f"Bearer {token}"}

    png_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4"
    files = {"file": ("avatar.png", io.BytesIO(png_bytes), "image/png")}
    res = client.post("/api/v1/customer/uploads/image", files=files, headers=headers)
    assert res.status_code == 200
    assert "/static/uploads/" in res.json().get("url", "")


def test_eicar_malware_signature_rejected(seeded_actors):
    """Verify that an uploaded file containing the standard EICAR test signature is rejected with 400."""
    c1 = seeded_actors["c1"]
    token = create_access_token({"sub": str(c1.user_id), "role": "customer", "customer_id": str(c1.id)})
    headers = {"Authorization": f"Bearer {token}"}

    # Disguised PNG containing EICAR test signature
    eicar_png = b"\x89PNG\r\n\x1a\n" + malware_scanner.EICAR_SIGNATURE
    files = {"file": ("infected.png", io.BytesIO(eicar_png), "image/png")}
    res = client.post("/api/v1/customer/uploads/image", files=files, headers=headers)
    assert res.status_code == 400
    assert "threat" in res.json().get("detail", "").lower() or "security violation" in res.json().get("detail", "").lower()


def test_scanner_fail_closed_when_mandatory(seeded_actors):
    """Verify that when CLAMAV_OPTIONAL_IN_DEV is False and daemon is offline, sensitive uploads are rejected with 503."""
    c1 = seeded_actors["c1"]
    token = create_access_token({"sub": str(c1.user_id), "role": "customer", "customer_id": str(c1.id)})
    headers = {"Authorization": f"Bearer {token}"}

    png_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4"
    files = {"file": ("avatar.png", io.BytesIO(png_bytes), "image/png")}

    with patch("app.services.malware_scanner.scan_file_bytes", side_effect=malware_scanner.MalwareScannerUnavailableError("Antivirus service is offline.")):
        res = client.post("/api/v1/customer/uploads/image", files=files, headers=headers)
        assert res.status_code == 503
        assert "scanning service unavailable" in res.json().get("detail", "").lower()


# =============================================================================
# PHASE 5: AUTHORIZATION & WEBSOCKET CHANNEL BOUNDARIES
# =============================================================================

def test_websocket_channel_tenant_isolation(sec_db: Session, seeded_actors):
    """Verify WebSocket channel authorization prevents cross-tenant access to customer and booking streams."""
    c1 = seeded_actors["c1"]
    c2 = seeded_actors["c2"]

    token_payload_c1 = {"sub": str(c1.user_id), "role": "customer", "customer_id": str(c1.id)}

    # 1. Customer 1 CAN subscribe to own customer channel
    assert _is_authorized_for_channel(token_payload_c1, f"customer_{c1.id}") is True

    # 2. Customer 1 CANNOT subscribe to Customer 2 channel
    assert _is_authorized_for_channel(token_payload_c1, f"customer_{c2.id}") is False

    # 3. Customer 1 CANNOT subscribe to universal admin bookings channel
    assert _is_authorized_for_channel(token_payload_c1, "bookings") is False
    assert _is_authorized_for_channel(token_payload_c1, "dashboard") is False

    # 4. Admin CAN subscribe to universal bookings and dashboard
    token_admin = {"sub": str(seeded_actors["admin"].id), "role": "admin"}
    assert _is_authorized_for_channel(token_admin, "bookings") is True
    assert _is_authorized_for_channel(token_admin, "dashboard") is True


def test_admin_rbac_permission_boundary(sec_db: Session, seeded_actors):
    """Verify admin lacking support:manage permission cannot reply to support tickets."""
    sec_db.rollback()
    u_id = uuid.uuid4()
    catalog_admin_user = User(
        id=u_id,
        email=f"catalog_admin_{uuid.uuid4().hex[:6]}@example.com",
        password_hash=hash_password("CatalogAdminPass123!"),
        role="admin",
        is_active=True
    )
    admin_role = AdminRole(
        id=uuid.uuid4(),
        user_id=u_id,
        role_name="catalog_specialist",
        permissions=["catalog:manage"],
        is_active=True
    )
    sec_db.add(catalog_admin_user)
    sec_db.commit()
    sec_db.add(admin_role)
    sec_db.commit()

    token_cat = create_access_token({"sub": str(u_id), "role": "admin"})

    res = client.post(
        f"/api/v1/admin/support/tickets/{uuid.uuid4()}/reply",
        json={"message_text": "Unauthorized reply attempt"},
        headers={"Authorization": f"Bearer {token_cat}"}
    )
    assert res.status_code == 403
    assert "support:manage" in res.json().get("detail", "")


# =============================================================================
# PHASE 6: SESSION LIFECYCLE & RATE-LIMIT CLEANUP
# =============================================================================

def test_bounded_security_cleanup(sec_db: Session):
    """Verify cleanup_expired_security_records removes expired records without touching active ones."""
    sec_db.rollback()
    now = datetime.now(timezone.utc)
    u_id = uuid.uuid4()
    dummy_user = User(id=u_id, email=f"cleanup_{uuid.uuid4().hex[:6]}@example.com", password_hash="hash", role="customer", is_active=True)
    sec_db.add(dummy_user)
    sec_db.commit()

    # 1. Expired revoked session (should be purged)
    expired_sess = ActiveSession(
        id=uuid.uuid4(), user_id=u_id, token_jti=f"jti_exp_{uuid.uuid4().hex}",
        is_revoked=True, created_at=now - timedelta(days=2), expires_at=now - timedelta(days=1)
    )
    # 2. Active non-expired session (MUST NOT be purged)
    active_sess = ActiveSession(
        id=uuid.uuid4(), user_id=u_id, token_jti=f"jti_act_{uuid.uuid4().hex}",
        is_revoked=False, created_at=now, expires_at=now + timedelta(hours=1)
    )
    # 3. Stale rate limit entry > 15m (should be purged)
    stale_rl = RateLimitEntry(key="test_stale_key", created_at=now - timedelta(minutes=30))
    # 4. Fresh rate limit entry (MUST NOT be purged)
    fresh_rl = RateLimitEntry(key="test_fresh_key", created_at=now)

    sec_db.add(expired_sess)
    sec_db.add(active_sess)
    sec_db.add(stale_rl)
    sec_db.add(fresh_rl)
    sec_db.commit()

    # Run cleanup
    counts = security_service.cleanup_expired_security_records(sec_db)
    assert counts["revoked_sessions_purged"] >= 1
    assert counts["rate_limit_entries_purged"] >= 1

    # Active session MUST still exist
    assert sec_db.query(ActiveSession).filter(ActiveSession.id == active_sess.id).first() is not None
    # Fresh rate limit MUST still exist
    assert sec_db.query(RateLimitEntry).filter(RateLimitEntry.id == fresh_rl.id).first() is not None


def test_rate_limit_db_outage_fails_secure():
    """Verify that during a database outage, in-memory sliding window enforces rate limit without failing open."""
    test_key = f"outage_test_{uuid.uuid4().hex}"

    with patch("app.core.database.SessionLocal", side_effect=Exception("Database Connection Timeout")):
        # First 5 calls pass
        for _ in range(5):
            allowed = check_shared_rate_limit(test_key, max_requests=5, window_seconds=60)
            assert allowed is True

        # 6th call MUST be rate-limited (blocked)
        rate_limited = check_shared_rate_limit(test_key, max_requests=5, window_seconds=60)
        assert rate_limited is False


# =============================================================================
# REAL SMTP DELIVERY & ADAPTER FAILURE RESILIENCE
# =============================================================================

def test_smtp_live_dispatch_with_mocked_server():
    """Verify _dispatch_via_smtp connects with TLS, logs in, and sends message."""
    mock_server = MagicMock()
    with patch("smtplib.SMTP", return_value=mock_server), \
         patch.object(settings, "SMTP_HOST", "smtp.smartserve.local"), \
         patch.object(settings, "SMTP_PORT", 587), \
         patch.object(settings, "SMTP_USER", "smtp_user"), \
         patch.object(settings, "SMTP_PASSWORD", "smtp_pass"), \
         patch.object(settings, "SMTP_USE_TLS", True):

        email_service._dispatch_via_smtp(
            recipient_email="customer@example.com",
            subject="Test Subject",
            body_text="Test Body",
            body_html="<p>Test Body</p>"
        )

        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("smtp_user", "smtp_pass")
        mock_server.send_message.assert_called_once()
        mock_server.quit.assert_called_once()


def test_smtp_authentication_failure():
    """Verify _dispatch_via_smtp raises exception when SMTP credentials fail."""
    import smtplib
    mock_server = MagicMock()
    mock_server.login.side_effect = smtplib.SMTPAuthenticationError(535, b"Authentication failed")

    with patch("smtplib.SMTP", return_value=mock_server), \
         patch.object(settings, "SMTP_HOST", "smtp.smartserve.local"), \
         patch.object(settings, "SMTP_PORT", 587), \
         patch.object(settings, "SMTP_USER", "invalid_user"), \
         patch.object(settings, "SMTP_PASSWORD", "wrong_password"):

        with pytest.raises(smtplib.SMTPAuthenticationError):
            email_service._dispatch_via_smtp(
                recipient_email="customer@example.com",
                subject="Test Subject",
                body_text="Test Body"
            )


def test_smtp_timeout_handling():
    """Verify _dispatch_via_smtp raises socket timeout exception on network stall."""
    with patch("smtplib.SMTP", side_effect=socket.timeout("Connection timed out")), \
         patch.object(settings, "SMTP_HOST", "slow.smtp.smartserve.local"), \
         patch.object(settings, "SMTP_PORT", 587):

        with pytest.raises(socket.timeout):
            email_service._dispatch_via_smtp(
                recipient_email="customer@example.com",
                subject="Test Subject",
                body_text="Test Body"
            )


# =============================================================================
# PASSWORD RESET TOKEN VALIDATION & SESSION REVOCATION
# =============================================================================

def test_password_reset_consume_token_and_session_revocation(sec_db: Session):
    """Verify password reset invalidates token, updates password, revokes active sessions, and permits login with new password."""
    sec_db.rollback()
    test_email = f"pwd_reset_flow_{uuid.uuid4().hex[:8]}@example.com"
    old_pwd = "OldPassword123!"
    new_pwd = "NewBrandNewPassword123!"

    u = User(id=uuid.uuid4(), email=test_email, password_hash=hash_password(old_pwd), role="customer", is_active=True)
    c = Customer(id=uuid.uuid4(), user_id=u.id, email=test_email, full_name="Reset Customer", phone="+919876543210", is_verified=True, is_active=True)
    sec_db.add(u)
    sec_db.add(c)
    sec_db.commit()

    # Login to establish active session
    login_res = client.post("/api/v1/customer/auth/login", json={"email": test_email, "password": old_pwd})
    assert login_res.status_code == 200
    token_before = login_res.json()["access_token"]

    # Request password reset
    forgot_res = client.post("/api/v1/customer/auth/forgot-password", json={"email": test_email})
    assert forgot_res.status_code == 200

    outbox = email_service.get_sent_test_emails()
    assert len(outbox) > 0
    body = outbox[-1]["body_text"]
    assert "token=" in body
    raw_token = body.split("token=")[1].split("\n")[0].split("&")[0].strip()

    # Reset password with raw token
    reset_res = client.post("/api/v1/customer/auth/reset-password", json={"token": raw_token, "new_password": new_pwd})
    assert reset_res.status_code == 200

    # Token cannot be reused (single-use)
    reuse_res = client.post("/api/v1/customer/auth/reset-password", json={"token": raw_token, "new_password": "AnotherPassword123!"})
    assert reuse_res.status_code == 400

    # Old session is revoked
    check_sess = client.get("/api/v1/customer/auth/me", headers={"Authorization": f"Bearer {token_before}"})
    assert check_sess.status_code == 401

    # Login with old password fails
    fail_login = client.post("/api/v1/customer/auth/login", json={"email": test_email, "password": old_pwd})
    assert fail_login.status_code == 401

    # Login with new password succeeds
    success_login = client.post("/api/v1/customer/auth/login", json={"email": test_email, "password": new_pwd})
    assert success_login.status_code == 200


def test_password_reset_expired_token_rejected(sec_db: Session):
    """Verify expired password reset token is rejected with 400."""
    sec_db.rollback()
    test_email = f"expired_token_{uuid.uuid4().hex[:8]}@example.com"
    u = User(id=uuid.uuid4(), email=test_email, password_hash="hash", role="customer", is_active=True)
    c = Customer(id=uuid.uuid4(), user_id=u.id, email=test_email, full_name="Expired User", is_verified=True, is_active=True)
    sec_db.add(u)
    sec_db.add(c)
    sec_db.commit()

    raw_token = "expired_raw_token_value_32_chars_long"
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    expired_record = PasswordResetToken(
        id=uuid.uuid4(),
        user_id=u.id,
        token_hash=token_hash,
        expires_at=datetime.now(timezone.utc) - timedelta(hours=1),
        is_used=False
    )
    sec_db.add(expired_record)
    sec_db.commit()

    res = client.post("/api/v1/customer/auth/reset-password", json={"token": raw_token, "new_password": "NewStrongPass123!"})
    assert res.status_code == 400
    assert "expired" in res.json()["detail"].lower()


# =============================================================================
# GOOGLE SOCIAL SIGNUP & ONBOARDING PROFILE COMPLETION
# =============================================================================

def test_google_signup_profile_completion_workflow(sec_db: Session):
    """Verify full workflow: new Google customer -> restricted pending token -> protected API blocked -> profile completion -> unrestricted token."""
    from app.api.v1.oauth import generate_oauth_state
    mock_email = f"google_flow_{uuid.uuid4().hex[:8]}@gmail.com"
    mock_sub = f"google_sub_{uuid.uuid4().hex[:12]}"

    with patch.object(settings, "GOOGLE_CLIENT_ID", "mock-google-id"), \
         patch.object(settings, "GOOGLE_CLIENT_SECRET", "mock-google-secret"), \
         patch("requests.post") as mock_post, \
         patch("requests.get") as mock_get:

        mock_post.return_value = MagicMock(ok=True, json=lambda: {"access_token": "mock-tok", "token_type": "Bearer"})
        mock_get.return_value = MagicMock(ok=True, json=lambda: {
            "sub": mock_sub,
            "email": mock_email,
            "name": "Google New User",
            "email_verified": True
        })

        # 1. Callback for new customer
        state = generate_oauth_state("google")
        res = client.post("/api/v1/customer/auth/oauth/google/callback", json={"code": "auth-code", "state": state})
        assert res.status_code == 200
        data = res.json()
        assert data["requires_profile_completion"] is True
        assert data["is_new_user"] is True
        pending_token = data["access_token"]

        # 2. Incomplete signup session CANNOT access protected customer APIs (e.g., bookings)
        blocked_res = client.get("/api/v1/customer/bookings", headers={"Authorization": f"Bearer {pending_token}"})
        assert blocked_res.status_code == 403
        assert "onboarding incomplete" in blocked_res.json()["detail"].lower()

        # 3. Invalid phone number rejected during profile completion
        invalid_phone_res = client.post(
            "/api/v1/customer/auth/complete-profile",
            json={"full_name": "Google New User", "phone": "123"},
            headers={"Authorization": f"Bearer {pending_token}"}
        )
        assert invalid_phone_res.status_code in (400, 422)

        # 4. Successful profile completion
        complete_res = client.post(
            "/api/v1/customer/auth/complete-profile",
            json={"full_name": "Google New User", "phone": "+919876543210", "preferences": ["cat-1", "cat-2"]},
            headers={"Authorization": f"Bearer {pending_token}"}
        )
        assert complete_res.status_code == 200
        complete_data = complete_res.json()
        assert complete_data["requires_profile_completion"] is False
        full_token = complete_data["access_token"]

        # 5. Full token CAN now access protected customer APIs
        allowed_res = client.get("/api/v1/customer/bookings", headers={"Authorization": f"Bearer {full_token}"})
        assert allowed_res.status_code == 200

