import uuid
from datetime import datetime, timezone, timedelta
from app.repositories.db import get_db
from app.models.support import SupportTicket, TicketMessage, TicketPriority, TicketStatus
from app.models.customer import Customer
from app.models.booking import Booking
from app.models.user import User

def seed_support_tickets():
    db = next(get_db())

    existing_count = db.query(SupportTicket).count()
    if existing_count >= 4:
        print(f"Support tickets already exist ({existing_count} records). Skipping seed.")
        return

    print("Seeding initial support tickets, message threads & evidence into PostgreSQL...")

    customers = db.query(Customer).all()
    bookings = db.query(Booking).all()
    admin_user = db.query(User).filter(User.role == "admin").first()

    if not customers:
        print("No customers found for support seeding.")
        return

    c1 = customers[0]
    c2 = customers[1] if len(customers) > 1 else customers[0]
    c3 = customers[2] if len(customers) > 2 else customers[0]

    b1 = bookings[0] if bookings else None
    b2 = bookings[1] if len(bookings) > 1 else b1

    sample_tickets = [
        {
            "customer_id": c1.id,
            "booking_id": b1.id if b1 else None,
            "subject": "Electrical Circuit Trip After Fan Installation",
            "description": "Technician finished installation 2 hours ago. Main breaker keeps tripping when fan is set to high speed. Requesting urgent re-inspection.",
            "priority": TicketPriority.HIGH,
            "status": TicketStatus.OPEN,
            "escalated": True,
            "evidence_url": "https://storage.smartserve.com/evidence/circuit_breaker_01.jpg",
            "messages": [
                {
                    "sender_id": c1.user_id if c1.user_id else c1.id,
                    "sender_role": "customer",
                    "text": "Main breaker keeps tripping when fan is set to high speed. Requesting urgent re-inspection.",
                    "created_at": datetime.now(timezone.utc) - timedelta(hours=3)
                }
            ]
        },
        {
            "customer_id": c2.id,
            "booking_id": b2.id if b2 else None,
            "subject": "Billing Query — Double Charge Deduction",
            "description": "I was charged ₹1,499 twice on my UPI account for booking #726cf75f. Please initiate refund for duplicate payment.",
            "priority": TicketPriority.MEDIUM,
            "status": TicketStatus.IN_PROGRESS,
            "escalated": False,
            "evidence_url": "https://storage.smartserve.com/evidence/upi_receipt_statement.pdf",
            "messages": [
                {
                    "sender_id": c2.user_id if c2.user_id else c2.id,
                    "sender_role": "customer",
                    "text": "Attached my UPI bank statement showing two identical transactions of ₹1,499.",
                    "created_at": datetime.now(timezone.utc) - timedelta(hours=6)
                },
                {
                    "sender_id": admin_user.id if admin_user else c2.id,
                    "sender_role": "admin",
                    "text": "Hello! I am looking into your duplicate transaction logs with Razorpay payment gateway right now.",
                    "created_at": datetime.now(timezone.utc) - timedelta(hours=4)
                }
            ]
        },
        {
            "customer_id": c3.id,
            "booking_id": None,
            "subject": "Delayed Arrival & Unprofessional Conduct",
            "description": "Provider arrived 45 minutes late for plumbing appointment without prior update.",
            "priority": TicketPriority.URGENT,
            "status": TicketStatus.OPEN,
            "escalated": True,
            "evidence_url": None,
            "messages": [
                {
                    "sender_id": c3.user_id if c3.user_id else c3.id,
                    "sender_role": "customer",
                    "text": "Provider arrived 45 minutes late for plumbing appointment without prior update.",
                    "created_at": datetime.now(timezone.utc) - timedelta(hours=12)
                }
            ]
        },
        {
            "customer_id": c1.id,
            "booking_id": None,
            "subject": "Completed Service Warranty Verification",
            "description": "Can you provide warranty documentation for AC Deep Cleaning service performed last week?",
            "priority": TicketPriority.LOW,
            "status": TicketStatus.RESOLVED,
            "escalated": False,
            "evidence_url": None,
            "messages": [
                {
                    "sender_id": c1.user_id if c1.user_id else c1.id,
                    "sender_role": "customer",
                    "text": "Requesting 30-day warranty card copy for my record.",
                    "created_at": datetime.now(timezone.utc) - timedelta(days=2)
                },
                {
                    "sender_id": admin_user.id if admin_user else c1.id,
                    "sender_role": "admin",
                    "text": "SmartServe 30-day warranty card has been dispatched to your email address.",
                    "created_at": datetime.now(timezone.utc) - timedelta(days=1)
                }
            ]
        }
    ]

    for tdata in sample_tickets:
        t = SupportTicket(
            id=uuid.uuid4(),
            customer_id=tdata["customer_id"],
            booking_id=tdata["booking_id"],
            assigned_admin_id=admin_user.id if admin_user else None,
            subject=tdata["subject"],
            description=tdata["description"],
            priority=tdata["priority"],
            status=tdata["status"],
            escalated_to_admin=tdata["escalated"],
            image_evidence_url=tdata["evidence_url"],
            created_at=datetime.now(timezone.utc) - timedelta(hours=12)
        )
        db.add(t)
        db.flush()

        for mdata in tdata["messages"]:
            msg = TicketMessage(
                id=uuid.uuid4(),
                ticket_id=t.id,
                sender_id=mdata["sender_id"],
                sender_role=mdata["sender_role"],
                message_text=mdata["text"],
                created_at=mdata["created_at"]
            )
            db.add(msg)

    db.commit()
    print("Initial support tickets & message threads seeded successfully!")

if __name__ == "__main__":
    seed_support_tickets()
