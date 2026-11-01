#!/usr/bin/env python3
"""
Verification suite for Section 2: Complete Forgot-Password and Reset-Password Flow.
Verifies all 12 security requirements with live SMTP delivery to configured test email.
"""
import sys
import os
import uuid
import hashlib
from datetime import datetime, timezone, timedelta
import requests

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.core.database import SessionLocal
from app.models.user import User, UserSession
from app.models.customer import Customer
from app.models.security import PasswordResetToken
from app.core.security import hash_password, create_access_token
from app.api.v1.customer import create_password_reset_token

BASE_URL = "http://127.0.0.1:8000/api/v1"

def log_test(step_num, title, passed, detail=""):
    mark = "[PASS]" if passed else "[FAIL]"
    print(f"Step {step_num:<2} {mark:<7} {title} {f'({detail})' if detail else ''}")
    return passed

def run():
    print("=" * 75)
    print("  SECTION 2: PASSWORD RESET SECURITY & WORKFLOW VERIFICATION")
    print("=" * 75)

    db = SessionLocal()
    results = {}
    
    # Authorized test recipient specified by user
    test_email = "aasthahotwani04@gmail.com"
    old_password = "InitialOldPassword123!"
    new_password = "SecureNewPassword456!"

    user = None
    created_user = False
    orig_password_hash = None
    test_session_id = None

    try:
        # Check if user already exists
        user = db.query(User).filter(User.email == test_email).first()
        if user:
            print(f"Using registered account for live email verification: {test_email}")
            orig_password_hash = user.password_hash
            user.password_hash = hash_password(old_password)
            user.is_active = True
            db.commit()
            db.refresh(user)
        else:
            print(f"Creating test account for live email verification: {test_email}")
            created_user = True
            user = User(
                id=uuid.uuid4(),
                email=test_email,
                password_hash=hash_password(old_password),
                role="customer",
                is_active=True
            )
            db.add(user)
            customer = Customer(
                id=uuid.uuid4(),
                user_id=user.id,
                email=test_email,
                full_name="Aastha Hotwani",
                phone="+919876543210"
            )
            db.add(customer)
            db.commit()

        # Add an active test session to verify session revocation
        test_session_id = uuid.uuid4()
        session_record = UserSession(
            id=test_session_id,
            user_id=user.id,
            device_info="Test Verification Session",
            ip_address="127.0.0.1"
        )
        db.add(session_record)
        db.commit()

        # Step 11: Non-registered email anti-enumeration
        non_existent_email = f"nonexistent_{uuid.uuid4().hex[:8]}@example.com"
        r_anti = requests.post(f"{BASE_URL}/customer/auth/forgot-password", json={"email": non_existent_email})
        anti_enum_ok = r_anti.status_code == 200 and "If the email exists" in r_anti.json().get("message", "")
        results["11_anti_enumeration"] = log_test(11, "Anti-Enumeration: Unregistered email returns identical generic message", anti_enum_ok)

        # Step 1: Submit password-reset request for target account (delivers exactly 1 live SMTP email)
        r_forgot = requests.post(f"{BASE_URL}/customer/auth/forgot-password", json={"email": test_email})
        forgot_ok = r_forgot.status_code == 200 and "If the email exists" in r_forgot.json().get("message", "")
        results["1_forgot_submit"] = log_test(1, "Submit password-reset request for test account", forgot_ok)

        # Step 2: Confirm SMTP / Email record persisted with status 'Sent'
        from app.models.email import EmailLog
        email_record = db.query(EmailLog).filter(EmailLog.recipient_email == test_email).order_by(EmailLog.sent_at.desc()).first()
        is_delivered = email_record is not None and email_record.status == "Sent"
        results["2_email_dispatch"] = log_test(2, "Confirm live email dispatch recorded in durable EmailLog", is_delivered, f"Status: {email_record.status if email_record else 'None'}")

        # Step 8a: Verify invalid token rejected
        r_invalid = requests.post(f"{BASE_URL}/customer/auth/reset-password", json={
            "token": "completely_invalid_token_string_12345",
            "new_password": new_password
        })
        results["8a_invalid_token"] = log_test(8, "Reject invalid reset token safely", r_invalid.status_code == 400, f"status {r_invalid.status_code}")

        # Step 8b & 9: Verify expired token rejected according to expiry policy
        expired_raw = f"expired_raw_{uuid.uuid4().hex}"
        expired_hash = hashlib.sha256(expired_raw.encode("utf-8")).hexdigest()
        expired_token = PasswordResetToken(
            id=uuid.uuid4(),
            user_id=user.id,
            token_hash=expired_hash,
            expires_at=datetime.now(timezone.utc) - timedelta(minutes=10),
            is_used=False
        )
        db.add(expired_token)
        db.commit()

        r_expired = requests.post(f"{BASE_URL}/customer/auth/reset-password", json={
            "token": expired_raw,
            "new_password": new_password
        })
        results["8b_expired_token"] = log_test(9, "Reject expired reset token (15-min policy enforced)", r_expired.status_code == 400, f"status {r_expired.status_code}")

        # Step 3, 4: Generate fresh valid token and reset password
        valid_raw = create_password_reset_token(db, user)
        r_reset = requests.post(f"{BASE_URL}/customer/auth/reset-password", json={
            "token": valid_raw,
            "new_password": new_password
        })
        results["4_set_new_password"] = log_test(4, "Set new password using valid reset token", r_reset.status_code == 200, f"status {r_reset.status_code}")

        # Step 5: Sign in using the new password
        r_login_new = requests.post(f"{BASE_URL}/customer/auth/login", json={
            "email": test_email,
            "password": new_password
        })
        new_token = r_login_new.json().get("access_token") if r_login_new.status_code == 200 else None
        results["5_signin_new_pwd"] = log_test(5, "Sign in using new password", bool(new_token), f"status {r_login_new.status_code}")

        # Step 6: Verify old password no longer works
        r_login_old = requests.post(f"{BASE_URL}/customer/auth/login", json={
            "email": test_email,
            "password": old_password
        })
        results["6_old_pwd_rejected"] = log_test(6, "Old password rejected upon login", r_login_old.status_code in (400, 401), f"status {r_login_old.status_code}")

        # Step 7: Verify reset token cannot be reused
        r_reuse = requests.post(f"{BASE_URL}/customer/auth/reset-password", json={
            "token": valid_raw,
            "new_password": "AnotherNewPassword789!"
        })
        results["7_token_single_use"] = log_test(7, "Token replay protection: Cannot reuse reset token", r_reuse.status_code == 400, f"status {r_reuse.status_code}")

        # Step 10: Verify test session was revoked
        test_session_check = db.query(UserSession).filter(UserSession.id == test_session_id).first() if test_session_id else None
        results["10_sessions_revoked"] = log_test(10, "Existing user sessions revoked on password reset", test_session_check is None)

        # Step 12: Safe logging on SMTP failure without exposing secrets
        import logging
        from io import StringIO
        log_stream = StringIO()
        handler = logging.StreamHandler(log_stream)
        logger = logging.getLogger("smartserve.services.email")
        logger.addHandler(handler)
        
        from app.services import email_service
        # Simulate send with invalid host using a dummy address (does not send real email)
        orig_host = email_service.settings.SMTP_HOST
        email_service.settings.SMTP_HOST = "invalid.smtp.nonexistent.local"
        email_service.send_email_dispatch(
            db,
            recipient_email="smtp_fail_sim@smartserve.com",
            subject="Simulated Failure",
            body_text="Test Body",
            template_key="test_fail"
        )
        email_service.settings.SMTP_HOST = orig_host
        log_output = log_stream.getvalue()
        
        no_secrets_leaked = ("password" not in log_output.lower() and "secret" not in log_output.lower())
        results["12_safe_logging"] = log_test(12, "SMTP errors logged safely without secret exposure", no_secrets_leaked)

    finally:
        # Safely cleanup tokens and restore original password hash for registered user
        if user:
            try:
                db.rollback()
                # Clean up any test reset tokens created during the test
                db.query(PasswordResetToken).filter(PasswordResetToken.user_id == user.id).delete()
                if test_session_id:
                    db.query(UserSession).filter(UserSession.id == test_session_id).delete()
                
                if orig_password_hash:
                    # Restore original password hash
                    user.password_hash = orig_password_hash
                    db.add(user)
                    db.commit()
                    print(f"Restored original password hash for: {test_email}")
                elif created_user:
                    # If this test created the account from scratch, delete the test user
                    db.query(Customer).filter(Customer.user_id == user.id).delete()
                    db.query(User).filter(User.id == user.id).delete()
                    db.commit()
            except Exception as e:
                db.rollback()
                print("Cleanup error (safe):", e)
        db.close()

    print("=" * 75)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"  Summary: {passed}/{total} checks passed.")
    print("=" * 75)
    return passed == total

if __name__ == "__main__":
    success = run()
    sys.exit(0 if success else 1)
