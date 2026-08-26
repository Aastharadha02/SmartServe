import uuid
from datetime import datetime, timezone, timedelta
from app.repositories.db import get_db
from app.models.user import User
from app.models.customer import Customer
from app.models.customer_flag import CustomerFlag
from app.models.booking import Booking, BookingStatus, PaymentStatus
from app.models.service import Service
from app.models.provider import Provider
from app.core.security import hash_password

def seed_initial_customers():
    db = next(get_db())
    existing_count = db.query(Customer).count()
    if existing_count >= 5:
        print(f"Customers already exist ({existing_count} records). Skipping seed.")
        return

    print("Seeding initial realistic customer records & booking history into PostgreSQL...")

    # Get sample services & providers for real booking links
    services = db.query(Service).limit(5).all()
    providers = db.query(Provider).limit(3).all()
    admin_user = db.query(User).filter(User.email == "admin@smartserve.com").first()
    if not admin_user:
        admin_user = db.query(User).first()
    admin_id = admin_user.id

    sample_customers = [
        {
            "name": "Ananya Rao",
            "email": "ananya.rao@example.com",
            "phone": "+91 98765 11223",
            "active": True,
            "bookings": [
                {"status": BookingStatus.COMPLETED, "price": 499.0, "days_ago": 15},
                {"status": BookingStatus.COMPLETED, "price": 1299.0, "days_ago": 8},
                {"status": BookingStatus.COMPLETED, "price": 899.0, "days_ago": 2},
            ],
            "flag": None
        },
        {
            "name": "Vikram Malhotra",
            "email": "vikram.malhotra@example.com",
            "phone": "+91 98765 22334",
            "active": True,
            "bookings": [
                {"status": BookingStatus.COMPLETED, "price": 1499.0, "days_ago": 20},
                {"status": BookingStatus.COMPLETED, "price": 599.0, "days_ago": 5},
            ],
            "flag": None
        },
        {
            "name": "Kavita Sharma",
            "email": "kavita.sharma@example.com",
            "phone": "+91 98765 33445",
            "active": True,
            "bookings": [
                {"status": BookingStatus.COMPLETED, "price": 799.0, "days_ago": 25},
                {"status": BookingStatus.CANCELLED, "price": 499.0, "days_ago": 12},
                {"status": BookingStatus.CANCELLED, "price": 1299.0, "days_ago": 4},
            ],
            "flag": {
                "flag_type": "Frequent Cancellation Pattern",
                "reason": "Customer cancelled 3 bookings within 10 minutes of scheduled arrival window."
            }
        },
        {
            "name": "Rahul Deshmukh",
            "email": "rahul.deshmukh@example.com",
            "phone": "+91 98765 44556",
            "active": False,
            "bookings": [
                {"status": BookingStatus.CANCELLED, "price": 2499.0, "days_ago": 30},
                {"status": BookingStatus.CANCELLED, "price": 1999.0, "days_ago": 18},
            ],
            "flag": {
                "flag_type": "Fraud Risk — Chargeback Abuse",
                "reason": "Payment dispute initiated for completed high-value service after full execution."
            }
        },
        {
            "name": "Siddharth Nair",
            "email": "siddharth.nair@example.com",
            "phone": "+91 98765 55667",
            "active": True,
            "bookings": [
                {"status": BookingStatus.COMPLETED, "price": 699.0, "days_ago": 14},
                {"status": BookingStatus.COMPLETED, "price": 1899.0, "days_ago": 3},
            ],
            "flag": None
        },
        {
            "name": "Meera Kapoor",
            "email": "meera.kapoor@example.com",
            "phone": "+91 98765 66778",
            "active": True,
            "bookings": [
                {"status": BookingStatus.COMPLETED, "price": 999.0, "days_ago": 10},
            ],
            "flag": None
        },
        {
            "name": "Rohan Sen",
            "email": "rohan.sen@example.com",
            "phone": "+91 98765 77889",
            "active": False,
            "bookings": [
                {"status": BookingStatus.CANCELLED, "price": 3499.0, "days_ago": 7},
            ],
            "flag": {
                "flag_type": "Suspicious Booking Pattern",
                "reason": "Multiple fake emergency service requests from unverified location."
            }
        },
        {
            "name": "Deepa Joshi",
            "email": "deepa.joshi@example.com",
            "phone": "+91 98765 88990",
            "active": True,
            "bookings": [
                {"status": BookingStatus.COMPLETED, "price": 1199.0, "days_ago": 16},
                {"status": BookingStatus.COMPLETED, "price": 799.0, "days_ago": 1},
            ],
            "flag": None
        }
    ]

    for cdata in sample_customers:
        # Check if customer already exists by email
        existing_c = db.query(Customer).filter(Customer.email == cdata["email"]).first()
        if existing_c:
            continue

        # 1. Create User account
        user = User(
            id=uuid.uuid4(),
            email=cdata["email"],
            password_hash=hash_password("CustomerPass123!"),
            role="customer",
            is_active=cdata["active"]
        )
        db.add(user)
        db.flush()

        # 2. Create Customer account
        customer = Customer(
            id=uuid.uuid4(),
            user_id=user.id,
            email=cdata["email"],
            password_hash=user.password_hash,
            full_name=cdata["name"],
            phone=cdata["phone"],
            role="customer",
            is_active=cdata["active"],
            created_at=datetime.now(timezone.utc) - timedelta(days=90)
        )
        db.add(customer)
        db.flush()

        # 3. Create Risk Flag if present
        if cdata["flag"]:
            flag = CustomerFlag(
                id=uuid.uuid4(),
                customer_id=customer.id,
                flag_type=cdata["flag"]["flag_type"],
                reason=cdata["flag"]["reason"],
                flagged_by=admin_id,
                created_at=datetime.now(timezone.utc) - timedelta(days=5)
            )
            db.add(flag)

        # 4. Create Bookings
        for bidx, bdata in enumerate(cdata["bookings"]):
            if services and providers:
                serv = services[bidx % len(services)]
                prov = providers[bidx % len(providers)]
                booking = Booking(
                    id=uuid.uuid4(),
                    customer_id=customer.id,
                    provider_id=prov.user_id,
                    service_id=serv.id,
                    status=bdata["status"],
                    payment_status=PaymentStatus.COMPLETED if bdata["status"] == BookingStatus.COMPLETED else PaymentStatus.REFUNDED,
                    scheduled_time=datetime.now(timezone.utc) - timedelta(days=bdata["days_ago"]),
                    address="Block B, Sector 62, Noida, Uttar Pradesh 201309",
                    total_price=bdata["price"],
                    otp_code="4892",
                    created_at=datetime.now(timezone.utc) - timedelta(days=bdata["days_ago"] + 1)
                )
                db.add(booking)

    db.commit()
    print("Initial customers & booking history seeded successfully!")

if __name__ == "__main__":
    seed_initial_customers()
