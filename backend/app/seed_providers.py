import uuid
from datetime import datetime, timezone, timedelta
from app.repositories.db import get_db
from app.models.user import User
from app.models.provider import Provider, Certificate
from app.core.security import hash_password

def seed_initial_providers():
    db = next(get_db())
    existing_count = db.query(Provider).count()
    if existing_count > 0:
        print(f"Providers already exist ({existing_count} records). Skipping seed.")
        return

    print("Seeding initial realistic provider records into PostgreSQL...")

    sample_providers = [
        {
            "name": "Rajesh Sharma",
            "email": "rajesh.sharma@smartserve.com",
            "phone": "+91 98765 12345",
            "category": "1. Beauty, Salon & Spa",
            "experience": 6,
            "verified": True,
            "active": True,
            "doc_type": "Identity Proof (Aadhaar / Passport)",
            "doc_num": "AADHAAR-8839-1029",
            "doc_status": "Verified"
        },
        {
            "name": "Sunita Verma",
            "email": "sunita.verma@smartserve.com",
            "phone": "+91 98765 23456",
            "category": "7. Domestic Help & Cooking",
            "experience": 8,
            "verified": True,
            "active": True,
            "doc_type": "Food Safety & Hygiene Certification",
            "doc_num": "FSSAI-883210-99",
            "doc_status": "Verified"
        },
        {
            "name": "Amit Kumar",
            "email": "amit.kumar@smartserve.com",
            "phone": "+91 98765 34567",
            "category": "5. Electrician, Plumber, Carpenter & Home Repairs",
            "experience": 5,
            "verified": False,
            "active": True,
            "doc_type": "Electrical License Grade A",
            "doc_num": "ELEC-LIC-44910",
            "doc_status": "Pending"
        },
        {
            "name": "Priya Patel",
            "email": "priya.patel@smartserve.com",
            "phone": "+91 98765 45678",
            "category": "3. Painting, Waterproofing & Home Improvement",
            "experience": 7,
            "verified": True,
            "active": True,
            "doc_type": "Contractor Master Certification",
            "doc_num": "CONT-CERT-9921",
            "doc_status": "Verified"
        },
        {
            "name": "Vikram Singh",
            "email": "vikram.singh@smartserve.com",
            "phone": "+91 98765 56789",
            "category": "4. AC, Appliance & Electronics Repair",
            "experience": 4,
            "verified": False,
            "active": False,
            "doc_type": "HVAC Technician Certification",
            "doc_num": "HVAC-EXP-0012",
            "doc_status": "Rejected"
        },
        {
            "name": "Anita Gupta",
            "email": "anita.gupta@smartserve.com",
            "phone": "+91 98765 67890",
            "category": "2. Cleaning & Home Cleaning",
            "experience": 3,
            "verified": False,
            "active": True,
            "doc_type": "Background Verification Certificate",
            "doc_num": "BGC-CLEAR-4412",
            "doc_status": "Pending"
        }
    ]

    for pdata in sample_providers:
        # 1. Create User
        user = User(
            id=uuid.uuid4(),
            email=pdata["email"],
            password_hash=hash_password("ProviderPass123!"),
            role="provider",
            is_active=pdata["active"]
        )
        db.add(user)
        db.flush()

        # 2. Create Provider
        provider = Provider(
            user_id=user.id,
            full_name=pdata["name"],
            category=pdata["category"],
            experience_years=pdata["experience"],
            is_verified=pdata["verified"],
            reliability_score=98.5,
            acceptance_rate=96.0,
            on_time_rate=98.0,
            cancellation_rate=1.5,
            no_show_rate=0.0,
            response_time_score=95.0,
            created_at=datetime.now(timezone.utc) - timedelta(days=60),
            updated_at=datetime.now(timezone.utc)
        )
        db.add(provider)
        db.flush()

        # 3. Create Certificate
        cert = Certificate(
            id=uuid.uuid4(),
            provider_id=user.id,
            document_url=f"https://smartserve.com/docs/{pdata['doc_num'].lower()}.pdf",
            certificate_type=pdata["doc_type"],
            document_number=pdata["doc_num"],
            expiry_date=datetime.now(timezone.utc) + timedelta(days=365),
            extracted_name=pdata["name"],
            is_duplicate=False,
            verification_status=pdata["doc_status"],
            uploaded_at=datetime.now(timezone.utc) - timedelta(days=10)
        )
        db.add(cert)

    db.commit()
    print("Initial providers seeded successfully!")

if __name__ == "__main__":
    seed_initial_providers()
