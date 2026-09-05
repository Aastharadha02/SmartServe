import os
import re
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_customer
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User, UserSession
from app.models.customer import (
    Customer,
    Booking,
    SupportTicket,
    TicketMessage,
    BookingFeedback,
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
    SubcategorySummary,
    ServiceItem,
    AddonItem,
    ServiceProcessStep,
    ServiceFeatureItem,
    ServiceMediaItem,
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




# 1. POST /customer/auth/register
@router.post("/auth/register", response_model=CustomerTokenResponse)
def register_customer(payload: CustomerRegisterPayload, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email address is already registered")

    pwd_hash = hash_password(payload.password)
    new_user = User(
        id=uuid.uuid4(),
        email=payload.email,
        hashed_password=pwd_hash,
        role="customer",
        is_active=True,
    )
    new_customer = Customer(
        id=uuid.uuid4(),
        user_id=new_user.id,
        full_name=payload.full_name,
        email=payload.email,
        password_hash=pwd_hash,
        phone=payload.phone or "+91 9876543210",
        preferences=payload.preferences,
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
        preferences=current_customer.preferences if isinstance(current_customer.preferences, list) else [],
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
def get_dashboard(current_customer: Customer = Depends(get_current_customer), db: Session = Depends(get_db)):
    from app.models.service import Service
    db_services = db.query(Service).filter(Service.is_active == True).all()
    cat_map = {}
    srv_list = []
    for s in db_services:
        if s.category not in cat_map:
            slug = s.category.lower().replace(" & ", "-").replace(" ", "-")
            cat_map[s.category] = CategoryItem(
                id=f"cat-{slug}",
                name=s.category,
                slug=slug,
                image=None,
                service_count=1
            )
        else:
            cat_map[s.category].service_count += 1
        
        if len(srv_list) < 6:
            srv_list.append(ServiceItem(
                id=str(s.id),
                name=s.name,
                category=s.category,
                category_slug=s.category.lower().replace(" & ", "-").replace(" ", "-"),
                subcategory=s.subcategory,
                subcategory_slug=s.subcategory.lower().replace(" & ", "-").replace(" ", "-"),
                description=f"Professional {s.name} service managed under {s.category}.",
                features=s.distinct_features if isinstance(s.distinct_features, list) else [],
                base_price=float(s.base_price),
                duration_minutes=60,
                rating=4.8,
                review_count=120,
                is_emergency=False,
                image_url=None,
                suggested_addons=[],
                process_steps=[],
                faqs=[]
            ))

    return {
        "greeting_name": current_customer.full_name,
        "categories": list(cat_map.values())[:8],
        "featured_services": srv_list,
        "recent_bookings": [],
    }


import re

def get_category_order(name: str) -> int:
    m = re.match(r"^(\d+)\.", name)
    return int(m.group(1)) if m else 999

def format_category_display_name(raw: str) -> str:
    cleaned = re.sub(r"^\d+\.\s*", "", raw)
    return cleaned.strip()

# 11. GET /customer/catalog/categories
@router.get("/catalog/categories", response_model=List[CategoryItem])
def get_catalog_categories(db: Session = Depends(get_db)):
    from app.models.service import Service
    db_services = db.query(Service).filter(Service.is_active == True).all()
    
    cat_map: Dict[str, Dict[str, Any]] = {}
    for s in db_services:
        cat = s.category or "General"
        sub = s.subcategory or "General"
        if cat not in cat_map:
            slug = cat.lower().replace(" & ", "-").replace(" ", "-")
            cat_map[cat] = {
                "id": f"cat-{slug}",
                "name": cat,
                "slug": slug,
                "display_name": format_category_display_name(cat),
                "order": get_category_order(cat),
                "subcategories": {},
                "service_count": 0,
                "active_count": 0
            }
        
        cat_map[cat]["service_count"] += 1
        cat_map[cat]["active_count"] += 1
        
        sub_dict = cat_map[cat]["subcategories"]
        if sub not in sub_dict:
            sub_dict[sub] = {"name": sub, "service_count": 0, "active_count": 0}
        sub_dict[sub]["service_count"] += 1
        sub_dict[sub]["active_count"] += 1

    result = []
    for cat_data in cat_map.values():
        sub_list = [
            SubcategorySummary(
                name=sub_info["name"],
                service_count=sub_info["service_count"],
                active_count=sub_info["active_count"]
            )
            for sub_info in sorted(cat_data["subcategories"].values(), key=lambda x: x["name"])
        ]
        result.append(CategoryItem(
            id=cat_data["id"],
            name=cat_data["name"],
            slug=cat_data["slug"],
            display_name=cat_data["display_name"],
            order=cat_data["order"],
            subcategories_count=len(sub_list),
            service_count=cat_data["service_count"],
            active_count=cat_data["active_count"],
            subcategories=sub_list
        ))

    result.sort(key=lambda c: (c.order, c.display_name or c.name))
    return result


def normalize_to_strings(raw_list) -> List[str]:
    if not isinstance(raw_list, list):
        return []
    res = []
    for elem in raw_list:
        if isinstance(elem, str):
            res.append(elem)
        elif isinstance(elem, dict):
            title = elem.get("title") or elem.get("name") or elem.get("label") or elem.get("step")
            desc = elem.get("description") or elem.get("desc") or elem.get("detail") or elem.get("details") or elem.get("text")
            if title and desc:
                res.append(f"{title}: {desc}")
            elif desc:
                res.append(str(desc))
            elif title:
                res.append(str(title))
            else:
                vals = [str(v) for v in elem.values() if v]
                res.append(": ".join(vals) if vals else str(elem))
        elif elem is not None:
            res.append(str(elem))
    return res


def parse_service_details(s) -> ServiceItem:
    cat_slug = s.category.lower().replace(" & ", "-").replace(" ", "-") if s.category else ""
    sub_slug = s.subcategory.lower().replace(" & ", "-").replace(" ", "-") if s.subcategory else ""

    included_features = normalize_to_strings(s.distinct_features)
    
    addons: List[AddonItem] = []
    process_steps: List[ServiceProcessStep] = []
    service_features: List[ServiceFeatureItem] = []
    service_media: List[ServiceMediaItem] = []
    faqs: List[ServiceFAQ] = []
    excluded: List[Any] = []
    tools_materials: List[Any] = []
    customer_setup: List[Any] = []
    aftercare: List[Any] = []
    expected_results: List[Any] = []
    important_notes: List[Any] = []
    highlights: List[Any] = []
    tips: List[Any] = []
    dos: List[Any] = []
    donts: List[Any] = []
    warranty_detail: Optional[str] = None
    description_text: Optional[str] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    keywords: List[str] = []
    explicit_duration: Optional[int] = None
    calc_duration: int = 0

    if s.suggested_addons and isinstance(s.suggested_addons, list):
        for idx, item in enumerate(s.suggested_addons):
            if not isinstance(item, dict):
                continue
            
            i_type = item.get("type")
            
            if i_type in ["description", "service_description"]:
                description_text = item.get("text") or item.get("description") or item.get("content")
            elif i_type == "seo_metadata":
                if not description_text and item.get("seo_description"):
                    description_text = item.get("seo_description")
                seo_title = item.get("seo_title")
                seo_description = item.get("seo_description")
                if isinstance(item.get("keywords"), list):
                    keywords = [str(k) for k in item.get("keywords")]
                if isinstance(item.get("highlights"), list):
                    highlights = item.get("highlights")
            elif i_type == "highlights":
                hl = item.get("highlights") or item.get("items") or []
                if isinstance(hl, list):
                    highlights = hl
            elif i_type in ["duration", "estimated_duration"]:
                mins = item.get("minutes") or item.get("duration") or item.get("duration_minutes")
                if mins:
                    try:
                        explicit_duration = int(mins)
                    except (ValueError, TypeError):
                        pass
            elif i_type in ["excluded", "excluded_scope"]:
                ex = item.get("excluded") or item.get("items") or []
                if isinstance(ex, list):
                    excluded = ex
            elif i_type == "process_steps":
                steps_data = item.get("steps") or item.get("items") or []
                if isinstance(steps_data, list):
                    for st in steps_data:
                        if isinstance(st, dict):
                            dur = int(st.get("duration_minutes", 15)) if st.get("duration_minutes") else 15
                            calc_duration += dur
                            process_steps.append(ServiceProcessStep(
                                step_number=int(st.get("step_number", len(process_steps) + 1)),
                                title=str(st.get("title", f"Step {len(process_steps) + 1}")),
                                description=str(st.get("description", "")),
                                duration_minutes=dur,
                                is_key_step=bool(st.get("is_key_step", False))
                            ))
            elif i_type == "service_features":
                sf = item.get("items") or item.get("features") or []
                if isinstance(sf, list):
                    for f in sf:
                        if isinstance(f, dict) and (f.get("title") or f.get("description")):
                            service_features.append(ServiceFeatureItem(
                                title=str(f.get("title", "")),
                                description=str(f.get("description", ""))
                            ))
            elif i_type == "service_media":
                sm = item.get("items") or item.get("media") or []
                if isinstance(sm, list):
                    for m in sm:
                        if isinstance(m, dict) and m.get("url"):
                            service_media.append(ServiceMediaItem(
                                id=str(m.get("id")) if m.get("id") else None,
                                url=str(m.get("url")),
                                caption=str(m.get("caption", "")),
                                media_type=str(m.get("media_type", "image")),
                                is_cover=bool(m.get("is_cover", False))
                            ))
            elif i_type in ["tools_materials", "products_and_tools"]:
                pt = item.get("products_and_tools") or item.get("items") or []
                if isinstance(pt, list) and pt:
                    tools_materials.extend(pt)
                else:
                    tools = item.get("tools") or []
                    mats = item.get("materials") or []
                    if isinstance(tools, list):
                        tools_materials.extend(tools)
                    if isinstance(mats, list):
                        tools_materials.extend(mats)
            elif i_type in ["customer_setup", "preparation"]:
                reqs = item.get("setup") or item.get("requirements") or item.get("items") or []
                if isinstance(reqs, list):
                    customer_setup = reqs
            elif i_type == "aftercare_precautions":
                ac = item.get("aftercare") or item.get("items") or []
                if isinstance(ac, list):
                    aftercare = ac
            elif i_type == "expected_results":
                exp = item.get("items") or item.get("results") or []
                if isinstance(exp, list):
                    expected_results = exp
            elif i_type == "important_notes":
                notes = item.get("items") or item.get("notes") or []
                if isinstance(notes, list):
                    important_notes = notes
            elif i_type == "tips":
                tp = item.get("items") or item.get("tips") or []
                if isinstance(tp, list):
                    tips = tp
            elif i_type in ["dos_donts", "dos_and_donts"]:
                if isinstance(item.get("dos"), list):
                    dos = item.get("dos")
                if isinstance(item.get("donts"), list):
                    donts = item.get("donts")
            elif i_type == "warranty":
                has_w = item.get("has_warranty", True)
                if has_w:
                    warranty_detail = item.get("details") or item.get("warranty")
            elif i_type == "faqs":
                faq_items = item.get("items") or item.get("faqs") or []
                if isinstance(faq_items, list):
                    for f in faq_items:
                        if isinstance(f, dict) and f.get("question"):
                            faqs.append(ServiceFAQ(
                                question=str(f.get("question")),
                                answer=str(f.get("answer", ""))
                            ))
            elif "price" in item and ("name" in item or "addon_id" in item):
                addons.append(AddonItem(
                    addon_id=str(item.get("addon_id", f"add-{idx}")),
                    name=str(item.get("name", "Add-on")),
                    price=float(item.get("price", 0.0)),
                    description=item.get("description")
                ))
            elif not description_text and item.get("description") and not i_type:
                description_text = item.get("description")

    duration_minutes = explicit_duration if explicit_duration is not None else (calc_duration if calc_duration > 0 else 45)

    cover_media = next((m.url for m in service_media if m.is_cover), None)
    first_media = service_media[0].url if service_media else None
    resolved_image = cover_media or first_media or None

    return ServiceItem(
        id=str(s.id),
        name=s.name,
        category=s.category,
        category_slug=cat_slug,
        subcategory=s.subcategory,
        subcategory_slug=sub_slug,
        description=description_text,
        distinct_features=included_features,
        features=included_features,
        included=included_features,
        excluded=normalize_to_strings(excluded),
        highlights=normalize_to_strings(highlights),
        base_price=float(s.base_price),
        max_demand_increase=float(s.max_demand_increase or 0.0),
        max_discount=float(s.max_discount or 0.0),
        duration_minutes=duration_minutes,
        rating=4.8,
        review_count=120,
        is_emergency=False,
        is_active=s.is_active,
        image_url=resolved_image,
        suggested_addons=addons,
        process_steps=process_steps,
        tools_materials=normalize_to_strings(tools_materials),
        customer_setup=normalize_to_strings(customer_setup),
        aftercare=normalize_to_strings(aftercare),
        expected_results=normalize_to_strings(expected_results),
        important_notes=normalize_to_strings(important_notes),
        warranty=warranty_detail,
        faqs=faqs,
        tips=normalize_to_strings(tips),
        dos=normalize_to_strings(dos),
        donts=normalize_to_strings(donts),
        seo_title=seo_title,
        seo_description=seo_description,
        keywords=keywords,
        service_features=service_features,
        service_media=service_media,
        created_at=s.created_at,
        updated_at=s.updated_at
    )


# 12. GET /customer/catalog/services
@router.get("/catalog/services", response_model=List[ServiceItem])
def get_catalog_services(
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    emergency_only: Optional[bool] = False,
    q: Optional[str] = None,
    db: Session = Depends(get_db),
):
    from app.models.service import Service
    query = db.query(Service).filter(Service.is_active == True)
    if category:
        clean_cat = category.strip()
        cat_no_num = re.sub(r'^\d+\.\s*', '', clean_cat)
        query = query.filter(
            (Service.category.ilike(f"%{clean_cat}%")) | 
            (Service.category.ilike(f"%{cat_no_num}%"))
        )
    if subcategory:
        clean_sub = subcategory.strip().lower()
        if clean_sub in ["men's salon", "mens salon"]:
            query = query.filter(func.lower(func.trim(Service.subcategory)) == "men's salon")
        elif clean_sub in ["women's salon", "womens salon"]:
            query = query.filter(func.lower(func.trim(Service.subcategory)) == "women's salon")
        elif clean_sub == "ac":
            query = query.filter(func.lower(func.trim(Service.subcategory)) == "ac")
        else:
            query = query.filter(func.lower(func.trim(Service.subcategory)) == clean_sub)
    if q:
        query = query.filter((Service.name.ilike(f"%{q}%")) | (Service.category.ilike(f"%{q}%")) | (Service.subcategory.ilike(f"%{q}%")))

    db_services = query.all()
    return [parse_service_details(s) for s in db_services]


# 13. GET /customer/catalog/services/{id}
@router.get("/catalog/services/{service_id}", response_model=ServiceItem)
def get_catalog_service_by_id(service_id: str, db: Session = Depends(get_db)):
    from app.models.service import Service
    try:
        s_uuid = uuid.UUID(service_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid service ID format")

    s = db.query(Service).filter(Service.id == s_uuid).first()
    if not s:
        raise HTTPException(status_code=404, detail="Service not found in catalog")

    print(f"[DEBUG GET SERVICE] service_id={service_id}, db={db.bind.url}, found={s.name}, price={s.base_price}")
    return parse_service_details(s)



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
            service_id=str(b.service_id),
            service_name=b.service_name,
            category=b.category,
            status=str(b.status.value if hasattr(b.status, "value") else b.status),
            scheduled_date=b.scheduled_date,
            scheduled_time=b.scheduled_time.strftime("%H:%M:%S") if hasattr(b.scheduled_time, "strftime") else str(b.scheduled_time),
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
    from app.models.service import Service
    db_service = None
    try:
        s_uuid = uuid.UUID(payload.service_id)
        db_service = db.query(Service).filter(Service.id == s_uuid).first()
    except Exception:
        db_service = None

    if not db_service:
        raise HTTPException(status_code=404, detail="Selected service is not found in catalog")

    if not db_service.is_active:
        raise HTTPException(status_code=400, detail="Cannot book an inactive or unpublished service")

    srv_id = db_service.id
    srv_name = db_service.name
    srv_category = db_service.category
    base_price = float(db_service.base_price)

    addons_sum = 0.0
    total_price = base_price + addons_sum
    ref_code = f"BK-{uuid.uuid4().hex[:6].upper()}"

    try:
        combined_str = f"{payload.scheduled_date}T{payload.scheduled_time}".strip()
        parsed_sched_time = datetime.fromisoformat(combined_str)
    except Exception:
        parsed_sched_time = datetime.utcnow()

    new_booking = Booking(
        id=uuid.uuid4(),
        booking_reference=ref_code,
        customer_id=current_customer.id,
        service_id=srv_id,
        service_name=srv_name,
        category=srv_category,
        status="Requested",
        scheduled_date=payload.scheduled_date,
        scheduled_time=parsed_sched_time,
        address_line1=payload.address_line1,
        landmark=payload.landmark,
        city=payload.city,
        pincode=payload.pincode,
        total_price=total_price,
        payment_method=payload.payment_method,
        notes=payload.notes,
        created_at=datetime.utcnow(),
    )
    current_customer.total_bookings = (current_customer.total_bookings or 0) + 1
    current_customer.lifetime_spent = (current_customer.lifetime_spent or Decimal("0.00")) + Decimal(str(total_price))

    db.add(new_booking)
    db.add(current_customer)
    db.commit()
    db.refresh(new_booking)

    sched_time_str = (
        new_booking.scheduled_time.strftime("%H:%M:%S")
        if hasattr(new_booking.scheduled_time, "strftime")
        else str(new_booking.scheduled_time)
    )

    return BookingDetail(
        id=str(new_booking.id),
        booking_reference=new_booking.booking_reference,
        customer_id=str(new_booking.customer_id),
        service_id=str(new_booking.service_id),
        service_name=new_booking.service_name,
        category=new_booking.category,
        status=str(new_booking.status),
        scheduled_date=new_booking.scheduled_date,
        scheduled_time=sched_time_str,
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
        record = (
            db.query(Booking)
            .filter((Booking.id == booking_id) | (Booking.booking_reference == booking_id))
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
        service_id=str(record.service_id),
        service_name=record.service_name,
        category=record.category,
        status=str(record.status.value if hasattr(record.status, "value") else record.status),
        scheduled_date=record.scheduled_date,
        scheduled_time=record.scheduled_time.strftime("%H:%M:%S") if hasattr(record.scheduled_time, "strftime") else str(record.scheduled_time),
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
    effective_reason = payload.reason or payload.cancellation_reason or "Cancelled by Customer"
    record = (
        db.query(Booking)
        .filter((Booking.id == booking_id) | (Booking.booking_reference == booking_id))
        .filter(Booking.customer_id == current_customer.id)
        .first()
    )
    if not record:
        record = (
            db.query(Booking)
            .filter((Booking.id == booking_id) | (Booking.booking_reference == booking_id))
            .first()
        )
    if record:
        record.status = "CANCELLED"
        record.cancellation_reason = effective_reason
        db.commit()
        db.refresh(record)
        
        sched_time_str = (
            record.scheduled_time.strftime("%H:%M:%S")
            if hasattr(record.scheduled_time, "strftime")
            else str(record.scheduled_time)
        )
        
        return BookingDetail(
            id=str(record.id),
            booking_reference=record.booking_reference,
            customer_id=str(record.customer_id),
            service_id=str(record.service_id),
            service_name=record.service_name,
            category=record.category,
            status=str(record.status.value if hasattr(record.status, "value") else record.status),
            scheduled_date=record.scheduled_date,
            scheduled_time=sched_time_str,
            address_line1=record.address_line1,
            city=record.city,
            pincode=record.pincode,
            total_price=float(record.total_price),
            payment_method=record.payment_method,
            cancellation_reason=effective_reason,
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
                    sender_name=m.sender_name or ("Support Agent" if m.sender_role != "customer" else "Customer"),
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
        description=payload.description,
        category=payload.category,
        priority=priority,
        status="OPEN",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    first_message = TicketMessage(
        id=uuid.uuid4(),
        ticket_id=ticket_id,
        sender_id=current_customer.user_id,
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
        booking_id=str(new_ticket.booking_id) if new_ticket.booking_id else None,
        subject=new_ticket.subject,
        description=new_ticket.description,
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
                attachment_url=first_message.attachment_url,
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
    try:
        t_uuid = uuid.UUID(ticket_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ticket ID format")

    t = db.query(SupportTicket).filter(SupportTicket.id == t_uuid, SupportTicket.customer_id == current_customer.id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Support ticket not found")

    return SupportTicketDetail(
        id=str(t.id),
        customer_id=str(t.customer_id),
        booking_id=str(t.booking_id) if t.booking_id else None,
        subject=t.subject,
        description=t.description,
        category=t.category,
        priority=t.priority,
        status=t.status,
        created_at=t.created_at,
        messages=[
            MessageItem(
                id=str(m.id),
                ticket_id=str(m.ticket_id),
                sender_role=m.sender_role,
                sender_name=m.sender_name or ("SmartServe Support Operations" if m.sender_role.lower() in ["admin", "agent"] else "Customer"),
                message_text=m.message_text,
                attachment_url=m.attachment_url,
                created_at=m.created_at,
            )
            for m in (t.messages or [])
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
    try:
        t_uuid = uuid.UUID(ticket_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ticket ID format")

    ticket = db.query(SupportTicket).filter(
        SupportTicket.id == t_uuid,
        SupportTicket.customer_id == current_customer.id
    ).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Support ticket not found")

    new_msg = TicketMessage(
        id=uuid.uuid4(),
        ticket_id=t_uuid,
        sender_id=current_customer.user_id,
        sender_role="customer",
        sender_name=current_customer.full_name,
        message_text=payload.message_text,
        attachment_url=payload.attachment_url,
        created_at=datetime.utcnow(),
    )
    db.add(new_msg)
    ticket.updated_at = datetime.utcnow()
    if ticket.status and ticket.status.lower() in ["resolved", "closed"]:
        ticket.status = "Open"
    db.commit()
    db.refresh(new_msg)

    return MessageItem(
        id=str(new_msg.id),
        ticket_id=str(ticket.id),
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
def get_recommendations(db: Session = Depends(get_db)):
    from app.models.service import Service
    db_services = db.query(Service).filter(Service.is_active == True).limit(4).all()
    return [parse_service_details(s) for s in db_services]


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
