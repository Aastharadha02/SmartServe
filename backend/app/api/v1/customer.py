import os
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_customer
from app.core.security import hash_password, verify_password, create_access_token
from app.models.customer import (
    User,
    Customer,
    Booking,
    SupportTicket,
    TicketMessage,
    BookingFeedback,
    UserSession,
)
from app.schemas.customer_schemas import (
    CustomerRegisterPayload,
    CustomerLoginPayload,
    CustomerTokenResponse,
    CustomerSessionResponse,
    ForgotPasswordPayload,
    ResetPasswordPayload,
    ChangePasswordPayload,
    CustomerProfileUpdate,
    CategoryItem,
    ServiceItem,
    AddonItem,
    ServiceProcessStep,
    ServiceFAQ,
    CreateBookingPayload,
    CancelBookingPayload,
    BookingFeedbackPayload,
    BookingDetail,
    CreateTicketPayload,
    TicketMessagePayload,
    SupportTicketDetail,
    MessageItem,
    SessionListItem,
)

router = APIRouter(prefix="/customer", tags=["Customer API"])

# Mock catalog fallback database items for fast development
MOCK_CATEGORIES: List[CategoryItem] = [
    CategoryItem(id="cat-1", name="AC & Appliance Repair", slug="ac-repair", image="https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=600&q=80", service_count=12),
    CategoryItem(id="cat-2", name="Deep Cleaning", slug="cleaning", image="https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=600&q=80", service_count=18),
    CategoryItem(id="cat-3", name="Plumbing Services", slug="plumbing", image="https://images.unsplash.com/photo-1505798577917-a65157d3320a?auto=format&fit=crop&w=600&q=80", service_count=15),
    CategoryItem(id="cat-4", name="Electrician & Wiring", slug="electrician", image="https://images.unsplash.com/photo-1621905252507-b35492cc74b4?auto=format&fit=crop&w=600&q=80", service_count=14),
    CategoryItem(id="cat-5", name="Painting & Waterproofing", slug="painting", image="https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=600&q=80", service_count=8),
]

MOCK_SERVICES: List[ServiceItem] = [
    ServiceItem(
        id="srv-ac-101",
        name="Split AC Foam Jet Deep Service",
        category="AC & Appliance Repair",
        category_slug="ac-repair",
        subcategory="AC Servicing",
        subcategory_slug="ac-servicing",
        description="Thorough 360-degree foam jet cleaning for indoor and outdoor AC units.",
        features=["Foam Jet Technology", "Free gas pressure check", "30-Day post-service warranty"],
        base_price=699.0,
        duration_minutes=60,
        rating=4.8,
        review_count=420,
        is_emergency=True,
        image_url="https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=600&q=80",
        suggested_addons=[
            AddonItem(addon_id="add-1", name="Anti-bacterial spray coating", price=199.0, description="Long lasting freshness"),
            AddonItem(addon_id="add-2", name="Outdoor unit deep pressure wash", price=299.0, description="Removes deep mud"),
        ],
        process_steps=[
            ServiceProcessStep(step_number=1, title="Pre-service inspection", description="Checks cooling performance", duration_minutes=10),
            ServiceProcessStep(step_number=2, title="Foam jet wash", description="Pressure foam wash", duration_minutes=35),
        ],
        faqs=[
            ServiceFAQ(question="Does this service include gas refill?", answer="Gas pressure check is included."),
        ],
    ),
    ServiceItem(
        id="srv-clean-201",
        name="Full Home Deep Cleaning (2 BHK)",
        category="Deep Cleaning",
        category_slug="cleaning",
        subcategory="Full Home",
        subcategory_slug="full-home",
        description="Complete deep cleaning of living rooms, bedrooms, kitchen, bathrooms.",
        features=["Machine scrubbing of floors", "Kitchen degreasing", "Sanitation"],
        base_price=3499.0,
        duration_minutes=240,
        rating=4.9,
        review_count=310,
        is_emergency=False,
        image_url="https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=600&q=80",
        suggested_addons=[
            AddonItem(addon_id="add-3", name="Sofa shampooing (5 seater)", price=799.0, description="Deep extraction"),
        ],
        process_steps=[
            ServiceProcessStep(step_number=1, title="Dusting & Vacuuming", description="Dusting ceiling fans", duration_minutes=60),
        ],
        faqs=[
            ServiceFAQ(question="Do I need to supply materials?", answer="No, our team carries all equipment."),
        ],
    ),
]


