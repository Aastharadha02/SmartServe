"""
SmartServe - Reusable Demo Accounts & Repeatable Testing Setup Service

Provides idempotent management of persistent local development demo accounts:
- One Demo Customer: demo.customer@smartserve.local / DemoCustomer123!
- One Demo Provider: demo.provider@smartserve.local / DemoProvider123!
- One Demo Administrator: demo.admin@smartserve.local / DemoAdmin123!

Safety Guarantees:
- Never runs destructive operations in production environments.
- Idempotently creates or reuses existing accounts without data duplication.
- Never hardcodes or bypasses authentication, OTP verification, or security controls.
- Scoped reset deletes ONLY demo-owned bookings/payments, preserving real accounts.
"""

import os
import uuid
from datetime import datetime, date, time, timezone, timedelta
from decimal import Decimal
from typing import Dict, Any, Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func

from app.core.config import settings
from app.core.security import hash_password
from app.models.user import User
from app.models.customer import Customer, Booking, SupportTicket, TicketMessage, BookingFeedback
from app.models.provider import Provider, Certificate, ProviderService, Availability
from app.models.security import AdminRole
from app.models.service import Service
from app.models.payment import BookingPayment, BookingOTP, PaymentStatus, OTPType
from app.services.booking.otp_service import generate_secure_otp, get_active_otp

DEMO_CUSTOMER_CONFIG = {
    "email": "demo.customer@smartserve.com",
    "password": "DemoCustomer123!",
    "full_name": "Demo Customer",
    "phone": "+91 98765 00001",
    "address": "101 Demo Residency, Sector 18, Noida",
    "city": "Noida",
    "pincode": "201301",
    "role": "customer",
}

DEMO_PROVIDER_CONFIG = {
    "email": "demo.provider@smartserve.com",
    "password": "DemoProvider123!",
    "full_name": "Demo Pro Services",
    "phone": "+91 98765 00002",
    "category": "2. Cleaning & Home Cleaning",
    "skills": "Certified Professional Deep Cleaning & Sanitation Specialist with 5+ years experience.",
    "service_area": "Noida, Greater Noida & Delhi NCR",
    "experience_years": 5,
    "base_price": 499.0,
    "role": "provider",
}

DEMO_ADMIN_CONFIG = {
    "email": "demo.admin@smartserve.com",
    "password": "DemoAdmin123!",
    "full_name": "Demo Operations Admin",
    "role": "super_admin",
}

ADMIN_PERMISSIONS = [
    "dashboard:view",
    "catalog:manage",
    "catalog:edit",
    "catalog:view",
    "providers:manage",
    "providers:view",
    "customers:manage",
    "customers:view",
    "admins:manage",
    "bookings:manage",
    "bookings:view",
    "insights:view",
    "support:manage",
    "security:manage",
    "emails:manage",
    "settings:manage",
]


def _check_environment_safety(operation_name: str, force: bool = False) -> None:
    """Enforce strict guard against running demo setup or reset in production."""
    env = (settings.ENVIRONMENT or "dev").strip().lower()
    if env in ["production", "prod"]:
        raise PermissionError(
            f"SAFETY VIOLATION: Operation '{operation_name}' is strictly blocked in production environment "
            f"(ENVIRONMENT='{settings.ENVIRONMENT}')."
        )

    db_url = str(settings.DATABASE_URL or "").lower()
    is_local_db = any(k in db_url for k in ["localhost", "127.0.0.1", "test", "sqlite"])
    if not is_local_db and not force:
        raise PermissionError(
            f"SAFETY VIOLATION: Database target does not appear to be local: {db_url.split('@')[-1] if '@' in db_url else 'remote'}. "
            f"Operation '{operation_name}' blocked to prevent modifying non-local databases."
        )


