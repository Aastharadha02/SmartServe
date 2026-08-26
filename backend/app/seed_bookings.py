import uuid
from datetime import datetime, timezone, timedelta
from app.repositories.db import get_db
from app.models.booking import Booking, BookingStatus, PaymentStatus
from app.models.customer import Customer
from app.models.provider import Provider
from app.models.service import Service

def seed_operational_bookings():
    db = next(get_db())

    # Check if bookings in active states already exist
    active_count = db.query(Booking).filter(Booking.status.in_([
        BookingStatus.REQUESTED, BookingStatus.ASSIGNED, BookingStatus.ACCEPTED, BookingStatus.STARTED
    ])).count()

    if active_count >= 5:
        print(f"Active bookings already seeded ({active_count} active bookings). Skipping seed.")
        return

    print("Seeding operational lifecycle bookings & emergency dispatches into PostgreSQL...")

    customers = db.query(Customer).all()
    providers = db.query(Provider).all()
    services = db.query(Service).limit(10).all()

    if not customers or not services:
        print("Missing customers or services to seed bookings.")
        return

    cust_1 = customers[0]
    cust_2 = customers[1] if len(customers) > 1 else customers[0]
    cust_3 = customers[2] if len(customers) > 2 else customers[0]

    prov_1 = providers[0] if providers else None
    prov_2 = providers[1] if len(providers) > 1 else prov_1

    sample_bookings = [
        {
            "customer_id": cust_1.id,
            "service_id": services[0].id,
            "provider_id": None,
            "status": BookingStatus.REQUESTED,
            "payment_status": PaymentStatus.PENDING,
            "scheduled_time": datetime.now(timezone.utc) + timedelta(hours=2),
            "address": "Flat 402, Sunshine Heights, Powai, Mumbai",
            "total_price": float(services[0].base_price or 899.0),
            "emergency_flag": "Emergency — Circuit Breaker Trip",
            "timeline": [
                {
                    "event": "Booking Requested by Customer",
                    "reason": "Emergency Dispatch Request",
                    "timestamp": (datetime.now(timezone.utc) - timedelta(minutes=15)).isoformat()
                }
            ]
        },
        {
            "customer_id": cust_2.id,
            "service_id": services[1].id if len(services) > 1 else services[0].id,
            "provider_id": prov_1.user_id if prov_1 else None,
            "status": BookingStatus.ASSIGNED,
            "payment_status": PaymentStatus.PENDING,
            "scheduled_time": datetime.now(timezone.utc) + timedelta(hours=4),
            "address": "B-12, Green Glen Layout, Bellandur, Bengaluru",
            "total_price": float(services[1].base_price or 1499.0) if len(services) > 1 else 1499.0,
            "emergency_flag": None,
            "timeline": [
                {
                    "event": "Booking Requested",
                    "reason": "Customer Booking",
                    "timestamp": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
                },
                {
                    "event": f"Assigned to Provider {prov_1.full_name if prov_1 else 'Priya Patel'}",
                    "reason": "Smart Matching Algorithm",
                    "timestamp": (datetime.now(timezone.utc) - timedelta(minutes=45)).isoformat()
                }
            ]
        },
        {
            "customer_id": cust_3.id,
            "service_id": services[2].id if len(services) > 2 else services[0].id,
            "provider_id": prov_2.user_id if prov_2 else None,
            "status": BookingStatus.ACCEPTED,
            "payment_status": PaymentStatus.PENDING,
            "scheduled_time": datetime.now(timezone.utc) + timedelta(hours=1),
            "address": "Villa 18, Palm Meadows, Whitefield, Bengaluru",
            "total_price": float(services[2].base_price or 699.0) if len(services) > 2 else 699.0,
            "emergency_flag": None,
            "timeline": [
                {
                    "event": "Booking Requested",
                    "reason": "Customer Scheduled",
                    "timestamp": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
                },
                {
                    "event": "Assigned to Provider",
                    "reason": "Dispatch System",
                    "timestamp": (datetime.now(timezone.utc) - timedelta(hours=1, minutes=30)).isoformat()
                },
                {
                    "event": "Accepted by Provider",
                    "reason": "Provider Acceptance",
                    "timestamp": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
                }
            ]
        },
        {
            "customer_id": cust_1.id,
            "service_id": services[3].id if len(services) > 3 else services[0].id,
            "provider_id": prov_1.user_id if prov_1 else None,
            "status": BookingStatus.STARTED,
            "payment_status": PaymentStatus.PENDING,
            "scheduled_time": datetime.now(timezone.utc) - timedelta(minutes=30),
            "address": "A-304, Urban Heights, HSR Layout, Bengaluru",
            "total_price": float(services[3].base_price or 1299.0) if len(services) > 3 else 1299.0,
            "emergency_flag": "Emergency — Main Water Leak",
            "timeline": [
                {
                    "event": "Emergency Request Logged",
                    "reason": "Urgent Pipe Leak",
                    "timestamp": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
                },
                {
                    "event": "Assigned & Accepted",
                    "reason": "Priority Match",
                    "timestamp": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
                },
                {
                    "event": "Service Started (OTP Verified)",
                    "reason": "Work Commenced",
                    "timestamp": (datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat()
                }
            ]
        }
    ]

    for bdata in sample_bookings:
        b = Booking(
            id=uuid.uuid4(),
            customer_id=bdata["customer_id"],
            service_id=bdata["service_id"],
            provider_id=bdata["provider_id"],
            status=bdata["status"],
            payment_status=bdata["payment_status"],
            scheduled_time=bdata["scheduled_time"],
            address=bdata["address"],
            total_price=bdata["total_price"],
            otp_code="5829",
            emergency_flag=bdata["emergency_flag"],
            timeline=bdata["timeline"],
            created_at=datetime.now(timezone.utc) - timedelta(hours=2)
        )
        db.add(b)

    db.commit()
    print("Operational lifecycle bookings seeded successfully!")

if __name__ == "__main__":
    seed_operational_bookings()