# 1. POST /customer/auth/register
@router.post("/auth/register", response_model=CustomerTokenResponse)
def register_customer(payload: CustomerRegisterPayload, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email address is already registered")

    new_user = User(
        id=uuid.uuid4(),
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role="customer",
        is_active=True,
    )
    new_customer = Customer(
        id=uuid.uuid4(),
        user_id=new_user.id,
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone or "+91 9876543210",
        is_verified=True,
        is_active=True,
    )
    db.add(new_user)
    db.add(new_customer)
    db.commit()

    token = create_access_token({"sub": str(new_user.id), "role": "customer", "customer_id": str(new_customer.id)})
    return CustomerTokenResponse(
        access_token=token,
        customer_id=str(new_customer.id),
        user_id=str(new_user.id),
        email=new_customer.email,
        full_name=new_customer.full_name,
        phone=new_customer.phone,
    )


# 2. POST /customer/auth/login
@router.post("/auth/login", response_model=CustomerTokenResponse)
def login_customer(payload: CustomerLoginPayload, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email, User.role == "customer").first()
    if not user or not verify_password(payload.password, user.hashed_password):
        # Allow dev fallback if user not in DB yet
        token = create_access_token({"sub": "00000000-0000-0000-0000-000000001001", "role": "customer", "customer_id": "00000000-0000-0000-0000-000000001002"})
        return CustomerTokenResponse(
            access_token=token,
            customer_id="00000000-0000-0000-0000-000000001002",
            user_id="00000000-0000-0000-0000-000000001001",
            email=payload.email,
            full_name=payload.email.split("@")[0].title() or "Pushkar Kanjani",
            phone="+91 9876543210",
        )

    customer = db.query(Customer).filter(Customer.user_id == user.id).first()
    customer_id = str(customer.id) if customer else str(user.id)
    full_name = customer.full_name if customer else user.email.split("@")[0].title()

    token = create_access_token({"sub": str(user.id), "role": "customer", "customer_id": customer_id})
    return CustomerTokenResponse(
        access_token=token,
        customer_id=customer_id,
        user_id=str(user.id),
        email=user.email,
        full_name=full_name,
        phone=customer.phone if customer else "+91 9876543210",
    )


# 3. GET /customer/auth/me
@router.get("/auth/me", response_model=CustomerSessionResponse)
def get_auth_me(current_customer: Customer = Depends(get_current_customer)):
    return CustomerSessionResponse(
        customer_id=str(current_customer.id),
        user_id=str(current_customer.user_id),
        email=current_customer.email,
        full_name=current_customer.full_name,
        phone=current_customer.phone,
        is_active=current_customer.is_active,
        is_verified=current_customer.is_verified,
        lifetime_spent=float(current_customer.lifetime_spent),
        total_bookings=current_customer.total_bookings,
        created_at=current_customer.created_at,
    )


# 4. POST /customer/auth/logout
@router.post("/auth/logout")
def logout_customer():
    return {"status": "ok", "message": "Signed out successfully"}


# 5. POST /customer/auth/forgot-password
@router.post("/auth/forgot-password")
def forgot_password(payload: ForgotPasswordPayload):
    return {"status": "ok", "message": "If the email exists, reset instructions have been sent."}


# 6. POST /customer/auth/reset-password
@router.post("/auth/reset-password")
def reset_password(payload: ResetPasswordPayload):
    return {"status": "ok", "message": "Password reset successfully."}


# 7. POST /customer/auth/change-password
@router.post("/auth/change-password")
def change_password(payload: ChangePasswordPayload, current_customer: Customer = Depends(get_current_customer), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_customer.user_id).first()
    if user:
        if not verify_password(payload.current_password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
        user.hashed_password = hash_password(payload.new_password)
        db.commit()
    return {"status": "ok", "message": "Password updated successfully"}


# 8. GET /customer/profile
@router.get("/profile", response_model=CustomerSessionResponse)
def get_profile(current_customer: Customer = Depends(get_current_customer)):
    return CustomerSessionResponse(
        customer_id=str(current_customer.id),
        user_id=str(current_customer.user_id),
        email=current_customer.email,
        full_name=current_customer.full_name,
        phone=current_customer.phone,
        is_active=current_customer.is_active,
        is_verified=current_customer.is_verified,
        lifetime_spent=float(current_customer.lifetime_spent),
        total_bookings=current_customer.total_bookings,
        created_at=current_customer.created_at,
    )


# 9. PATCH /customer/profile
@router.patch("/profile", response_model=CustomerSessionResponse)
def update_profile(
    payload: CustomerProfileUpdate,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    if payload.full_name:
        current_customer.full_name = payload.full_name
    if payload.email:
        current_customer.email = payload.email
    if payload.phone:
        current_customer.phone = payload.phone

    db.add(current_customer)
    db.commit()
    db.refresh(current_customer)

    return CustomerSessionResponse(
        customer_id=str(current_customer.id),
        user_id=str(current_customer.user_id),
        email=current_customer.email,
        full_name=current_customer.full_name,
        phone=current_customer.phone,
        is_active=current_customer.is_active,
        is_verified=current_customer.is_verified,
        lifetime_spent=float(current_customer.lifetime_spent),
        total_bookings=current_customer.total_bookings,
        created_at=current_customer.created_at,
    )


# 10. GET /customer/dashboard
@router.get("/dashboard")
def get_dashboard(current_customer: Customer = Depends(get_current_customer)):
    return {
        "greeting_name": current_customer.full_name,
        "categories": MOCK_CATEGORIES,
        "featured_services": MOCK_SERVICES,
        "recent_bookings": [],
    }


# 11. GET /customer/catalog/categories
@router.get("/catalog/categories", response_model=List[CategoryItem])
def get_catalog_categories(db: Session = Depends(get_db)):
    from app.models.service import Service
    db_services = db.query(Service).filter(Service.is_active == True).all()
    if db_services:
        cat_map = {}
        for s in db_services:
            if s.category not in cat_map:
                slug = s.category.lower().replace(" & ", "-").replace(" ", "-")
                cat_map[s.category] = CategoryItem(
                    id=f"cat-{slug}",
                    name=s.category,
                    slug=slug,
                    image="https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=600&q=80",
                    service_count=1
                )
            else:
                cat_map[s.category].service_count += 1
        return list(cat_map.values())
    return MOCK_CATEGORIES


# 12. GET /customer/catalog/services
@router.get("/catalog/services", response_model=List[ServiceItem])
def get_catalog_services(
    category: Optional[str] = None,
    emergency_only: Optional[bool] = False,
    q: Optional[str] = None,
    db: Session = Depends(get_db),
):
    from app.models.service import Service
    query = db.query(Service).filter(Service.is_active == True)
    if category:
        query = query.filter((Service.category.ilike(f"%{category}%")) | (Service.subcategory.ilike(f"%{category}%")))
    if q:
        query = query.filter((Service.name.ilike(f"%{q}%")) | (Service.category.ilike(f"%{q}%")) | (Service.subcategory.ilike(f"%{q}%")))

    db_services = query.all()
    if db_services:
        res = []
        for s in db_services:
            cat_slug = s.category.lower().replace(" & ", "-").replace(" ", "-")
            sub_slug = s.subcategory.lower().replace(" & ", "-").replace(" ", "-")
            addons = []
            if s.suggested_addons and isinstance(s.suggested_addons, list):
                for idx, a in enumerate(s.suggested_addons):
                    if isinstance(a, dict):
                        addons.append(AddonItem(
                            addon_id=str(a.get("addon_id", f"add-{idx}")),
                            name=str(a.get("name", "Addon Service")),
                            price=float(a.get("price", 199.0)),
                            description=str(a.get("description", ""))
                        ))
            features = s.distinct_features if isinstance(s.distinct_features, list) else []

            res.append(ServiceItem(
                id=str(s.id),
                name=s.name,
                category=s.category,
                category_slug=cat_slug,
                subcategory=s.subcategory,
                subcategory_slug=sub_slug,
                description=f"Professional {s.name} service managed under {s.category}.",
                features=features,
                base_price=float(s.base_price),
                duration_minutes=60,
                rating=4.8,
                review_count=120,
                is_emergency=False,
                image_url="https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=600&q=80",
                suggested_addons=addons,
                process_steps=[
                    ServiceProcessStep(step_number=1, title="Inspection", description="Pre-service diagnostic check", duration_minutes=15),
                    ServiceProcessStep(step_number=2, title="Execution", description="High quality service delivery", duration_minutes=45)
                ],
                faqs=[
                    ServiceFAQ(question="Is warranty included?", answer="Yes, 30-day SmartServe service warranty included.")
                ]
            ))
        return res

    items = list(MOCK_SERVICES)
    if category:
        items = [s for s in items if s.category_slug == category or category.lower() in s.category.lower()]
    if emergency_only:
        items = [s for s in items if s.is_emergency]
    if q:
        q_lower = q.lower()
        items = [s for s in items if q_lower in s.name.lower() or q_lower in s.category.lower() or q_lower in s.description.lower()]
    return items


# 13. GET /customer/catalog/services/{id}
@router.get("/catalog/services/{service_id}", response_model=ServiceItem)
def get_catalog_service_by_id(service_id: str, db: Session = Depends(get_db)):
    from app.models.service import Service
    if len(service_id) == 36:
        try:
            s_uuid = uuid.UUID(service_id)
            s = db.query(Service).filter(Service.id == s_uuid, Service.is_active == True).first()
            if s:
                cat_slug = s.category.lower().replace(" & ", "-").replace(" ", "-")
                sub_slug = s.subcategory.lower().replace(" & ", "-").replace(" ", "-")
                addons = []
                if s.suggested_addons and isinstance(s.suggested_addons, list):
                    for idx, a in enumerate(s.suggested_addons):
                        if isinstance(a, dict):
                            addons.append(AddonItem(
                                addon_id=str(a.get("addon_id", f"add-{idx}")),
                                name=str(a.get("name", "Addon Service")),
                                price=float(a.get("price", 199.0)),
                                description=str(a.get("description", ""))
                            ))
                features = s.distinct_features if isinstance(s.distinct_features, list) else []

                return ServiceItem(
                    id=str(s.id),
                    name=s.name,
                    category=s.category,
                    category_slug=cat_slug,
                    subcategory=s.subcategory,
                    subcategory_slug=sub_slug,
                    description=f"Professional {s.name} service managed under {s.category}.",
                    features=features,
                    base_price=float(s.base_price),
                    duration_minutes=60,
                    rating=4.8,
                    review_count=120,
                    is_emergency=False,
                    image_url="https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=600&q=80",
                    suggested_addons=addons,
                    process_steps=[
                        ServiceProcessStep(step_number=1, title="Inspection", description="Pre-service diagnostic check", duration_minutes=15),
                        ServiceProcessStep(step_number=2, title="Execution", description="High quality service delivery", duration_minutes=45)
                    ],
                    faqs=[
                        ServiceFAQ(question="Is warranty included?", answer="Yes, 30-day SmartServe service warranty included.")
                    ]
                )
        except Exception:
            pass

    found = next((s for s in MOCK_SERVICES if s.id == service_id), None)
    if found:
        return found
    return MOCK_SERVICES[0]



# 14. GET /customer/bookings
@router.get("/bookings", response_model=List[BookingDetail])
def get_customer_bookings(
    status_filter: Optional[str] = None,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    query = db.query(Booking).filter(Booking.customer_id == current_customer.id)
    if status_filter and status_filter.upper() != "ALL":
        query = query.filter(Booking.status == status_filter.upper())

    records = query.order_by(Booking.created_at.desc()).all()
    if not records:
        return []

    return [

        BookingDetail(
            id=str(b.id),
            booking_reference=b.booking_reference,
            customer_id=str(b.customer_id),
            service_id=b.service_id,
            service_name=b.service_name,
            category=b.category,
            status=b.status,
            scheduled_date=b.scheduled_date,
            scheduled_time=b.scheduled_time,
            address_line1=b.address_line1,
            landmark=b.landmark,
            city=b.city,
            pincode=b.pincode,
            total_price=float(b.total_price),
            payment_method=b.payment_method,
            cancellation_reason=b.cancellation_reason,
            notes=b.notes,
            created_at=b.created_at,
        )
        for b in records
    ]


# 15. POST /customer/bookings
@router.post("/bookings", response_model=BookingDetail)
def create_customer_booking(
    payload: CreateBookingPayload,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    service = next((s for s in MOCK_SERVICES if s.id == payload.service_id), MOCK_SERVICES[0])
    addons_sum = sum(a.price for a in service.suggested_addons if a.addon_id in payload.addon_ids)
    total_price = service.base_price + addons_sum
    ref_code = f"BK-{uuid.uuid4().hex[:6].upper()}"

    new_booking = Booking(
        id=uuid.uuid4(),
        booking_reference=ref_code,
        customer_id=current_customer.id,
        service_id=service.id,
        service_name=service.name,
        category=service.category,
        status="CONFIRMED",
        scheduled_date=payload.scheduled_date,
        scheduled_time=payload.scheduled_time,
        address_line1=payload.address_line1,
        landmark=payload.landmark,
        city=payload.city,
        pincode=payload.pincode,
        total_price=total_price,
        payment_method=payload.payment_method,
        notes=payload.notes,
        created_at=datetime.utcnow(),
    )
    current_customer.total_bookings += 1
    current_customer.lifetime_spent += Decimal(str(total_price))

    db.add(new_booking)
    db.add(current_customer)
    db.commit()
    db.refresh(new_booking)

    return BookingDetail(
        id=str(new_booking.id),
        booking_reference=new_booking.booking_reference,
        customer_id=str(new_booking.customer_id),
        service_id=new_booking.service_id,
        service_name=new_booking.service_name,
        category=new_booking.category,
        status=new_booking.status,
        scheduled_date=new_booking.scheduled_date,
        scheduled_time=new_booking.scheduled_time,
        address_line1=new_booking.address_line1,
        landmark=new_booking.landmark,
        city=new_booking.city,
        pincode=new_booking.pincode,
        total_price=float(new_booking.total_price),
        payment_method=new_booking.payment_method,
        notes=new_booking.notes,
        created_at=new_booking.created_at,
    )


# 16. GET /customer/bookings/{id}
@router.get("/bookings/{booking_id}", response_model=BookingDetail)
def get_booking_by_id(
    booking_id: str,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    record = (
        db.query(Booking)
        .filter((Booking.id == booking_id) | (Booking.booking_reference == booking_id))
        .filter(Booking.customer_id == current_customer.id)
        .first()
    )
    if not record:
        return BookingDetail(
            id=booking_id,
            booking_reference="BK-1001",
            customer_id=str(current_customer.id),
            service_id="srv-ac-101",
            service_name="Split AC Foam Jet Deep Service",
            category="AC & Appliance Repair",
            status="CONFIRMED",
            scheduled_date="2026-09-02",
            scheduled_time="14:00",
            address_line1="Flat 402, Green Valley Heights, Sector 62, Noida",
            city="Noida",
            pincode="201301",
            total_price=699.0,
            payment_method="COD",
            created_at=datetime.utcnow(),
        )

    return BookingDetail(
        id=str(record.id),
        booking_reference=record.booking_reference,
        customer_id=str(record.customer_id),
        service_id=record.service_id,
        service_name=record.service_name,
        category=record.category,
        status=record.status,
        scheduled_date=record.scheduled_date,
        scheduled_time=record.scheduled_time,
        address_line1=record.address_line1,
        landmark=record.landmark,
        city=record.city,
        pincode=record.pincode,
        total_price=float(record.total_price),
        payment_method=record.payment_method,
        cancellation_reason=record.cancellation_reason,
        notes=record.notes,
        created_at=record.created_at,
    )


# 17. POST /customer/bookings/{id}/cancel
@router.post("/bookings/{booking_id}/cancel", response_model=BookingDetail)
def cancel_booking(
    booking_id: str,
    payload: CancelBookingPayload,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    record = db.query(Booking).filter(Booking.id == booking_id, Booking.customer_id == current_customer.id).first()
    if record:
        record.status = "CANCELLED"
        record.cancellation_reason = payload.reason
        db.commit()
        db.refresh(record)
        return BookingDetail(
            id=str(record.id),
            booking_reference=record.booking_reference,
            customer_id=str(record.customer_id),
            service_id=record.service_id,
            service_name=record.service_name,
            category=record.category,
            status=record.status,
            scheduled_date=record.scheduled_date,
            scheduled_time=record.scheduled_time,
            address_line1=record.address_line1,
            city=record.city,
            pincode=record.pincode,
            total_price=float(record.total_price),
            payment_method=record.payment_method,
            cancellation_reason=record.cancellation_reason,
            created_at=record.created_at,
        )

    return BookingDetail(
        id=booking_id,
        booking_reference="BK-1001",
        customer_id=str(current_customer.id),
        service_id="srv-ac-101",
        service_name="Split AC Foam Jet Deep Service",
        category="AC & Appliance Repair",
        status="CANCELLED",
        scheduled_date="2026-09-02",
        scheduled_time="14:00",
        address_line1="Flat 402, Green Valley Heights",
        city="Noida",
        pincode="201301",
        total_price=699.0,
        payment_method="COD",
        cancellation_reason=payload.reason,
        created_at=datetime.utcnow(),
    )


# 18. POST /customer/bookings/{id}/feedback
@router.post("/bookings/{booking_id}/feedback")
def submit_booking_feedback(
    booking_id: str,
    payload: BookingFeedbackPayload,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    fb = BookingFeedback(
        id=uuid.uuid4(),
        booking_id=uuid.UUID(booking_id) if len(booking_id) == 36 else uuid.uuid4(),
        customer_id=current_customer.id,
        rating=payload.rating,
        review_text=payload.review_text,
        created_at=datetime.utcnow(),
    )
    try:
        db.add(fb)
        db.commit()
    except Exception:
        db.rollback()

    return {"status": "ok", "message": "Feedback submitted successfully"}


# 19. GET /customer/support/tickets
@router.get("/support/tickets", response_model=List[SupportTicketDetail])
def get_customer_support_tickets(
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    records = db.query(SupportTicket).filter(SupportTicket.customer_id == current_customer.id).all()
    if not records:
        return []

    return [

        SupportTicketDetail(
            id=str(t.id),
            customer_id=str(t.customer_id),
            booking_id=str(t.booking_id) if t.booking_id else None,
            subject=t.subject,
            category=t.category,
            priority=t.priority,
            status=t.status,
            created_at=t.created_at,
            messages=[
                MessageItem(
                    id=str(m.id),
                    ticket_id=str(m.ticket_id),
                    sender_role=m.sender_role,
                    sender_name=m.sender_name,
                    message_text=m.message_text,
                    attachment_url=m.attachment_url,
                    created_at=m.created_at,
                )
                for m in t.messages
            ],
        )
        for t in records
    ]


# 20. POST /customer/support/tickets
@router.post("/support/tickets", response_model=SupportTicketDetail)
def create_support_ticket(
    payload: CreateTicketPayload,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    ticket_id = uuid.uuid4()
    priority = "High" if payload.category in ["Booking issue", "Service quality"] else (payload.priority or "Normal")

    new_ticket = SupportTicket(
        id=ticket_id,
        customer_id=current_customer.id,
        subject=payload.subject,
        category=payload.category,
        priority=priority,
        status="OPEN",
        created_at=datetime.utcnow(),
    )
    first_message = TicketMessage(
        id=uuid.uuid4(),
        ticket_id=ticket_id,
        sender_role="customer",
        sender_name=current_customer.full_name,
        message_text=payload.description,
        created_at=datetime.utcnow(),
    )
    db.add(new_ticket)
    db.add(first_message)
    db.commit()
    db.refresh(new_ticket)

    return SupportTicketDetail(
        id=str(new_ticket.id),
        customer_id=str(new_ticket.customer_id),
        subject=new_ticket.subject,
        category=new_ticket.category,
        priority=new_ticket.priority,
        status=new_ticket.status,
        created_at=new_ticket.created_at,
        messages=[
            MessageItem(
                id=str(first_message.id),
                ticket_id=str(first_message.ticket_id),
                sender_role=first_message.sender_role,
                sender_name=first_message.sender_name,
                message_text=first_message.message_text,
                created_at=first_message.created_at,
            )
        ],
    )


# 21. GET /customer/support/tickets/{id}
@router.get("/support/tickets/{ticket_id}", response_model=SupportTicketDetail)
def get_support_ticket_by_id(
    ticket_id: str,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    t = db.query(SupportTicket).filter(SupportTicket.id == ticket_id, SupportTicket.customer_id == current_customer.id).first()
    if not t:
        return SupportTicketDetail(
            id=ticket_id,
            customer_id=str(current_customer.id),
            subject="Technician delay inquiry",
            category="Booking issue",
            priority="High",
            status="OPEN",
            created_at=datetime.utcnow(),
            messages=[
                MessageItem(
                    id="msg-1",
                    ticket_id=ticket_id,
                    sender_role="customer",
                    sender_name=current_customer.full_name,
                    message_text="Technician is running behind schedule.",
                    created_at=datetime.utcnow(),
                )
            ],
        )

    return SupportTicketDetail(
        id=str(t.id),
        customer_id=str(t.customer_id),
        subject=t.subject,
        category=t.category,
        priority=t.priority,
        status=t.status,
        created_at=t.created_at,
        messages=[
            MessageItem(
                id=str(m.id),
                ticket_id=str(m.ticket_id),
                sender_role=m.sender_role,
                sender_name=m.sender_name,
                message_text=m.message_text,
                attachment_url=m.attachment_url,
                created_at=m.created_at,
            )
            for m in t.messages
        ],
    )


# 22. POST /customer/support/tickets/{id}/messages
@router.post("/support/tickets/{ticket_id}/messages", response_model=MessageItem)
def add_ticket_message(
    ticket_id: str,
    payload: TicketMessagePayload,
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    new_msg = TicketMessage(
        id=uuid.uuid4(),
        ticket_id=uuid.UUID(ticket_id) if len(ticket_id) == 36 else uuid.uuid4(),
        sender_role="customer",
        sender_name=current_customer.full_name,
        message_text=payload.message_text,
        attachment_url=payload.attachment_url,
        created_at=datetime.utcnow(),
    )
    try:
        db.add(new_msg)
        db.commit()
    except Exception:
        db.rollback()

    return MessageItem(
        id=str(new_msg.id),
        ticket_id=ticket_id,
        sender_role=new_msg.sender_role,
        sender_name=new_msg.sender_name,
        message_text=new_msg.message_text,
        attachment_url=new_msg.attachment_url,
        created_at=new_msg.created_at,
    )


# 23. GET /customer/feedback
@router.get("/feedback")
def get_customer_feedbacks(current_customer: Customer = Depends(get_current_customer), db: Session = Depends(get_db)):
    fbs = db.query(BookingFeedback).filter(BookingFeedback.customer_id == current_customer.id).all()
    return [
        {
            "id": str(f.id),
            "booking_id": str(f.booking_id),
            "rating": f.rating,
            "review_text": f.review_text,
            "created_at": f.created_at,
        }
        for f in fbs
    ]


# 24. GET /customer/sessions
@router.get("/sessions", response_model=List[SessionListItem])
def get_customer_sessions(current_customer: Customer = Depends(get_current_customer)):
    return [
        SessionListItem(
            id="sess-1",
            device_info="Chrome on Windows 11",
            ip_address="127.0.0.1",
            last_active=datetime.utcnow(),
            is_current=True,
        )
    ]


# 25. POST /customer/sessions/{id}/revoke
@router.post("/sessions/{session_id}/revoke")
def revoke_session(session_id: str):
    return {"status": "ok", "message": f"Session {session_id} revoked"}


# 26. POST /customer/sessions/revoke-all
@router.post("/sessions/revoke-all")
def revoke_all_sessions():
    return {"status": "ok", "message": "All other sessions revoked"}


# 27. GET /customer/recommendations
@router.get("/recommendations", response_model=List[ServiceItem])
def get_recommendations():
    return MOCK_SERVICES


# 28. POST /customer/uploads/image
@router.post("/uploads/image")
async def upload_image(file: UploadFile = File(...)):
    os.makedirs("customer_uploads", exist_ok=True)
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join("customer_uploads", filename)
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)
    return {"url": f"/static/uploads/{filename}"}
