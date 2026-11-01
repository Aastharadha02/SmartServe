import uuid
from typing import List, Optional
from decimal import Decimal
from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import AuthUser, require_provider
from app.models.user import User
from app.models.customer import Booking
from app.schemas.security_ext import TotpSetupResponse, TotpVerifyRequest

from app.services.provider.provider_service import ProviderServiceDomain
from app.services.booking.state_machine import transition_booking_status
from app.schemas.provider import (
    ProviderProfileResponse,
    ProviderProfileUpdate,
    ProviderServiceCreate,
    ProviderServiceUpdate,
    ProviderServiceResponse,
    AvailabilityCreate,
    AvailabilityUpdate,
    AvailabilityResponse,
    CertificateCreate,
    CertificateResponse,
    ProviderBookingResponse,
    ProviderServiceCatalogResponse,
    ProviderDashboardStatsResponse,
    ProviderProfileTrustResponse,
    ProviderStatusResponse,
    ProviderResubmitRequest,
    BookingStatusUpdatePayload,
    BookingStartPayload,
    BookingRejectPayload,
    BookingCompletePayload,
    CashCollectionReportPayload,
    ProviderPaymentReportResponse,
    ProviderTicketCreateRequest,
)
from app.schemas.support import (
    SupportTicketResponse,
    TicketReplyRequest,
    TicketMessageResponse,
)

router = APIRouter(tags=["Providers & Verification"])


def get_service_domain(db: Session = Depends(get_db)) -> ProviderServiceDomain:
    return ProviderServiceDomain(db)


# ==========================================
# PROVIDER PROFILE ENDPOINTS
# ==========================================

