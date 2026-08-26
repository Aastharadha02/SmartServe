import uuid
from datetime import datetime, timezone, timedelta
from app.repositories.db import get_db
from app.models.security import FailedLoginAttempt, AuditLog
from app.models.suspicious_activity import SuspiciousActivity
from app.models.user import User

def seed_security_events():
    db = next(get_db())

    existing_failed = db.query(FailedLoginAttempt).count()
    if existing_failed == 0:
        print("Seeding initial failed login attempts into PostgreSQL...")
        failed_attempts = [
            {
                "email": "unauthorized.attempt@domain.com",
                "ip": "185.220.101.4",
                "count": 5,
                "locked_until": datetime.now(timezone.utc) + timedelta(minutes=30)
            },
            {
                "email": "hacker_test@malicious-bot.net",
                "ip": "198.51.100.22",
                "count": 3,
                "locked_until": None
            },
            {
                "email": "support.admin@smartserve.com",
                "ip": "49.37.12.189",
                "count": 2,
                "locked_until": None
            }
        ]
        for fa in failed_attempts:
            db.add(FailedLoginAttempt(
                id=uuid.uuid4(),
                email=fa["email"],
                ip_address=fa["ip"],
                attempt_count=fa["count"],
                last_attempt=datetime.now(timezone.utc) - timedelta(minutes=15),
                locked_until=fa["locked_until"]
            ))

    existing_suspicious = db.query(SuspiciousActivity).count()
    if existing_suspicious == 0:
        print("Seeding initial suspicious activity anomalies into PostgreSQL...")
        admin_user = db.query(User).filter(User.role == "admin").first()

        if admin_user:
            from app.services import security_service
            security_service.create_active_session(
                db, user_id=admin_user.id, token_jti="jwt_admin_session_01",
                ip_address="127.0.0.1", user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128.0"
            )

        suspicious_events = [
            {
                "user_id": admin_user.id if admin_user else None,
                "anomaly_type": "Brute-Force Authentication Spike",
                "risk_score": 0.88,
                "details": {
                    "detection_reason": "5 consecutive failed password attempts within 45 seconds from IP 185.220.101.4",
                    "ip_address": "185.220.101.4",
                    "geo_location": "Frankfurt, DE",
                    "ai_signal": "AI-Assisted Risk Signal — High Anomaly Score"
                }
            },
            {
                "user_id": admin_user.id if admin_user else None,
                "anomaly_type": "Geographic Velocity Anomaly",
                "risk_score": 0.72,
                "details": {
                    "detection_reason": "Login session initiated from Mumbai, IN 10 minutes after session from London, UK",
                    "ip_address": "103.21.126.11",
                    "geo_location": "Mumbai, IN",
                    "ai_signal": "AI-Assisted Risk Signal — Impossible Travel Speed"
                }
            },
            {
                "user_id": None,
                "anomaly_type": "Privilege Escalation Attempt",
                "risk_score": 0.94,
                "details": {
                    "detection_reason": "Attempted access to /admin/admins/role without super_admin RBAC scope",
                    "ip_address": "49.37.12.189",
                    "geo_location": "Bengaluru, IN",
                    "ai_signal": "AI-Assisted Risk Signal — Critical Security Violation"
                }
            }
        ]
        for se in suspicious_events:
            db.add(SuspiciousActivity(
                id=uuid.uuid4(),
                user_id=se["user_id"],
                anomaly_type=se["anomaly_type"],
                risk_score=se["risk_score"],
                details_json=se["details"],
                created_at=datetime.now(timezone.utc) - timedelta(hours=2)
            ))

    db.commit()
    print("Initial security events seeded successfully!")

if __name__ == "__main__":
    seed_security_events()
