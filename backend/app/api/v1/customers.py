import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin, require_permission
from app.repositories.db import get_db
from app.repositories import customer_repository, audit_repository
from app.models.user import User
from app.models.customer import Customer
from app.models.customer_flag import CustomerFlag
from app.schemas.people import CustomerDetailResponse, CustomerFlagRequest, AccountStatusRequest

from app.models.booking import Booking, BookingStatus
from app.models.service import Service
from app.models.provider import Provider

router = APIRouter(prefix="/admin/customers", tags=["Admin People Management — Customers"])

@router.get("/", response_model=List[CustomerDetailResponse])
def list_customers(
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_flagged: Optional[bool] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """List customer accounts with search, activity counts, and risk flag filters."""
    query = db.query(Customer)

    if is_active is not None:
        query = query.filter(Customer.is_active == is_active)

    customers = query.offset(skip).limit(limit).all()

    res = []
    for c in customers:
        if search:
            s_lower = search.lower()
            if (
                s_lower not in c.full_name.lower() and
                s_lower not in c.email.lower() and
                s_lower not in str(c.id).lower()
            ):
                continue

        # Get flags for this customer
        flags = db.query(CustomerFlag).filter(CustomerFlag.customer_id == c.id).all()
        flag_list = [
            {
                "id": str(f.id),
                "flag_type": f.flag_type,
                "reason": f.reason,
                "created_at": f.created_at.isoformat() if f.created_at else ""
            } for f in flags
        ]
        has_flags = len(flags) > 0

        if is_flagged is not None and has_flags != is_flagged:
            continue

        # Get bookings for this customer
        b_query = db.query(Booking).filter(Booking.customer_id == c.id).all()
        total_b = len(b_query)
        completed_b = sum(1 for b in b_query if str(b.status).upper() == "COMPLETED" or b.status == BookingStatus.COMPLETED)
        cancelled_b = sum(1 for b in b_query if str(b.status).upper() == "CANCELLED" or b.status == BookingStatus.CANCELLED)

        res.append(CustomerDetailResponse(
            id=str(c.id),
            user_id=str(c.user_id) if c.user_id else None,
            full_name=c.full_name,
            email=c.email,
            phone=c.phone,
            is_active=c.is_active,
            bookings_count=total_b,
            completed_bookings_count=completed_b,
            cancelled_bookings_count=cancelled_b,
            is_flagged=has_flags,
            flags=flag_list,
            created_at=c.created_at.isoformat() if c.created_at else ""
        ))
    return res

@router.get("/{customer_id}", response_model=CustomerDetailResponse)
def get_customer_detail(
    customer_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Retrieve detailed customer profile by ID, including booking history and risk flags."""
    try:
        c_uuid = uuid.UUID(customer_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid customer ID format")

    customer = customer_repository.get_customer_by_id(db, c_uuid)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Get flags
    flags = db.query(CustomerFlag).filter(CustomerFlag.customer_id == c_uuid).all()
    flag_list = [
        {
            "id": str(f.id),
            "flag_type": f.flag_type,
            "reason": f.reason,
            "created_at": f.created_at.isoformat() if f.created_at else ""
        } for f in flags
    ]

    # Get booking history
    b_query = db.query(Booking).filter(Booking.customer_id == c_uuid).order_by(Booking.created_at.desc()).all()
    booking_list = []
    completed_b = 0
    cancelled_b = 0

    for b in b_query:
        status_str = b.status.value if hasattr(b.status, 'value') else str(b.status)
        if status_str.upper() == "COMPLETED":
            completed_b += 1
        elif status_str.upper() == "CANCELLED":
            cancelled_b += 1

        service = db.query(Service).filter(Service.id == b.service_id).first()
        provider = db.query(Provider).filter(Provider.user_id == b.provider_id).first() if b.provider_id else None

        booking_list.append({
            "id": str(b.id),
            "service_id": str(b.service_id),
            "service_name": service.name if service else "Service Booking",
            "provider_name": provider.full_name if provider else "Unassigned Provider",
            "status": status_str,
            "total_price": float(b.total_price),
            "scheduled_time": b.scheduled_time.isoformat() if b.scheduled_time else "",
            "created_at": b.created_at.isoformat() if b.created_at else ""
        })

    return CustomerDetailResponse(
        id=str(customer.id),
        user_id=str(customer.user_id) if customer.user_id else None,
        full_name=customer.full_name,
        email=customer.email,
        phone=customer.phone,
        is_active=customer.is_active,
        bookings_count=len(b_query),
        completed_bookings_count=completed_b,
        cancelled_bookings_count=cancelled_b,
        is_flagged=len(flags) > 0,
        flags=flag_list,
        bookings=booking_list,
        created_at=customer.created_at.isoformat() if customer.created_at else ""
    )

@router.post("/{customer_id}/status")
def update_customer_account_status(
    customer_id: str,
    req: AccountStatusRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("customers:manage"))
):
    """Suspend or reactivate customer account."""
    try:
        c_uuid = uuid.UUID(customer_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid customer ID format")

    customer = customer_repository.get_customer_by_id(db, c_uuid)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer.is_active = req.is_active
    # Also update user active status if linked
    if customer.user_id:
        user = db.query(User).filter(User.id == customer.user_id).first()
        if user:
            user.is_active = req.is_active

    db.commit()

    action_str = "Reactivated" if req.is_active else "Suspended"
    audit_repository.create_audit_log(
        db, actor_id=admin.id, actor_email=admin.email, actor_role=admin.role,
        action=f"Customer Account {action_str} ({customer.email})",
        target_resource=str(c_uuid),
        metadata_json={"reason": req.reason or "Admin Action"}
    )

    return {
        "status": "success",
        "customer_id": customer_id,
        "is_active": req.is_active,
        "message": f"Customer {customer.full_name} status updated to {action_str.lower()}."
    }

@router.post("/{customer_id}/flag")
def flag_customer_account(
    customer_id: str,
    req: CustomerFlagRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("customers:manage"))
):
    """Flag customer account for fraudulent or suspicious behavior."""
    try:
        c_uuid = uuid.UUID(customer_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid customer ID format")

    customer = customer_repository.get_customer_by_id(db, c_uuid)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    flag_entry = CustomerFlag(
        id=uuid.uuid4(),
        customer_id=c_uuid,
        flag_type=req.flag_type,
        reason=req.reason,
        flagged_by=admin.id
    )
    db.add(flag_entry)
    db.commit()

    audit_repository.create_audit_log(
        db, actor_id=admin.id, actor_email=admin.email, actor_role=admin.role,
        action=f"Flagged Customer Account ({customer.email}) for {req.flag_type}",
        target_resource=str(c_uuid),
        risk_level="Warning",
        metadata_json={"reason": req.reason}
    )

    return {
        "status": "success",
        "customer_id": customer_id,
        "flag_type": req.flag_type,
        "message": f"Customer {customer.full_name} flagged successfully."
    }