@router.get(
    "/providers/me",
    response_model=ProviderProfileResponse,
    summary="Get current authenticated provider profile",
)
def get_my_provider_profile(
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    return service.get_my_profile(current_user)


@router.patch(
    "/providers/me",
    response_model=ProviderProfileResponse,
    summary="Update current authenticated provider profile",
)
def update_my_provider_profile(
    update_data: ProviderProfileUpdate,
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    return service.update_my_profile(current_user, update_data)


@router.get(
    "/providers/me/profile-trust",
    response_model=ProviderProfileTrustResponse,
    summary="Get verified trust signals and stats for current provider",
)
def get_my_profile_trust(
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    return service.get_profile_trust(current_user)


@router.get(
    "/providers/me/status",
    response_model=ProviderStatusResponse,
    summary="Get current provider's application verification status (accessible while Pending)",
)
def get_my_verification_status(
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    """
    Returns the provider's verification status, document breakdown, and rejection reason.
    This endpoint does NOT require is_verified=True — any authenticated provider can call it.
    Used by the Application Status page after onboarding submission.
    """
    return service.get_my_status(current_user)


@router.post(
    "/providers/me/resubmit",
    response_model=ProviderStatusResponse,
    summary="Re-submit application with updated documents after admin requested changes",
)
def resubmit_my_application(
    payload: ProviderResubmitRequest,
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    """
    Called by the provider when Admin requests document corrections or additional documents.
    Resets verification status to 'Pending' so Admin can review again.
    """
    return service.resubmit_application(current_user, payload)


@router.get(
    "/providers/{provider_id}",
    response_model=ProviderProfileResponse,
    summary="Get provider profile with strict ownership check",
)
def get_provider_profile(
    provider_id: uuid.UUID,
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    return service.get_provider_profile(current_user, provider_id)


# ==========================================
# PROVIDER SERVICES ENDPOINTS
# ==========================================

@router.get(
    "/providers/me/services",
    response_model=List[ProviderServiceCatalogResponse],
    summary="List customized services offered by current authenticated provider joined with master catalog",
)
def list_my_provider_services(
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    return service.list_my_services_catalog(current_user)


@router.post(
    "/providers/me/services",
    response_model=ProviderServiceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a service offering to current provider profile",
)
def create_provider_service_offering(
    data: ProviderServiceCreate,
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    return service.add_provider_service(current_user, data)


@router.patch(
    "/providers/me/services/{id}",
    response_model=ProviderServiceResponse,
    summary="Update customized pricing or active status of a service offering",
)
def update_provider_service_offering(
    id: uuid.UUID,
    data: ProviderServiceUpdate,
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    return service.update_provider_service(current_user, id, data)


@router.delete(
    "/providers/me/services/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a service offering from current provider profile",
)
def delete_provider_service_offering(
    id: uuid.UUID,
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    service.delete_provider_service(current_user, id)
    return None


@router.get(
    "/providers/{provider_id}/services",
    response_model=List[ProviderServiceResponse],
    summary="List customized services offered by a provider with ownership check",
)
def list_provider_services(
    provider_id: uuid.UUID,
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    return service.list_provider_services(current_user, provider_id)


# ==========================================
# AVAILABILITY SCHEDULE ENDPOINTS
# ==========================================

@router.get(
    "/providers/me/availability",
    response_model=List[AvailabilityResponse],
    summary="View active available timeslots for current provider",
)
def get_my_availability(
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    return service.list_availability(current_user, current_user.id)


@router.post(
    "/providers/me/availability",
    response_model=AvailabilityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Publish a new available timeslot",
)
def add_availability_slot(
    data: AvailabilityCreate,
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    return service.add_availability_slot(current_user, data)


@router.patch(
    "/providers/me/availability/{id}",
    response_model=AvailabilityResponse,
    summary="Update an existing timeslot (status or hours) with conflict checks",
)
def update_availability_slot(
    id: uuid.UUID,
    data: AvailabilityUpdate,
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    return service.update_availability_slot(current_user, id, data)


@router.get(
    "/providers/{provider_id}/availability",
    response_model=List[AvailabilityResponse],
    summary="View active available timeslots for a provider with ownership check",
)
def get_provider_availability(
    provider_id: uuid.UUID,
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    return service.list_availability(current_user, provider_id)


@router.delete(
    "/providers/me/availability/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an available timeslot",
)
def delete_availability_slot(
    id: uuid.UUID,
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    service.delete_availability_slot(current_user, id)
    return None


# ==========================================
# CERTIFICATES & VERIFICATION ENDPOINTS
# ==========================================

@router.post(
    "/certificates",
    response_model=CertificateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload certificate metadata for admin verification review",
)
def upload_certificate(
    data: CertificateCreate,
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    return service.upload_certificate(current_user, data)


@router.get(
    "/certificates",
    response_model=List[CertificateResponse],
    summary="List all uploaded certificates and verification statuses for current provider",
)
def list_my_certificates(
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    return service.get_my_certificates(current_user)


@router.get(
    "/certificates/{id}",
    response_model=CertificateResponse,
    summary="Get a certificate by ID with strict ownership check",
)
def get_certificate_by_id(
    id: uuid.UUID,
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    return service.get_certificate_by_id(current_user, id)


@router.delete(
    "/certificates/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a certificate with strict ownership check",
)
def delete_certificate(
    id: uuid.UUID,
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    service.delete_certificate(current_user, id)
    return None


# ==========================================
# PROVIDER BOOKINGS & ASSIGNED JOBS
# ==========================================

@router.get(
    "/providers/me/dashboard-stats",
    response_model=ProviderDashboardStatsResponse,
    summary="Get aggregated live dashboard metrics for current provider",
)
def get_my_dashboard_stats(
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    return service.get_dashboard_stats(current_user)


@router.get(
    "/providers/me/bookings",
    response_model=List[ProviderBookingResponse],
    summary="List all customer bookings assigned to current authenticated provider",
)
def get_my_assigned_bookings(
    status_filter: Optional[str] = None,
    current_user: AuthUser = Depends(require_provider),
    db: Session = Depends(get_db),
):
    from sqlalchemy.orm import joinedload
    query = (
        db.query(Booking)
        .options(
            joinedload(Booking.service),
            joinedload(Booking.customer),
        )
        .filter(Booking.provider_id == current_user.id)
    )
    if status_filter and status_filter.upper() != "ALL":
        query = query.filter(Booking.status.ilike(f"%{status_filter}%"))
    bookings = query.order_by(Booking.created_at.desc()).all()
    results = []
    for b in bookings:
        clean_bp = []
        for p in (b.before_photos or []):
            if isinstance(p, str):
                if p.startswith("/static/"):
                    clean_bp.append(f"https://smartserve-api-de3f.onrender.com{p}")
                elif p.startswith("data:image"):
                    if len(p) <= 120000:
                        clean_bp.append(p)
                    else:
                        clean_bp.append("https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=600&q=80")
                else:
                    clean_bp.append(p)
        clean_ap = []
        for p in (b.after_photos or []):
            if isinstance(p, str):
                if p.startswith("/static/"):
                    clean_ap.append(f"https://smartserve-api-de3f.onrender.com{p}")
                elif p.startswith("data:image"):
                    if len(p) <= 120000:
                        clean_ap.append(p)
                    else:
                        clean_ap.append("https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=600&q=80")
                else:
                    clean_ap.append(p)
        results.append(
            ProviderBookingResponse(
                id=b.id,
                booking_reference=b.booking_reference,
                customer_id=b.customer_id,
                customer_name=b.customer.full_name if b.customer else "Customer",
                customer_phone=b.customer.phone if b.customer else None,
                service_id=b.service_id,
                service_name=b.get_service_name() if hasattr(b, "get_service_name") else (b.service_name or "Home Service"),
                category=b.get_category() if hasattr(b, "get_category") else (b.category or "General"),
                status=str(b.status.value if hasattr(b.status, "value") else b.status),
                payment_status=str(b.payment_status or "Pending"),
                scheduled_time=b.scheduled_time,
                scheduled_date=b.scheduled_date,
                address=b.address or "",
                total_price=Decimal(str(b.total_price or "0.00")),
                otp_code=None,
                emergency_flag=b.emergency_flag,
                customer_notes=b.customer_notes or b.notes,
                before_photos=clean_bp,
                after_photos=clean_ap,
                timeline=b.timeline,
                created_at=b.created_at,
            )
        )
    return results


@router.get(
    "/providers/me/bookings/{booking_id}",
    response_model=ProviderBookingResponse,
    summary="Get single assigned booking by ID with ownership check",
)
def get_my_assigned_booking_detail(
    booking_id: uuid.UUID,
    current_user: AuthUser = Depends(require_provider),
    db: Session = Depends(get_db),
):
    b = db.query(Booking).filter(Booking.id == booking_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Booking not found")
    if b.provider_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You cannot access bookings assigned to another provider",
        )
    return ProviderBookingResponse(
        id=b.id,
        booking_reference=b.booking_reference,
        customer_id=b.customer_id,
        customer_name=b.customer.full_name if b.customer else "Customer",
        customer_phone=b.customer.phone if b.customer else None,
        service_id=b.service_id,
        service_name=b.get_service_name() if hasattr(b, "get_service_name") else (b.service_name or "Home Service"),
        category=b.get_category() if hasattr(b, "get_category") else (b.category or "General"),
        status=str(b.status.value if hasattr(b.status, "value") else b.status),
        payment_status=str(b.payment_status or "Pending"),
        scheduled_time=b.scheduled_time,
        scheduled_date=b.scheduled_date,
        address=b.address or "",
        total_price=Decimal(str(b.total_price or "0.00")),
        otp_code=None,
        emergency_flag=b.emergency_flag,
        timeline=b.timeline,
        created_at=b.created_at,
    )


def _serialize_booking_response(b: Booking) -> ProviderBookingResponse:
    return ProviderBookingResponse(
        id=b.id,
        booking_reference=b.booking_reference,
        customer_id=b.customer_id,
        customer_name=b.customer.full_name if b.customer else "Customer",
        customer_phone=b.customer.phone if b.customer else None,
        service_id=b.service_id,
        service_name=b.get_service_name() if hasattr(b, "get_service_name") else (b.service_name or "Home Service"),
        category=b.get_category() if hasattr(b, "get_category") else (b.category or "General"),
        status=str(b.status.value if hasattr(b.status, "value") else b.status),
        payment_status=str(b.payment_status or "Pending"),
        scheduled_time=b.scheduled_time,
        scheduled_date=b.scheduled_date,
        address=b.address or "",
        total_price=Decimal(str(b.total_price or "0.00")),
        otp_code=None,
        emergency_flag=b.emergency_flag,
        customer_notes=b.customer_notes or b.notes,
        before_photos=b.before_photos or [],
        after_photos=b.after_photos or [],
        timeline=b.timeline,
        created_at=b.created_at,
    )


@router.post(
    "/providers/me/bookings/{booking_id}/accept",
    response_model=ProviderBookingResponse,
    summary="Accept an incoming requested booking",
)
def accept_booking(
    booking_id: uuid.UUID,
    current_user: AuthUser = Depends(require_provider),
    db: Session = Depends(get_db),
):
    from app.core.websockets import broadcast_realtime

    updated = transition_booking_status(
        db=db,
        booking_id=booking_id,
        next_status="Accepted",
        user=current_user,
    )

    cust_id = str(updated.customer_id) if updated.customer_id else None
    cust_user_id = str(updated.customer.user_id) if updated.customer and hasattr(updated.customer, 'user_id') else None

    # Direct realtime WebSocket broadcast (independent of Kafka)
    channels = ["dashboard", "bookings", "admin", f"booking_{updated.id}", f"admin_booking_{updated.id}"]
    if cust_id:
        channels.extend([f"customer_{cust_id}", f"user_{cust_id}"])
    if cust_user_id:
        channels.extend([f"customer_{cust_user_id}", f"user_{cust_user_id}"])
    channels.extend([f"provider_{current_user.id}", f"user_{current_user.id}"])

    accepted_msg = {
        "type": "BOOKING_ACCEPTED",
        "event": "booking.accepted",
        "event_type": "booking.accepted",
        "booking_id": str(updated.id),
        "status": "Accepted",
        "booking": {
            "id": str(updated.id),
            "booking_reference": updated.booking_reference,
            "customer_id": cust_id,
            "customer_user_id": cust_user_id,
            "customer_name": updated.customer.full_name if updated.customer else "Customer",
            "provider_id": str(current_user.id),
            "provider_name": current_user.full_name,
            "service_name": updated.service_name,
            "status": "Accepted",
            "total_price": float(updated.total_price or 0.0),
            "scheduled_date": updated.scheduled_date,
            "scheduled_time": updated.scheduled_time.strftime("%H:%M:%S") if hasattr(updated.scheduled_time, "strftime") else str(updated.scheduled_time),
        },
        "data": {
            "id": str(updated.id),
            "status": "Accepted",
        }
    }
    broadcast_realtime(channels, accepted_msg)

    # Optional background Kafka notification if available
    try:
        from app.services.kafka import kafka_producer, KafkaTopics, KafkaEvent
        accepted_event = KafkaEvent(
            event_type=KafkaTopics.BOOKING_ACCEPTED,
            booking_id=str(updated.id),
            sender_id=str(current_user.id),
            receiver_id=cust_id,
            payload=accepted_msg["booking"]
        )
        kafka_producer.publish_event(KafkaTopics.BOOKING_ACCEPTED, accepted_event)
    except Exception:
        pass

    return _serialize_booking_response(updated)


@router.post(
    "/providers/me/bookings/{booking_id}/reject",
    response_model=ProviderBookingResponse,
    summary="Reject an incoming requested booking with optional reason",
)
def reject_booking(
    booking_id: uuid.UUID,
    payload: Optional[BookingRejectPayload] = None,
    current_user: AuthUser = Depends(require_provider),
    db: Session = Depends(get_db),
):
    from app.core.websockets import broadcast_realtime

    if not payload or not payload.reason or not payload.reason.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rejection reason is required when declining a booking request.",
        )
    reason = payload.reason.strip()
    updated = transition_booking_status(
        db=db,
        booking_id=booking_id,
        next_status="Rejected",
        user=current_user,
        reason=reason,
    )

    cust_id = str(updated.customer_id) if updated.customer_id else None
    cust_user_id = str(updated.customer.user_id) if updated.customer and hasattr(updated.customer, 'user_id') else None

    # Direct realtime WebSocket broadcast (independent of Kafka)
    channels = ["dashboard", "bookings", "admin", f"booking_{updated.id}", f"admin_booking_{updated.id}"]
    if cust_id:
        channels.extend([f"customer_{cust_id}", f"user_{cust_id}"])
    if cust_user_id:
        channels.extend([f"customer_{cust_user_id}", f"user_{cust_user_id}"])
    channels.extend([f"provider_{current_user.id}", f"user_{current_user.id}"])

    rejected_msg = {
        "type": "BOOKING_REJECTED",
        "event": "booking.rejected",
        "event_type": "booking.rejected",
        "booking_id": str(updated.id),
        "status": "Rejected",
        "reason": reason,
        "rejection_reason": reason,
        "cancellation_reason": reason,
        "booking": {
            "id": str(updated.id),
            "booking_reference": updated.booking_reference,
            "customer_id": cust_id,
            "customer_user_id": cust_user_id,
            "customer_name": updated.customer.full_name if updated.customer else "Customer",
            "provider_id": str(current_user.id),
            "provider_name": current_user.full_name,
            "service_name": updated.service_name,
            "status": "Rejected",
            "reason": reason,
            "rejection_reason": reason,
            "cancellation_reason": reason,
            "total_price": float(updated.total_price or 0.0),
            "scheduled_date": updated.scheduled_date,
        },
        "data": {
            "id": str(updated.id),
            "status": "Rejected",
            "reason": reason,
        }
    }
    broadcast_realtime(channels, rejected_msg)

    try:
        from app.services.kafka import kafka_producer, KafkaTopics, KafkaEvent
        rejected_event = KafkaEvent(
            event_type=KafkaTopics.BOOKING_REJECTED,
            booking_id=str(updated.id),
            sender_id=str(current_user.id),
            receiver_id=cust_id,
            payload=rejected_msg["booking"]
        )
        kafka_producer.publish_event(KafkaTopics.BOOKING_REJECTED, rejected_event)
    except Exception:
        pass

    return _serialize_booking_response(updated)


@router.post(
    "/providers/me/bookings/{booking_id}/start",
    response_model=ProviderBookingResponse,
    summary="Mark an arrived booking as Started with verified customer 4-digit start OTP",
)
def start_booking(
    booking_id: uuid.UUID,
    payload: Optional[BookingStartPayload] = None,
    current_user: AuthUser = Depends(require_provider),
    db: Session = Depends(get_db),
):
    from app.core.websockets import broadcast_realtime

    otp = payload.otp_code.strip() if (payload and payload.otp_code) else None
    updated = transition_booking_status(
        db=db,
        booking_id=booking_id,
        next_status="Started",
        user=current_user,
        otp_code=otp,
    )

    cust_id = str(updated.customer_id) if updated.customer_id else None
    cust_user_id = str(updated.customer.user_id) if updated.customer and hasattr(updated.customer, 'user_id') else None

    # Direct realtime WebSocket broadcast (Phase 1: No Kafka required)
    channels = ["dashboard", "bookings", "admin", f"booking_{updated.id}", f"admin_booking_{updated.id}"]
    if cust_id:
        channels.extend([f"customer_{cust_id}", f"user_{cust_id}"])
    if cust_user_id:
        channels.extend([f"customer_{cust_user_id}", f"user_{cust_user_id}"])
    channels.extend([f"provider_{current_user.id}", f"user_{current_user.id}"])

    started_msg = {
        "type": "BOOKING_STARTED",
        "event": "booking.started",
        "event_type": "booking.started",
        "booking_id": str(updated.id),
        "status": "Started",
        "booking": {
            "id": str(updated.id),
            "booking_reference": updated.booking_reference,
            "customer_id": cust_id,
            "customer_name": updated.customer.full_name if updated.customer else "Customer",
            "provider_id": str(current_user.id),
            "provider_name": current_user.full_name,
            "service_name": updated.service_name,
            "status": "Started",
            "total_price": float(updated.total_price or 0.0),
        },
        "data": {
            "id": str(updated.id),
            "status": "Started",
        }
    }
    broadcast_realtime(channels, started_msg)

    return _serialize_booking_response(updated)


@router.post(
    "/providers/me/bookings/{booking_id}/complete",
    response_model=ProviderBookingResponse,
    summary="Complete a job in progress with verified customer 4-digit completion OTP",
)
def complete_booking(
    booking_id: uuid.UUID,
    payload: Optional[BookingCompletePayload] = None,
    current_user: AuthUser = Depends(require_provider),
    db: Session = Depends(get_db),
):
    from app.core.websockets import broadcast_realtime
    from app.models.provider import ProviderLocation

    reason = payload.notes if payload else None
    otp = payload.otp_code.strip() if (payload and payload.otp_code) else None
    updated = transition_booking_status(
        db=db,
        booking_id=booking_id,
        next_status="Completed",
        user=current_user,
        reason=reason,
        otp_code=otp,
    )

    # Stop active location tracking in PostgreSQL
    try:
        loc = db.query(ProviderLocation).filter(ProviderLocation.provider_id == current_user.id).first()
        if loc:
            loc.is_active = False
            db.add(loc)
            db.commit()
    except Exception:
        pass

    cust_id = str(updated.customer_id) if updated.customer_id else None
    cust_user_id = str(updated.customer.user_id) if updated.customer and hasattr(updated.customer, 'user_id') else None

    # Direct realtime WebSocket broadcast
    channels = ["dashboard", "bookings", "admin", f"booking_{updated.id}", f"admin_booking_{updated.id}"]
    if cust_id:
        channels.extend([f"customer_{cust_id}", f"user_{cust_id}"])
    if cust_user_id:
        channels.extend([f"customer_{cust_user_id}", f"user_{cust_user_id}"])
    channels.extend([f"provider_{current_user.id}", f"user_{current_user.id}"])

    completed_msg = {
        "type": "BOOKING_COMPLETED",
        "event": "booking.completed",
        "event_type": "booking.completed",
        "booking_id": str(updated.id),
        "status": "Completed",
        "booking": {
            "id": str(updated.id),
            "booking_reference": updated.booking_reference,
            "customer_id": cust_id,
            "customer_name": updated.customer.full_name if updated.customer else "Customer",
            "provider_id": str(current_user.id),
            "provider_name": current_user.full_name,
            "service_name": updated.service_name,
            "status": "Completed",
            "total_price": float(updated.total_price or 0.0),
        },
        "data": {
            "id": str(updated.id),
            "status": "Completed",
        }
    }
    broadcast_realtime(channels, completed_msg)

    return _serialize_booking_response(updated)


@router.post(
    "/providers/me/bookings/{booking_id}/cash-collected",
    response_model=ProviderPaymentReportResponse,
    summary="Report Cash on Delivery collection from customer",
)
def report_cash_collected(
    booking_id: uuid.UUID,
    payload: CashCollectionReportPayload,
    current_user: AuthUser = Depends(require_provider),
    db: Session = Depends(get_db),
):
    from datetime import datetime, timezone
    from app.core.websockets import broadcast_realtime
    from app.models.payment import BookingPayment

    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Only assigned provider may report collection
    if booking.provider_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You can only report cash collection for your assigned bookings.",
        )

    # Booking must be started or completed
    curr_st = str(booking.status.value if hasattr(booking.status, "value") else booking.status).lower()
    if curr_st not in ["started", "completed", "arrived"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot report cash collection when booking is in '{booking.status}' status. Service must be started or completed.",
        )

    # Prevent duplicate collection reports
    curr_pay_st = str(booking.payment_status or "Pending").strip().lower()
    if curr_pay_st in ["collection reported", "paid", "collection_reported"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cash collection has already been reported or verified for this booking. Duplicate reports are not permitted.",
        )

    agreed_amount = Decimal(str(booking.total_price or "0.00"))
    reported_amount = Decimal(str(payload.reported_amount))
    discrepancy_amount = abs(reported_amount - agreed_amount)
    has_discrepancy = (reported_amount != agreed_amount)

    now_utc = datetime.now(timezone.utc)

    # Check for existing BookingPayment record
    payment = db.query(BookingPayment).filter(BookingPayment.booking_id == booking.id).first()
    if not payment:
        payment = BookingPayment(
            id=uuid.uuid4(),
            booking_id=booking.id,
            customer_id=booking.customer_id,
            provider_id=current_user.id,
            payment_method="COD",
            agreed_amount=agreed_amount,
            created_at=now_utc,
        )

    payment.reported_amount = reported_amount
    payment.status = "Collection Reported"
    payment.discrepancy_flag = has_discrepancy
    payment.discrepancy_amount = discrepancy_amount
    payment.collected_at = now_utc
    payment.collection_notes = payload.notes
    payment.updated_at = now_utc
    db.add(payment)

    booking.payment_status = "Collection Reported"
    booking.payment_method = "COD"

    # Add audit event to booking timeline
    tl_event = {
        "event": "Provider Reported Cash Collection",
        "actor": current_user.full_name or current_user.email,
        "role": "provider",
        "reported_amount": float(reported_amount),
        "agreed_amount": float(agreed_amount),
        "discrepancy_flag": has_discrepancy,
        "discrepancy_amount": float(discrepancy_amount),
        "notes": payload.notes or "",
        "timestamp": now_utc.isoformat(),
    }
    cur_tl = list(booking.timeline or [])
    cur_tl.append(tl_event)
    booking.timeline = cur_tl

    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(booking, "timeline")

    db.commit()
    db.refresh(payment)
    db.refresh(booking)

    # Automated Notification Trigger: Payment Collection Reported
    try:
        from app.services.notification import notify_booking_event
        notify_booking_event(
            db,
            booking,
            "payment.collection_reported",
            extra_context={
                "payment_id": str(payment.id),
                "notes": payload.notes,
            },
        )
    except Exception as exc:
        pass

    # Broadcast notification across channels
    cust_id = str(booking.customer_id) if booking.customer_id else None
    channels = ["dashboard", "bookings", "admin", f"booking_{booking.id}", f"admin_booking_{booking.id}"]
    if cust_id:
        channels.extend([f"customer_{cust_id}", f"user_{cust_id}"])
    channels.extend([f"provider_{current_user.id}", f"user_{current_user.id}"])

    msg = {
        "type": "PAYMENT_COLLECTION_REPORTED",
        "event": "payment.collection_reported",
        "event_type": "payment.collection_reported",
        "booking_id": str(booking.id),
        "payment_id": str(payment.id),
        "payment_status": "Collection Reported",
        "agreed_amount": float(agreed_amount),
        "reported_amount": float(reported_amount),
        "discrepancy_flag": has_discrepancy,
        "discrepancy_amount": float(discrepancy_amount),
        "timestamp": now_utc.isoformat(),
    }
    broadcast_realtime(channels, msg)

    discrepancy_msg = f" Discrepancy of ₹{abs(float(discrepancy_amount)):.2f} flagged for admin review." if has_discrepancy else ""
    return ProviderPaymentReportResponse(
        payment_id=str(payment.id),
        booking_id=str(booking.id),
        booking_reference=booking.booking_reference,
        agreed_amount=float(agreed_amount),
        reported_amount=float(reported_amount),
        status="Collection Reported",
        discrepancy_flag=has_discrepancy,
        discrepancy_amount=float(discrepancy_amount),
        collected_at=now_utc.isoformat(),
        message=f"Cash collection of ₹{float(reported_amount):.2f} recorded.{discrepancy_msg} Awaiting admin verification.",
    )



@router.post(
    "/providers/me/bookings/{booking_id}/on-the-way",
    response_model=ProviderBookingResponse,
    summary="Mark provider on the way to customer location",
)
def mark_booking_on_the_way(
    booking_id: uuid.UUID,
    current_user: AuthUser = Depends(require_provider),
    db: Session = Depends(get_db),
):
    from app.core.websockets import broadcast_realtime

    updated = transition_booking_status(
        db=db,
        booking_id=booking_id,
        next_status="On The Way",
        user=current_user,
    )

    cust_id = str(updated.customer_id) if updated.customer_id else None
    cust_user_id = str(updated.customer.user_id) if updated.customer and hasattr(updated.customer, 'user_id') else None

    channels = ["dashboard", "bookings", "admin", f"booking_{updated.id}", f"admin_booking_{updated.id}"]
    if cust_id:
        channels.extend([f"customer_{cust_id}", f"user_{cust_id}"])
    if cust_user_id:
        channels.extend([f"customer_{cust_user_id}", f"user_{cust_user_id}"])
    channels.extend([f"provider_{current_user.id}", f"user_{current_user.id}"])

    status_msg = {
        "type": "BOOKING_STATUS_UPDATED",
        "event": "booking.updated",
        "event_type": "booking.updated",
        "booking_id": str(updated.id),
        "status": "On The Way",
        "otp_code": updated.otp_code,
        "booking": {
            "id": str(updated.id),
            "booking_reference": updated.booking_reference,
            "customer_id": cust_id,
            "provider_id": str(current_user.id),
            "status": "On The Way",
            "otp_code": updated.otp_code,
        },
        "data": {
            "id": str(updated.id),
            "status": "On The Way",
            "otp_code": updated.otp_code,
        }
    }
    broadcast_realtime(channels, status_msg)
    return _serialize_booking_response(updated)


@router.post(
    "/providers/me/bookings/{booking_id}/start-trip",
    response_model=ProviderBookingResponse,
    summary="Alias for on-the-way: start provider trip to customer location",
)
def start_booking_trip(
    booking_id: uuid.UUID,
    current_user: AuthUser = Depends(require_provider),
    db: Session = Depends(get_db),
):
    return mark_booking_on_the_way(booking_id=booking_id, current_user=current_user, db=db)


@router.post(
    "/providers/me/bookings/{booking_id}/arrived",
    response_model=ProviderBookingResponse,
    summary="Mark provider arrived at customer location",
)
def mark_booking_arrived(
    booking_id: uuid.UUID,
    current_user: AuthUser = Depends(require_provider),
    db: Session = Depends(get_db),
):
    from app.core.websockets import broadcast_realtime

    updated = transition_booking_status(
        db=db,
        booking_id=booking_id,
        next_status="Arrived",
        user=current_user,
    )

    cust_id = str(updated.customer_id) if updated.customer_id else None
    cust_user_id = str(updated.customer.user_id) if updated.customer and hasattr(updated.customer, 'user_id') else None

    channels = ["dashboard", "bookings", "admin", f"booking_{updated.id}", f"admin_booking_{updated.id}"]
    if cust_id:
        channels.extend([f"customer_{cust_id}", f"user_{cust_id}"])
    if cust_user_id:
        channels.extend([f"customer_{cust_user_id}", f"user_{cust_user_id}"])
    channels.extend([f"provider_{current_user.id}", f"user_{current_user.id}"])

    status_msg = {
        "type": "BOOKING_STATUS_UPDATED",
        "event": "booking.updated",
        "event_type": "booking.updated",
        "booking_id": str(updated.id),
        "status": "Arrived",
        "otp_code": updated.otp_code,
        "booking": {
            "id": str(updated.id),
            "booking_reference": updated.booking_reference,
            "customer_id": cust_id,
            "provider_id": str(current_user.id),
            "status": "Arrived",
            "otp_code": updated.otp_code,
        },
        "data": {
            "id": str(updated.id),
            "status": "Arrived",
            "otp_code": updated.otp_code,
        }
    }
    broadcast_realtime(channels, status_msg)
    return _serialize_booking_response(updated)


@router.patch(
    "/providers/me/bookings/{booking_id}/status",
    response_model=ProviderBookingResponse,
    summary="Generic state machine transition endpoint for provider booking",
)
def update_booking_status(
    booking_id: uuid.UUID,
    payload: BookingStatusUpdatePayload,
    current_user: AuthUser = Depends(require_provider),
    db: Session = Depends(get_db),
):
    from app.core.websockets import broadcast_realtime

    target_st = payload.target_status
    if not target_st:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status field is required for transition."
        )

    updated = transition_booking_status(
        db=db,
        booking_id=booking_id,
        next_status=target_st,
        user=current_user,
        reason=payload.reason,
        otp_code=payload.otp_code,
    )

    cust_id = str(updated.customer_id) if updated.customer_id else None
    cust_user_id = str(updated.customer.user_id) if updated.customer and hasattr(updated.customer, 'user_id') else None

    # Direct realtime WebSocket broadcast (Phase 1: No Kafka required)
    channels = ["dashboard", "bookings", "admin", f"booking_{updated.id}", f"admin_booking_{updated.id}"]
    if cust_id:
        channels.extend([f"customer_{cust_id}", f"user_{cust_id}"])
    if cust_user_id:
        channels.extend([f"customer_{cust_user_id}", f"user_{cust_user_id}"])
    channels.extend([f"provider_{current_user.id}", f"user_{current_user.id}"])

    status_msg = {
        "type": "BOOKING_STATUS_UPDATED",
        "event": "booking.updated",
        "event_type": "booking.updated",
        "booking_id": str(updated.id),
        "status": updated.status,
        "otp_code": updated.otp_code,
        "booking": {
            "id": str(updated.id),
            "booking_reference": updated.booking_reference,
            "customer_id": cust_id,
            "provider_id": str(current_user.id),
            "status": updated.status,
            "otp_code": updated.otp_code,
        },
        "data": {
            "id": str(updated.id),
            "status": updated.status,
            "otp_code": updated.otp_code,
        }
    }
    broadcast_realtime(channels, status_msg)

    return _serialize_booking_response(updated)


@router.post(
    "/providers/me/bookings/{booking_id}/photos/before",
    summary="Upload before-service proof photo",
)
async def upload_before_service_photo(
    booking_id: uuid.UUID,
    request: Request,
    current_user: AuthUser = Depends(require_provider),
    db: Session = Depends(get_db),
):
    import os
    from datetime import datetime
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if not booking.provider_id or str(booking.provider_id) != str(current_user.id):
        booking.provider_id = current_user.id

    url = None
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        body = await request.json()
        url = body.get("photo_url")
    else:
        form = await request.form()
        file = form.get("file")
        if file and hasattr(file, "read"):
            os.makedirs("customer_uploads", exist_ok=True)
            fname = getattr(file, "filename", "photo.jpg")
            filename = f"before_{uuid.uuid4().hex[:8]}_{fname}"
            filepath = os.path.join("customer_uploads", filename)
            content = await file.read()
            with open(filepath, "wb") as f:
                f.write(content)
            url = f"https://smartserve-api-de3f.onrender.com/static/uploads/{filename}"

    if not url:
        raise HTTPException(status_code=400, detail="No photo file or photo_url provided")

    if url and url.startswith("data:image"):
        if len(url) <= 120000:
            pass
        else:
            try:
                import base64
                os.makedirs("customer_uploads", exist_ok=True)
                header, encoded = url.split(",", 1) if "," in url else ("", url)
                ext = "png" if "png" in header else "jpg"
                filename = f"before_{uuid.uuid4().hex[:8]}.{ext}"
                filepath = os.path.join("customer_uploads", filename)
                with open(filepath, "wb") as f:
                    f.write(base64.b64decode(encoded))
                url = f"https://smartserve-api-de3f.onrender.com/static/uploads/{filename}"
            except Exception:
                url = "https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=600&q=80"

    current_photos = list(booking.before_photos or [])
    if url not in current_photos:
        current_photos.append(url)
    booking.before_photos = current_photos

    timeline_photo = url if not url.startswith("data:image") or len(url) < 300 else url[:100]
    cur_tl = list(booking.timeline or [])
    cur_tl.append({
        "event": "Before-Service Photo Uploaded",
        "actor": current_user.full_name or "Provider",
        "role": "provider",
        "photo_url": timeline_photo,
        "timestamp": datetime.utcnow().isoformat(),
    })
    booking.timeline = cur_tl

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return {
        "success": True,
        "photo_url": url,
        "before_photos": booking.before_photos,
    }


@router.post(
    "/providers/me/bookings/{booking_id}/photos/after",
    summary="Upload after-service proof photo",
)
async def upload_after_service_photo(
    booking_id: uuid.UUID,
    request: Request,
    current_user: AuthUser = Depends(require_provider),
    db: Session = Depends(get_db),
):
    import os
    from datetime import datetime
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if not booking.provider_id or str(booking.provider_id) != str(current_user.id):
        booking.provider_id = current_user.id

    url = None
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        body = await request.json()
        url = body.get("photo_url")
    else:
        form = await request.form()
        file = form.get("file")
        if file and hasattr(file, "read"):
            os.makedirs("customer_uploads", exist_ok=True)
            fname = getattr(file, "filename", "photo.jpg")
            filename = f"after_{uuid.uuid4().hex[:8]}_{fname}"
            filepath = os.path.join("customer_uploads", filename)
            content = await file.read()
            with open(filepath, "wb") as f:
                f.write(content)
            url = f"https://smartserve-api-de3f.onrender.com/static/uploads/{filename}"

    if not url:
        raise HTTPException(status_code=400, detail="No photo file or photo_url provided")

    if url and url.startswith("data:image"):
        if len(url) <= 120000:
            pass
        else:
            try:
                import base64
                os.makedirs("customer_uploads", exist_ok=True)
                header, encoded = url.split(",", 1) if "," in url else ("", url)
                ext = "png" if "png" in header else "jpg"
                filename = f"after_{uuid.uuid4().hex[:8]}.{ext}"
                filepath = os.path.join("customer_uploads", filename)
                with open(filepath, "wb") as f:
                    f.write(base64.b64decode(encoded))
                url = f"https://smartserve-api-de3f.onrender.com/static/uploads/{filename}"
            except Exception:
                url = "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=600&q=80"

    current_photos = list(booking.after_photos or [])
    if url not in current_photos:
        current_photos.append(url)
    booking.after_photos = current_photos

    timeline_photo = url if not url.startswith("data:image") or len(url) < 300 else url[:100]
    cur_tl = list(booking.timeline or [])
    cur_tl.append({
        "event": "After-Service Photo Uploaded",
        "actor": current_user.full_name or "Provider",
        "role": "provider",
        "photo_url": timeline_photo,
        "timestamp": datetime.utcnow().isoformat(),
    })
    booking.timeline = cur_tl

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return {
        "success": True,
        "photo_url": url,
        "after_photos": booking.after_photos,
    }


@router.get(
    "/providers/me/bookings/{booking_id}/photos",
    summary="Get before and after service photos for a booking",
)
def get_service_photos(
    booking_id: uuid.UUID,
    current_user: AuthUser = Depends(require_provider),
    db: Session = Depends(get_db),
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.provider_id == current_user.id
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found or not assigned to you")

    return {
        "booking_id": str(booking.id),
        "before_photos": booking.before_photos or [],
        "after_photos": booking.after_photos or [],
    }



from pydantic import BaseModel

class ProviderLocationPayload(BaseModel):
    booking_id: uuid.UUID
    latitude: float
    longitude: float
    heading: Optional[float] = None
    speed: Optional[float] = None
    accuracy: Optional[float] = None
    timestamp: Optional[str] = None


@router.post(
    "/providers/me/location",
    summary="Update real-time GPS location of provider for active booking",
)
def update_provider_location(
    payload: ProviderLocationPayload,
    current_user: AuthUser = Depends(require_provider),
    db: Session = Depends(get_db),
):
    from datetime import datetime
    from app.models.provider import Provider, ProviderLocation
    from app.core.websockets import broadcast_realtime

    # 1. Coordinate Validity Check
    if not (-90.0 <= payload.latitude <= 90.0 and -180.0 <= payload.longitude <= 180.0):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid GPS coordinates: latitude must be in [-90, 90] and longitude in [-180, 180].",
        )

    # 2. Safety Check: Verify provider is verified
    provider = db.query(Provider).filter(Provider.user_id == current_user.id).first()
    if not provider or not provider.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only approved, verified service providers can broadcast live GPS location.",
        )

    # 3. Safety Check: Verify active booking ownership and state
    booking = db.query(Booking).filter(
        Booking.id == payload.booking_id,
        Booking.provider_id == current_user.id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active booking not found for this provider.",
        )

    active_statuses = ["Accepted", "On The Way", "Arrived", "Started"]
    if booking.status not in active_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Live location updates are only permitted during an active job. Current status: '{booking.status}'",
        )

    # 4. Upsert latest location record in PostgreSQL
    loc = db.query(ProviderLocation).filter(ProviderLocation.provider_id == current_user.id).first()
    now_utc = datetime.utcnow()
    if not loc:
        loc = ProviderLocation(
            id=uuid.uuid4(),
            provider_id=current_user.id,
            booking_id=payload.booking_id,
            latitude=Decimal(str(payload.latitude)),
            longitude=Decimal(str(payload.longitude)),
            heading=Decimal(str(payload.heading)) if payload.heading is not None else None,
            speed=Decimal(str(payload.speed)) if payload.speed is not None else None,
            accuracy=Decimal(str(payload.accuracy)) if payload.accuracy is not None else None,
            is_active=True,
            updated_at=now_utc,
        )
        db.add(loc)
    else:
        loc.booking_id = payload.booking_id
        loc.latitude = Decimal(str(payload.latitude))
        loc.longitude = Decimal(str(payload.longitude))
        if payload.heading is not None:
            loc.heading = Decimal(str(payload.heading))
        if payload.speed is not None:
            loc.speed = Decimal(str(payload.speed))
        if payload.accuracy is not None:
            loc.accuracy = Decimal(str(payload.accuracy))
        loc.is_active = True
        loc.updated_at = now_utc
        db.add(loc)

    db.commit()

    # 5. Direct WebSocket broadcast to customer, admin, and active booking channels
    cust_id = str(booking.customer_id) if booking.customer_id else None
    channels = ["dashboard", "bookings", "admin", f"booking_{booking.id}", f"admin_booking_{booking.id}"]
    if cust_id:
        channels.extend([f"customer_{cust_id}", f"user_{cust_id}"])
    if booking.customer and hasattr(booking.customer, "user_id") and booking.customer.user_id:
        channels.extend([f"customer_{booking.customer.user_id}", f"user_{booking.customer.user_id}"])

    loc_msg = {
        "type": "PROVIDER_LOCATION_UPDATED",
        "event": "provider.location.updated",
        "event_type": "provider.location.updated",
        "booking_id": str(booking.id),
        "provider_id": str(current_user.id),
        "provider_name": provider.full_name,
        "latitude": float(payload.latitude),
        "longitude": float(payload.longitude),
        "heading": float(payload.heading) if payload.heading is not None else None,
        "speed": float(payload.speed) if payload.speed is not None else None,
        "accuracy": float(payload.accuracy) if payload.accuracy is not None else None,
        "status": booking.status,
        "updated_at": f"{now_utc.isoformat()}Z",
    }
    broadcast_realtime(channels, loc_msg)

    return {
        "status": "success",
        "booking_id": str(booking.id),
        "latitude": float(payload.latitude),
        "longitude": float(payload.longitude),
        "updated_at": f"{now_utc.isoformat()}Z",
    }


@router.post(
    "/providers/dev-simulate-location",
    summary="[DEV ONLY] Update real-time GPS location of provider along OSRM route for testing",
)
def dev_simulate_provider_location(
    payload: ProviderLocationPayload,
    db: Session = Depends(get_db),
):
    from datetime import datetime
    from app.models.provider import Provider, ProviderLocation
    from app.core.websockets import broadcast_realtime
    from app.core.config import settings

    if settings.ENVIRONMENT == "production":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="DEV GPS simulation endpoint is disabled in production.",
        )

    if not (-90.0 <= payload.latitude <= 90.0 and -180.0 <= payload.longitude <= 180.0):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid GPS coordinates.",
        )

    booking = db.query(Booking).filter(Booking.id == payload.booking_id).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found.")

    provider_id = booking.provider_id
    provider = db.query(Provider).filter(Provider.user_id == provider_id).first() if provider_id else None

    now_utc = datetime.utcnow()
    loc = db.query(ProviderLocation).filter(ProviderLocation.booking_id == payload.booking_id).first()
    if not loc and provider_id:
        loc = db.query(ProviderLocation).filter(ProviderLocation.provider_id == provider_id).first()

    if not loc:
        loc = ProviderLocation(
            id=uuid.uuid4(),
            provider_id=provider_id or uuid.uuid4(),
            booking_id=payload.booking_id,
            latitude=Decimal(str(payload.latitude)),
            longitude=Decimal(str(payload.longitude)),
            heading=Decimal(str(payload.heading)) if payload.heading is not None else None,
            speed=Decimal(str(payload.speed)) if payload.speed is not None else None,
            accuracy=Decimal(str(payload.accuracy)) if payload.accuracy is not None else Decimal("5.0"),
            is_active=True,
            updated_at=now_utc,
        )
        db.add(loc)
    else:
        loc.booking_id = payload.booking_id
        loc.latitude = Decimal(str(payload.latitude))
        loc.longitude = Decimal(str(payload.longitude))
        if payload.heading is not None:
            loc.heading = Decimal(str(payload.heading))
        if payload.speed is not None:
            loc.speed = Decimal(str(payload.speed))
        if payload.accuracy is not None:
            loc.accuracy = Decimal(str(payload.accuracy))
        loc.is_active = True
        loc.updated_at = now_utc
        db.add(loc)

    db.commit()

    cust_id = str(booking.customer_id) if booking.customer_id else None
    channels = ["dashboard", "bookings", "admin", f"booking_{booking.id}", f"admin_booking_{booking.id}"]
    if cust_id:
        channels.extend([f"customer_{cust_id}", f"user_{cust_id}"])
    if booking.customer and hasattr(booking.customer, "user_id") and booking.customer.user_id:
        channels.extend([f"customer_{booking.customer.user_id}", f"user_{booking.customer.user_id}"])

    loc_msg = {
        "type": "PROVIDER_LOCATION_UPDATED",
        "event": "provider.location.updated",
        "event_type": "provider.location.updated",
        "booking_id": str(booking.id),
        "provider_id": str(provider_id) if provider_id else "",
        "provider_name": provider.full_name if provider else (booking.provider_name or "Service Partner"),
        "latitude": float(payload.latitude),
        "longitude": float(payload.longitude),
        "heading": float(payload.heading) if payload.heading is not None else None,
        "speed": float(payload.speed) if payload.speed is not None else None,
        "accuracy": float(payload.accuracy) if payload.accuracy is not None else 5.0,
        "status": booking.status,
        "updated_at": f"{now_utc.isoformat()}Z",
    }
    broadcast_realtime(channels, loc_msg)

    return {
        "status": "success",
        "booking_id": str(booking.id),
        "latitude": float(payload.latitude),
        "longitude": float(payload.longitude),
        "updated_at": f"{now_utc.isoformat()}Z",
    }


# ==========================================
# SUPPORT TICKETS
# ==========================================

def _serialize_ticket_response(t) -> SupportTicketResponse:
    from app.schemas.support import TicketMessageResponse
    msgs = [
        TicketMessageResponse(
            id=str(m.id),
            sender_id=str(m.sender_id),
            sender_role=m.sender_role,
            sender_name=getattr(m, "sender_name", None) or (m.sender_role.title() if m.sender_role else "User"),
            message_text=m.message_text,
            attachment_url=m.attachment_url,
            created_at=m.created_at.isoformat() if m.created_at else ""
        ) for m in getattr(t, "messages", [])
    ]
    msgs.sort(key=lambda m: m.created_at)
    
    # Resolve accurate customer name
    c_name = "Customer"
    if getattr(t, "customer", None) and getattr(t.customer, "full_name", None):
        c_name = t.customer.full_name
    elif not getattr(t, "customer_id", None) and getattr(t, "provider_id", None):
        c_name = "Provider"

    return SupportTicketResponse(
        id=str(t.id),
        customer_id=str(t.customer_id) if getattr(t, "customer_id", None) else None,
        provider_id=str(t.provider_id) if getattr(t, "provider_id", None) else None,
        customer_name=c_name,
        subject=t.subject,
        description=t.description,
        category=getattr(t, "category", None),
        priority=t.priority.value if hasattr(t.priority, "value") else str(t.priority),
        status=t.status.value if hasattr(t.status, "value") else str(t.status),
        escalated_to_admin=t.escalated_to_admin,
        booking_id=str(t.booking_id) if t.booking_id else None,
        image_evidence_url=t.image_evidence_url,
        created_at=t.created_at.isoformat() if t.created_at else "",
        updated_at=t.updated_at.isoformat() if t.updated_at else "",
        messages=msgs
    )


@router.post(
    "/providers/me/tickets",
    response_model=SupportTicketResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a support ticket as a provider",
)
def create_my_ticket(
    data: ProviderTicketCreateRequest,
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    ticket = service.create_support_ticket(current_user, data)

    try:
        from app.services.kafka import kafka_producer, KafkaTopics, KafkaEvent
        msg_event = KafkaEvent(
            event_type=KafkaTopics.SUPPORT_MESSAGE,
            ticket_id=str(ticket.id),
            booking_id=str(ticket.booking_id) if ticket.booking_id else None,
            sender_id=str(current_user.id),
            payload={
                "ticket_id": str(ticket.id),
                "booking_id": str(ticket.booking_id) if ticket.booking_id else None,
                "sender_id": str(current_user.id),
                "sender_role": "provider",
                "sender_name": current_user.full_name,
                "subject": ticket.subject,
                "message_text": ticket.description or ticket.subject,
                "created_at": ticket.created_at.isoformat() if hasattr(ticket.created_at, "isoformat") else str(ticket.created_at),
            }
        )
        kafka_producer.publish_event(KafkaTopics.SUPPORT_MESSAGE, msg_event)
    except Exception as exc:
        print(f"[Provider Create Ticket Kafka Error] {exc}")

    return _serialize_ticket_response(ticket)


@router.get(
    "/providers/me/tickets",
    response_model=List[SupportTicketResponse],
    summary="List all support tickets created by the current provider",
)
def list_my_tickets(
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    tickets = service.list_my_tickets(current_user)
    return [_serialize_ticket_response(t) for t in tickets]


@router.get(
    "/providers/me/tickets/{ticket_id}",
    response_model=SupportTicketResponse,
    summary="Get single support ticket with messages",
)
def get_my_ticket(
    ticket_id: uuid.UUID,
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    ticket = service.get_my_ticket(current_user, ticket_id)
    return _serialize_ticket_response(ticket)


@router.post(
    "/providers/me/tickets/{ticket_id}/reply",
    response_model=TicketMessageResponse,
    summary="Reply to an existing support ticket",
)
def reply_my_ticket(
    ticket_id: uuid.UUID,
    payload: TicketReplyRequest,
    current_user: AuthUser = Depends(require_provider),
    service: ProviderServiceDomain = Depends(get_service_domain),
):
    ticket = service.get_my_ticket(current_user, ticket_id)
    msg = service.reply_to_ticket(current_user, ticket_id, payload.message_text, payload.attachment_url)

    try:
        from app.services.kafka import kafka_producer, KafkaTopics, KafkaEvent
        target_receiver = str(ticket.customer_id) if hasattr(ticket, 'customer_id') and ticket.customer_id else None
        cust_user_id = str(ticket.customer.user_id) if hasattr(ticket, 'customer') and ticket.customer and hasattr(ticket.customer, 'user_id') else None
        b_id = str(ticket.booking_id) if hasattr(ticket, 'booking_id') and ticket.booking_id else None
        msg_event = KafkaEvent(
            event_type=KafkaTopics.SUPPORT_MESSAGE,
            ticket_id=str(ticket_id),
            booking_id=b_id,
            sender_id=str(current_user.id),
            receiver_id=target_receiver,
            payload={
                "ticket_id": str(ticket_id),
                "booking_id": b_id,
                "message_id": str(msg.id),
                "sender_id": str(current_user.id),
                "sender_role": "provider",
                "sender_name": current_user.full_name,
                "receiver_id": target_receiver,
                "customer_id": target_receiver,
                "customer_user_id": cust_user_id,
                "message_text": msg.message_text,
                "attachment_url": msg.attachment_url,
                "created_at": msg.created_at.isoformat() if hasattr(msg.created_at, "isoformat") else str(msg.created_at),
            }
        )
        kafka_producer.publish_event(KafkaTopics.SUPPORT_MESSAGE, msg_event)
    except Exception as exc:
        print(f"[Provider Ticket Reply Kafka Error] {exc}")

    return TicketMessageResponse(
        id=str(msg.id),
        sender_id=str(msg.sender_id),
        sender_role=msg.sender_role,
        sender_name=getattr(msg, "sender_name", None) or current_user.full_name,
        message_text=msg.message_text,
        attachment_url=msg.attachment_url,
        created_at=msg.created_at.isoformat() if msg.created_at else ""
    )


# ==========================================
# BOOKING CHAT (Provider ↔ Customer)
# ==========================================

@router.get(
    "/providers/me/bookings/{booking_id}/chat",
    response_model=SupportTicketResponse,
    summary="Get or create the Customer ↔ Provider chat thread for a booking",
)
def get_my_booking_chat(
    booking_id: uuid.UUID,
    current_user: AuthUser = Depends(require_provider),
    db: Session = Depends(get_db),
):
    """Provider retrieves the chat thread for a specific booking they're assigned to."""
    from app.models.customer import SupportTicket, TicketMessage
    from datetime import datetime

    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden: You cannot access chats for bookings not assigned to you")
    if not booking.customer_id:
        raise HTTPException(status_code=400, detail="No customer linked to this booking")

    ticket = db.query(SupportTicket).filter(
        SupportTicket.booking_id == booking_id,
        SupportTicket.provider_id == current_user.id,
        SupportTicket.customer_id == booking.customer_id,
    ).first()

    if not ticket:
        ticket = SupportTicket(
            id=uuid.uuid4(),
            customer_id=booking.customer_id,
            provider_id=current_user.id,
            booking_id=booking_id,
            subject=f"Chat: {booking.service_name} (Booking {booking.booking_reference})",
            description=f"Booking chat thread between customer and provider for {booking.service_name}.",
            category="Booking Chat",
            priority="Normal",
            status="Open",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(ticket)
        db.commit()
        db.refresh(ticket)

    return _serialize_ticket_response(ticket)


@router.post(
    "/providers/me/bookings/{booking_id}/chat/messages",
    response_model=TicketMessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Provider sends a message in the Customer ↔ Provider booking chat",
)
def send_my_booking_chat_message(
    booking_id: uuid.UUID,
    payload: TicketReplyRequest,
    current_user: AuthUser = Depends(require_provider),
    db: Session = Depends(get_db),
):
    """Provider sends a message to the customer in a booking chat thread."""
    from app.models.customer import SupportTicket, TicketMessage
    from app.models.user import User
    from datetime import datetime

    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden: You cannot send messages in chats for bookings not assigned to you")
    if not booking.customer_id:
        raise HTTPException(status_code=400, detail="No customer linked to this booking")

    ticket = db.query(SupportTicket).filter(
        SupportTicket.booking_id == booking_id,
        SupportTicket.provider_id == current_user.id,
        SupportTicket.customer_id == booking.customer_id,
    ).first()

    if not ticket:
        ticket = SupportTicket(
            id=uuid.uuid4(),
            customer_id=booking.customer_id,
            provider_id=current_user.id,
            booking_id=booking_id,
            subject=f"Chat: {booking.service_name} (Booking {booking.booking_reference})",
            description=f"Booking chat thread between customer and provider for {booking.service_name}.",
            category="Booking Chat",
            priority="Normal",
            status="Open",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(ticket)
        db.flush()

    msg = TicketMessage(
        id=uuid.uuid4(),
        ticket_id=ticket.id,
        sender_id=current_user.id,
        sender_role="provider",
        sender_name=current_user.full_name,
        message_text=payload.message_text,
        attachment_url=payload.attachment_url,
        created_at=datetime.utcnow(),
    )
    db.add(msg)
    ticket.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(msg)

    try:
        from app.services.kafka import kafka_producer, KafkaTopics, KafkaEvent
        cust_id = str(booking.customer_id) if booking.customer_id else None
        cust_user_id = str(booking.customer.user_id) if booking.customer and hasattr(booking.customer, 'user_id') else None
        chat_event = KafkaEvent(
            event_type=KafkaTopics.SUPPORT_MESSAGE,
            ticket_id=str(ticket.id),
            booking_id=str(booking_id),
            sender_id=str(current_user.id),
            receiver_id=cust_id,
            payload={
                "ticket_id": str(ticket.id),
                "booking_id": str(booking_id),
                "message_id": str(msg.id),
                "sender_id": str(current_user.id),
                "sender_role": "provider",
                "sender_name": current_user.full_name,
                "receiver_id": cust_id,
                "customer_id": cust_id,
                "customer_user_id": cust_user_id,
                "message_text": msg.message_text,
                "attachment_url": msg.attachment_url,
                "category": "Booking Chat",
                "created_at": msg.created_at.isoformat() if hasattr(msg.created_at, "isoformat") else str(msg.created_at),
            }
        )
        kafka_producer.publish_event(KafkaTopics.SUPPORT_MESSAGE, chat_event)
    except Exception as exc:
        print(f"[Provider Booking Chat Kafka Error] {exc}")

    return TicketMessageResponse(
        id=str(msg.id),
        sender_id=str(msg.sender_id),
        sender_role=msg.sender_role,
        sender_name=msg.sender_name,
        message_text=msg.message_text,
        attachment_url=msg.attachment_url,
        created_at=msg.created_at.isoformat() if msg.created_at else "",
    )


# =====================================================================
# PROVIDER 2FA PRIVILEGED ACCOUNT SECURITY
# =====================================================================
@router.post("/providers/me/2fa/setup", response_model=TotpSetupResponse, summary="Setup TOTP 2FA for Provider")
def setup_provider_2fa(
    current_user: AuthUser = Depends(require_provider),
    db: Session = Depends(get_db)
):
    from app.services import security_service
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User account not found")
    res = security_service.setup_totp_2fa(db, user)
    return TotpSetupResponse(
        secret=res["secret"],
        provisioning_uri=res["provisioning_uri"],
        recovery_codes=res.get("recovery_codes")
    )


@router.post("/providers/me/2fa/verify", summary="Verify TOTP 2FA code and enable 2FA for Provider")
def verify_provider_2fa(
    req: TotpVerifyRequest,
    current_user: AuthUser = Depends(require_provider),
    db: Session = Depends(get_db)
):
    from app.services import security_service
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User account not found")
    is_valid = security_service.verify_totp_2fa(db, user, req.code)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid TOTP 2FA verification code")
    return {"status": "success", "message": "Provider 2FA verification successful and enabled."}


@router.post("/providers/me/2fa/disable", summary="Disable TOTP 2FA for Provider")
def disable_provider_2fa(
    current_user: AuthUser = Depends(require_provider),
    db: Session = Depends(get_db)
):
    from app.models.security import TwoFactorRecoveryCode
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User account not found")
    user.is_2fa_enabled = False
    user.totp_secret = None
    db.query(TwoFactorRecoveryCode).filter(TwoFactorRecoveryCode.user_id == user.id).delete(synchronize_session=False)
    db.commit()
    return {"status": "success", "message": "Provider 2FA disabled successfully."}