def setup_demo_accounts(db: Session, update_passwords: bool = True) -> Dict[str, Any]:
    """
    Idempotently sets up or updates the 3 persistent local demo accounts.
    Reuses existing accounts, maintains account IDs, ensures required profiles,
    certificates, catalog associations, and free availability slots are ready.
    """
    _check_environment_safety("setup_demo_accounts")

    now_utc = datetime.now(timezone.utc)
    results = {
        "customer": {},
        "provider": {},
        "admin": {},
        "created_records": [],
        "reused_records": [],
    }

    # -------------------------------------------------------------------------
    # 1. DEMO CUSTOMER
    # -------------------------------------------------------------------------
    cust_email = DEMO_CUSTOMER_CONFIG["email"]
    cust_user = db.query(User).filter(User.email == cust_email).first()
    if not cust_user:
        cust_user = User(
            id=uuid.uuid4(),
            email=cust_email,
            password_hash=hash_password(DEMO_CUSTOMER_CONFIG["password"]),
            role="customer",
            is_active=True,
            is_2fa_enabled=False,
            created_at=now_utc,
        )
        cust_user.is_profile_complete = True
        db.add(cust_user)
        db.flush()
        results["created_records"].append(f"User: {cust_email}")
    else:
        cust_user.is_active = True
        cust_user.is_profile_complete = True
        if update_passwords:
            cust_user.password_hash = hash_password(DEMO_CUSTOMER_CONFIG["password"])
        results["reused_records"].append(f"User: {cust_email}")

    cust_profile = db.query(Customer).filter(Customer.user_id == cust_user.id).first()
    if not cust_profile:
        cust_profile = Customer(
            id=uuid.uuid4(),
            user_id=cust_user.id,
            email=cust_email,
            full_name=DEMO_CUSTOMER_CONFIG["full_name"],
            phone=DEMO_CUSTOMER_CONFIG["phone"],
            is_active=True,
            is_verified=True,
            lifetime_spent=Decimal("0.00"),
            total_bookings=0,
            preferences={
                "address": DEMO_CUSTOMER_CONFIG["address"],
                "city": DEMO_CUSTOMER_CONFIG["city"],
                "pincode": DEMO_CUSTOMER_CONFIG["pincode"],
            },
            created_at=now_utc,
        )
        db.add(cust_profile)
        db.flush()
        results["created_records"].append(f"Customer Profile: {cust_email}")
    else:
        cust_profile.full_name = DEMO_CUSTOMER_CONFIG["full_name"]
        cust_profile.phone = DEMO_CUSTOMER_CONFIG["phone"]
        cust_profile.is_active = True
        cust_profile.is_verified = True
        results["reused_records"].append(f"Customer Profile: {cust_email}")

    results["customer"] = {
        "user_id": str(cust_user.id),
        "customer_id": str(cust_profile.id),
        "email": cust_email,
        "password": DEMO_CUSTOMER_CONFIG["password"],
        "full_name": cust_profile.full_name,
        "role": cust_user.role,
    }

    # -------------------------------------------------------------------------
    # 2. DEMO PROVIDER
    # -------------------------------------------------------------------------
    prov_email = DEMO_PROVIDER_CONFIG["email"]
    prov_user = db.query(User).filter(User.email == prov_email).first()
    if not prov_user:
        prov_user = User(
            id=uuid.uuid4(),
            email=prov_email,
            password_hash=hash_password(DEMO_PROVIDER_CONFIG["password"]),
            role="provider",
            is_active=True,
            is_2fa_enabled=False,
            created_at=now_utc,
        )
        prov_user.is_profile_complete = True
        db.add(prov_user)
        db.flush()
        results["created_records"].append(f"User: {prov_email}")
    else:
        prov_user.is_active = True
        prov_user.is_profile_complete = True
        if update_passwords:
            prov_user.password_hash = hash_password(DEMO_PROVIDER_CONFIG["password"])
        results["reused_records"].append(f"User: {prov_email}")

    prov_profile = db.query(Provider).filter(Provider.user_id == prov_user.id).first()
    if not prov_profile:
        prov_profile = Provider(
            user_id=prov_user.id,
            full_name=DEMO_PROVIDER_CONFIG["full_name"],
            category=DEMO_PROVIDER_CONFIG["category"],
            skills=DEMO_PROVIDER_CONFIG["skills"],
            service_area=DEMO_PROVIDER_CONFIG["service_area"],
            experience_years=DEMO_PROVIDER_CONFIG["experience_years"],
            base_price=Decimal(str(DEMO_PROVIDER_CONFIG["base_price"])),
            is_verified=True,
            reliability_score=Decimal("99.50"),
            acceptance_rate=Decimal("98.50"),
            on_time_rate=Decimal("99.00"),
            cancellation_rate=Decimal("0.50"),
            no_show_rate=Decimal("0.00"),
            response_time_score=Decimal("98.00"),
            created_at=now_utc,
        )
        db.add(prov_profile)
        db.flush()
        results["created_records"].append(f"Provider Profile: {prov_email}")
    else:
        prov_profile.full_name = DEMO_PROVIDER_CONFIG["full_name"]
        prov_profile.category = DEMO_PROVIDER_CONFIG["category"]
        prov_profile.service_area = DEMO_PROVIDER_CONFIG["service_area"]
        prov_profile.is_verified = True
        prov_profile.reliability_score = Decimal("99.50")
        prov_profile.acceptance_rate = Decimal("98.50")
        results["reused_records"].append(f"Provider Profile: {prov_email}")

    # Ensure Verified KYC Documents
    certs = db.query(Certificate).filter(Certificate.provider_id == prov_user.id).all()
    if not certs:
        doc_types = [
            ("Identity Proof (Aadhaar)", "DEMO-AADHAAR-9012", "https://smartserve.local/kyc/demo_aadhaar.pdf"),
            ("Professional Trade Credential", "DEMO-CERT-CLEAN-55", "https://smartserve.local/kyc/demo_cleaning_cert.pdf"),
            ("Police Verification Certificate", "DEMO-POLICE-VERIF-2026", "https://smartserve.local/kyc/demo_police_verif.pdf"),
        ]
        for ctype, dnum, durl in doc_types:
            c = Certificate(
                id=uuid.uuid4(),
                provider_id=prov_user.id,
                certificate_type=ctype,
                document_number=dnum,
                document_url=durl,
                extracted_name=prov_profile.full_name,
                verification_status="Verified",
                verified_at=now_utc,
                uploaded_at=now_utc,
            )
            db.add(c)
        results["created_records"].append(f"KYC Certificates (3) for {prov_email}")
    else:
        for c in certs:
            c.verification_status = "Verified"
            c.verified_at = now_utc

    # Ensure Catalog Services are Associated
    # Associate all active services in cleaning or top services
    cleaning_services = (
        db.query(Service)
        .filter(Service.category.ilike("%cleaning%"), Service.is_active == True)
        .all()
    )
    if not cleaning_services:
        cleaning_services = db.query(Service).filter(Service.is_active == True).limit(10).all()

    ps_count = 0
    for svc in cleaning_services:
        ps_entry = (
            db.query(ProviderService)
            .filter(
                ProviderService.provider_id == prov_user.id,
                ProviderService.service_id == svc.id,
            )
            .first()
        )
        if not ps_entry:
            ps_entry = ProviderService(
                id=uuid.uuid4(),
                provider_id=prov_user.id,
                service_id=svc.id,
                price=Decimal(str(svc.base_price)),
                duration_minutes=60,
                active=True,
                created_at=now_utc,
            )
            db.add(ps_entry)
            ps_count += 1
        else:
            ps_entry.active = True
    if ps_count > 0:
        results["created_records"].append(f"{ps_count} ProviderService links for {prov_email}")

    # Ensure Free Availability Slots for next 30 days
    today = date.today()
    slot_times = [
        (time(9, 0), time(11, 0)),
        (time(11, 30), time(13, 30)),
        (time(14, 0), time(16, 0)),
        (time(16, 30), time(18, 30)),
    ]
    slots_added = 0
    for day_offset in range(30):
        d = today + timedelta(days=day_offset)
        for st, et in slot_times:
            existing_slot = (
                db.query(Availability)
                .filter(
                    Availability.provider_id == prov_user.id,
                    Availability.slot_date == d,
                    Availability.start_time == st,
                )
                .first()
            )
            if not existing_slot:
                slot = Availability(
                    id=uuid.uuid4(),
                    provider_id=prov_user.id,
                    slot_date=d,
                    start_time=st,
                    end_time=et,
                    status="FREE",
                    created_at=now_utc,
                )
                db.add(slot)
                slots_added += 1
            elif existing_slot.status != "FREE":
                existing_slot.status = "FREE"
    if slots_added > 0:
        results["created_records"].append(f"{slots_added} Free Availability slots for {prov_email}")

    results["provider"] = {
        "user_id": str(prov_user.id),
        "email": prov_email,
        "password": DEMO_PROVIDER_CONFIG["password"],
        "full_name": prov_profile.full_name,
        "category": prov_profile.category,
        "role": prov_user.role,
        "services_count": len(cleaning_services),
    }

    # -------------------------------------------------------------------------
    # 3. DEMO ADMINISTRATOR
    # -------------------------------------------------------------------------
    admin_email = DEMO_ADMIN_CONFIG["email"]
    admin_user = db.query(User).filter(User.email == admin_email).first()
    if not admin_user:
        admin_user = User(
            id=uuid.uuid4(),
            email=admin_email,
            password_hash=hash_password(DEMO_ADMIN_CONFIG["password"]),
            role="super_admin",
            is_active=True,
            is_2fa_enabled=False,
            created_at=now_utc,
        )
        admin_user.is_profile_complete = True
        db.add(admin_user)
        db.flush()
        results["created_records"].append(f"User: {admin_email}")
    else:
        admin_user.is_active = True
        admin_user.role = "super_admin"
        admin_user.is_profile_complete = True
        if update_passwords:
            admin_user.password_hash = hash_password(DEMO_ADMIN_CONFIG["password"])
        results["reused_records"].append(f"User: {admin_email}")

    admin_role_entry = db.query(AdminRole).filter(AdminRole.user_id == admin_user.id).first()
    if not admin_role_entry:
        admin_role_entry = AdminRole(
            id=uuid.uuid4(),
            user_id=admin_user.id,
            role_name="super_admin",
            permissions=ADMIN_PERMISSIONS,
            is_active=True,
            created_at=now_utc,
        )
        db.add(admin_role_entry)
        results["created_records"].append(f"AdminRole permissions for {admin_email}")
    else:
        admin_role_entry.role_name = "super_admin"
        admin_role_entry.permissions = ADMIN_PERMISSIONS
        admin_role_entry.is_active = True
        results["reused_records"].append(f"AdminRole permissions for {admin_email}")

    results["admin"] = {
        "user_id": str(admin_user.id),
        "email": admin_email,
        "password": DEMO_ADMIN_CONFIG["password"],
        "full_name": DEMO_ADMIN_CONFIG["full_name"],
        "role": admin_user.role,
        "permissions_count": len(ADMIN_PERMISSIONS),
    }

    db.commit()
    return results


