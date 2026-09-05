"""
SmartServe - Quick Local Database Setup & Seed Tool
Automatically initializes all tables, imports all 457 authentic catalog services
from backend/backup/smartserve_complete_catalog_backup.json, and seeds admin & customer accounts.
"""

import os
import sys
import json
import uuid
from datetime import datetime, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.repositories.db import engine, get_db
from app.models.base import Base
# Import models to ensure tables are registered with Base.metadata
from app.models.service import Service
from app.models.user import User
from app.models.security import AdminRole, AuditLog
from app.models.customer import Customer, Booking, SupportTicket, TicketMessage, BookingFeedback
from app.seed_admins import seed_initial_admins
from app.core.security import hash_password

BACKUP_JSON = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backup", "smartserve_complete_catalog_backup.json"))

def setup_and_seed():
    print("=" * 70)
    print("SmartServe Local Database Initializer & Catalog Seeder")
    print("=" * 70)

    # 1. Create all tables
    print("\n--> [1/4] Ensuring all PostgreSQL database tables exist...")
    Base.metadata.create_all(bind=engine)
    print("    [SUCCESS] All schema tables verified/created.")

    db = next(get_db())

    # 2. Seed Admin Accounts
    print("\n--> [2/4] Seeding Admin Accounts & RBAC Permissions...")
    seed_initial_admins()

    # 3. Seed Demo Customer Account
    print("\n--> [3/4] Ensuring Demo Customer Account exists...")
    demo_cust_user = db.query(User).filter(User.email == "customer@example.com").first()
    if not demo_cust_user:
        demo_cust_user = User(
            id=uuid.uuid4(),
            email="customer@example.com",
            password_hash=hash_password("CustomerPassword123!"),
            role="customer",
            is_active=True,
            is_2fa_enabled=False,
            created_at=datetime.now(timezone.utc)
        )
        db.add(demo_cust_user)
        db.flush()

    demo_cust_profile = db.query(Customer).filter(Customer.user_id == demo_cust_user.id).first()
    if not demo_cust_profile:
        demo_cust_profile = Customer(
            id=uuid.uuid4(),
            user_id=demo_cust_user.id,
            email=demo_cust_user.email,
            full_name="Aastha Sharma",
            phone="+91 9876543210",
            is_active=True,
            is_verified=True,
            total_bookings=0,
            lifetime_spent=0.0,
            created_at=datetime.now(timezone.utc)
        )
        db.add(demo_cust_profile)
        db.commit()
        print("    [SUCCESS] Created demo customer: customer@example.com / CustomerPassword123!")
    else:
        print("    [INFO] Demo customer already exists.")

    # 4. Import Catalog from backup JSON
    print("\n--> [4/4] Importing 457 authentic services from backup JSON...")
    if not os.path.exists(BACKUP_JSON):
        print(f"    [ERROR] Backup JSON file not found at: {BACKUP_JSON}")
        return

    with open(BACKUP_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    services_data = data.get("all_services", [])
    print(f"    Loaded {len(services_data)} services from backup JSON.")

    inserted = 0
    updated = 0

    for s_item in services_data:
        s_id = uuid.UUID(s_item["service_id"])
        svc = db.query(Service).filter(Service.id == s_id).first()

        # Reconstruct distinct_features and suggested_addons
        distinct_features = {
            "description": s_item.get("description", ""),
            "highlights": s_item.get("highlights", []),
            "included": s_item.get("included_features", []),
            "excluded": s_item.get("excluded_scope", []),
            "warranty": s_item.get("warranty_coverage", ""),
            "faqs": s_item.get("faqs", [])
        }

        suggested_addons = [
            {"type": "description", "text": s_item.get("description", "")},
            {"type": "highlights", "items": s_item.get("highlights", [])},
            {"type": "excluded_scope", "items": s_item.get("excluded_scope", [])},
            {"type": "process_steps", "steps": s_item.get("process_steps", [])},
            {"type": "aftercare_precautions", "aftercare": s_item.get("aftercare_precautions", [])},
            {"type": "tools_materials", "tools": s_item.get("tools_materials", []), "materials": []},
            {"type": "customer_setup", "requirements": s_item.get("customer_setup_requirements", [])},
            {"type": "expected_results", "items": s_item.get("expected_results", [])},
            {"type": "important_notes", "items": s_item.get("important_notes", [])},
            {"type": "warranty", "details": s_item.get("warranty_coverage", ""), "has_warranty": True},
            {"type": "faqs", "items": s_item.get("faqs", [])},
            {"type": "tips", "items": s_item.get("tips", [])},
            {"type": "dos_donts", "dos": s_item.get("dos", []), "donts": s_item.get("donts", [])},
            {"type": "duration", "minutes": s_item.get("estimated_duration_minutes", 60)},
        ]
        if s_item.get("suggested_addons"):
            suggested_addons.extend(s_item.get("suggested_addons"))

        if not svc:
            svc = Service(
                id=s_id,
                category=s_item["category_name"],
                subcategory=s_item["subcategory_name"],
                name=s_item["service_name"],
                base_price=s_item["base_price_inr"],
                max_demand_increase=s_item.get("max_demand_surge_percent", 0.0),
                max_discount=s_item.get("max_discount_percent", 0.0),
                distinct_features=distinct_features,
                suggested_addons=suggested_addons,
                is_active=s_item.get("is_active", True)
            )
            db.add(svc)
            inserted += 1
        else:
            svc.category = s_item["category_name"]
            svc.subcategory = s_item["subcategory_name"]
            svc.name = s_item["service_name"]
            svc.base_price = s_item["base_price_inr"]
            svc.max_demand_increase = s_item.get("max_demand_surge_percent", 0.0)
            svc.max_discount = s_item.get("max_discount_percent", 0.0)
            svc.distinct_features = distinct_features
            svc.suggested_addons = suggested_addons
            svc.is_active = s_item.get("is_active", True)
            updated += 1

    db.commit()
    print(f"    [SUCCESS] Database Catalog sync complete: {inserted} inserted, {updated} updated.")

    total_services = db.query(Service).count()
    print(f"\n[SUMMARY] Total Services in Database: {total_services} across 14 Categories.")
    print("Database setup & catalog seeding finished successfully!")

if __name__ == "__main__":
    setup_and_seed()