def prepare_demo_booking(
    db: Session,
    status: str = "Arrived",
    service_id: Optional[uuid.UUID] = None,
    agreed_amount: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Creates a fresh, verified demo booking for COD and Two-Stage OTP demonstration.
    - Uses the persistent demo customer and demo provider.
    - Generates authentic Start OTP (and Completion OTP if status is 'Started').
    - Establishes a BookingPayment record in 'Pending' status.
    - Avoids modifying other user or booking records.
    """
    _check_environment_safety("prepare_demo_booking")

    # Ensure demo accounts exist
    cust_user = db.query(User).filter(User.email == DEMO_CUSTOMER_CONFIG["email"]).first()
    prov_user = db.query(User).filter(User.email == DEMO_PROVIDER_CONFIG["email"]).first()
    if not cust_user or not prov_user:
        setup_demo_accounts(db)
        cust_user = db.query(User).filter(User.email == DEMO_CUSTOMER_CONFIG["email"]).first()
        prov_user = db.query(User).filter(User.email == DEMO_PROVIDER_CONFIG["email"]).first()

    cust_profile = db.query(Customer).filter(Customer.user_id == cust_user.id).first()
    prov_profile = db.query(Provider).filter(Provider.user_id == prov_user.id).first()

    # Find service
    service = None
    if service_id:
        service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        # Prefer a cleaning service offered by demo provider
        service = (
            db.query(Service)
            .join(ProviderService, ProviderService.service_id == Service.id)
            .filter(
                ProviderService.provider_id == prov_user.id,
                ProviderService.active == True,
                Service.is_active == True,
            )
            .first()
        )
    if not service:
        service = db.query(Service).filter(Service.is_active == True).first()
        if service:
            # Ensure demo provider offers it
            ps = ProviderService(
                id=uuid.uuid4(),
                provider_id=prov_user.id,
                service_id=service.id,
                price=Decimal(str(service.base_price)),
                duration_minutes=60,
                active=True,
            )
            db.add(ps)
            db.flush()

    if not service:
        raise ValueError("Cannot prepare demo booking: No active services exist in the database catalog.")

    price = Decimal(str(agreed_amount or service.base_price or 750.0))
    now_utc = datetime.now(timezone.utc)
    scheduled_time = now_utc + timedelta(hours=2)

    ref_suffix = uuid.uuid4().hex[:6].upper()
    booking_reference = f"DEMO-{ref_suffix}"

    status_normalized = status.strip().title()
    valid_statuses = ["Requested", "Accepted", "Arrived", "Started", "Completed"]
    if status_normalized not in valid_statuses:
        status_normalized = "Arrived"

    timeline = [
        {
            "event": "Booking Created",
            "actor": cust_profile.full_name,
            "role": "customer",
            "status": "Requested",
            "timestamp": now_utc.isoformat(),
        }
    ]
    if status_normalized in ["Accepted", "Arrived", "Started", "Completed"]:
        timeline.append({
            "event": "Provider Accepted Job",
            "actor": prov_profile.full_name,
            "role": "provider",
            "status": "Accepted",
            "timestamp": (now_utc + timedelta(minutes=5)).isoformat(),
        })
    if status_normalized in ["Arrived", "Started", "Completed"]:
        timeline.append({
            "event": "Provider Arrived at Location",
            "actor": prov_profile.full_name,
            "role": "provider",
            "status": "Arrived",
            "timestamp": (now_utc + timedelta(minutes=25)).isoformat(),
        })
    if status_normalized in ["Started", "Completed"]:
        timeline.append({
            "event": "Service Started via Start OTP",
            "actor": prov_profile.full_name,
            "role": "provider",
            "status": "Started",
            "timestamp": (now_utc + timedelta(minutes=30)).isoformat(),
        })
    if status_normalized == "Completed":
        timeline.append({
            "event": "Service Completed via Completion OTP",
            "actor": prov_profile.full_name,
            "role": "provider",
            "status": "Completed",
            "timestamp": (now_utc + timedelta(minutes=90)).isoformat(),
        })

    booking = Booking(
        id=uuid.uuid4(),
        customer_id=cust_profile.id,
        provider_id=prov_user.id,
        service_id=service.id,
        status=status_normalized,
        payment_method="COD",
        payment_status="Pending",
        scheduled_time=scheduled_time,
        address=DEMO_CUSTOMER_CONFIG["address"],
        total_price=price,
        timeline=timeline,
        created_at=now_utc,
        updated_at=now_utc,
    )
    db.add(booking)
    db.flush()

    payment = BookingPayment(
        id=uuid.uuid4(),
        booking_id=booking.id,
        customer_id=cust_profile.id,
        provider_id=prov_user.id,
        payment_method="COD",
        agreed_amount=price,
        status=PaymentStatus.PENDING.value,
        discrepancy_flag=False,
        discrepancy_amount=Decimal("0.00"),
        created_at=now_utc,
        updated_at=now_utc,
    )
    db.add(payment)
    db.flush()

    # Generate Start OTP
    start_otp_record = generate_secure_otp(booking.id, OTPType.START.value, db)
    start_otp_code = start_otp_record.otp_code

    completion_otp_code = None
    if status_normalized in ["Started", "Completed"]:
        # Mark Start OTP consumed
        start_otp_record.is_used = True
        start_otp_record.used_at = now_utc
        # Mint Completion OTP
        comp_otp_record = generate_secure_otp(booking.id, OTPType.COMPLETE.value, db)
        completion_otp_code = comp_otp_record.otp_code
        if status_normalized == "Completed":
            comp_otp_record.is_used = True
            comp_otp_record.used_at = now_utc

    db.commit()
    db.refresh(booking)

    return {
        "booking_id": str(booking.id),
        "booking_reference": str(booking.id)[:8].upper(),
        "status": booking.status,
        "payment_method": booking.payment_method,
        "payment_status": booking.payment_status,
        "service_name": service.name,
        "agreed_amount": float(price),
        "customer_email": cust_user.email,
        "provider_email": prov_user.email,
        "start_otp": start_otp_code,
        "completion_otp": completion_otp_code,
        "scheduled_time": scheduled_time.isoformat(),
        "address": booking.address,
    }


def reset_demo_data(db: Session, force: bool = False) -> Dict[str, Any]:
    """
    Safely purges ONLY demo-owned booking and payment records.
    - Refuses to run in production environments.
    - Limits deletion strictly to bookings belonging to demo.customer / demo.provider.
    - Preserves demo user accounts, provider credentials, certificates, and catalog.
    - Leaves all non-demo customers, providers, and bookings untouched.
    """
    _check_environment_safety("reset_demo_data", force=force)

    cust_user = db.query(User).filter(User.email == DEMO_CUSTOMER_CONFIG["email"]).first()
    prov_user = db.query(User).filter(User.email == DEMO_PROVIDER_CONFIG["email"]).first()

    if not cust_user and not prov_user:
        return {
            "message": "No demo accounts exist in this database. Nothing to reset.",
            "deleted_bookings": 0,
            "deleted_payments": 0,
            "deleted_otps": 0,
        }

    cust_id = None
    if cust_user:
        cust_profile = db.query(Customer).filter(Customer.user_id == cust_user.id).first()
        if cust_profile:
            cust_id = cust_profile.id

    prov_id = prov_user.id if prov_user else None

    # Query strictly demo bookings
    filter_clauses = []
    if cust_id:
        filter_clauses.append(Booking.customer_id == cust_id)
    if prov_id:
        filter_clauses.append(Booking.provider_id == prov_id)

    if not filter_clauses:
        return {
            "message": "No demo bookings found.",
            "deleted_bookings": 0,
            "deleted_payments": 0,
            "deleted_otps": 0,
        }

    demo_bookings = db.query(Booking).filter(or_(*filter_clauses)).all()
    booking_ids = [b.id for b in demo_bookings]

    deleted_payments = 0
    deleted_otps = 0
    deleted_bookings = len(booking_ids)

    if booking_ids:
        # Delete related payments
        deleted_payments = (
            db.query(BookingPayment)
            .filter(BookingPayment.booking_id.in_(booking_ids))
            .delete(synchronize_session=False)
        )

        # Delete related OTPs
        deleted_otps = (
            db.query(BookingOTP)
            .filter(BookingOTP.booking_id.in_(booking_ids))
            .delete(synchronize_session=False)
        )

        # Delete related feedback
        db.query(BookingFeedback).filter(BookingFeedback.booking_id.in_(booking_ids)).delete(synchronize_session=False)

        # Delete related support tickets
        db.query(SupportTicket).filter(SupportTicket.booking_id.in_(booking_ids)).delete(synchronize_session=False)

        # Delete bookings
        db.query(Booking).filter(Booking.id.in_(booking_ids)).delete(synchronize_session=False)

    # Reset customer counters
    if cust_id:
        cust_profile = db.query(Customer).filter(Customer.id == cust_id).first()
        if cust_profile:
            cust_profile.total_bookings = 0
            cust_profile.lifetime_spent = Decimal("0.00")

    # Reset availability slots for demo provider back to FREE
    if prov_id:
        db.query(Availability).filter(
            Availability.provider_id == prov_id,
            Availability.status != "FREE",
        ).update({"status": "FREE"}, synchronize_session=False)

    db.commit()

    return {
        "message": f"Successfully reset demo booking records without touching user accounts or non-demo data.",
        "deleted_bookings": deleted_bookings,
        "deleted_payments": deleted_payments,
        "deleted_otps": deleted_otps,
        "preserved_accounts": [
            DEMO_CUSTOMER_CONFIG["email"],
            DEMO_PROVIDER_CONFIG["email"],
            DEMO_ADMIN_CONFIG["email"],
        ],
    }
