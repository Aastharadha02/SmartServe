import uuid
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.customer import Booking
from app.models.booking import BookingStatus, PaymentStatus
from app.core.dependencies import AuthUser
from app.services.booking.otp_service import generate_secure_otp, get_active_otp, verify_and_consume_otp

# Valid state transitions mapping: source_status -> set of allowed next_statuses
ALLOWED_TRANSITIONS: Dict[str, set] = {
    BookingStatus.REQUESTED.value: {
        BookingStatus.ACCEPTED.value,
        BookingStatus.REJECTED.value,
        BookingStatus.CANCELLED.value,
        BookingStatus.EXPIRED.value,
    },
    BookingStatus.ASSIGNED.value: {
        BookingStatus.ACCEPTED.value,
        BookingStatus.REJECTED.value,
        BookingStatus.CANCELLED.value,
        BookingStatus.EXPIRED.value,
    },
    BookingStatus.ACCEPTED.value: {
        BookingStatus.ON_THE_WAY.value,
        BookingStatus.CANCELLED.value,
    },
    BookingStatus.ON_THE_WAY.value: {
        BookingStatus.ARRIVED.value,
        BookingStatus.CANCELLED.value,
    },
    BookingStatus.ARRIVED.value: {
        BookingStatus.STARTED.value,
        BookingStatus.CANCELLED.value,
    },
    BookingStatus.STARTED.value: {
        BookingStatus.COMPLETED.value,
        BookingStatus.PAID.value,
    },
    # Terminal states: strictly read-only, no further transitions allowed
    BookingStatus.COMPLETED.value: set(),
    BookingStatus.PAID.value: set(),
    BookingStatus.CANCELLED.value: set(),
    BookingStatus.REJECTED.value: set(),
    BookingStatus.EXPIRED.value: set(),
}

TERMINAL_STATES = {
    BookingStatus.COMPLETED.value,
    BookingStatus.PAID.value,
    BookingStatus.CANCELLED.value,
    BookingStatus.REJECTED.value,
    BookingStatus.EXPIRED.value,
}


STATUS_NORMALIZATION_MAP: Dict[str, str] = {
    "requested": BookingStatus.REQUESTED.value,
    "assigned": BookingStatus.ASSIGNED.value,
    "accepted": BookingStatus.ACCEPTED.value,
    "on_the_way": BookingStatus.ON_THE_WAY.value,
    "on the way": BookingStatus.ON_THE_WAY.value,
    "ontheway": BookingStatus.ON_THE_WAY.value,
    "arrived": BookingStatus.ARRIVED.value,
    "started": BookingStatus.STARTED.value,
    "completed": BookingStatus.COMPLETED.value,
    "paid": BookingStatus.PAID.value,
    "cancelled": BookingStatus.CANCELLED.value,
    "canceled": BookingStatus.CANCELLED.value,
    "rejected": BookingStatus.REJECTED.value,
    "declined": BookingStatus.REJECTED.value,
    "expired": BookingStatus.EXPIRED.value,
}


def normalize_status(val: Any) -> str:
    if val is None:
        return ""
    if hasattr(val, "value"):
        val = val.value
    cleaned = str(val).strip().lower().replace("-", "_")
    return STATUS_NORMALIZATION_MAP.get(cleaned, str(val).strip())


def get_current_status_val(booking: Booking) -> str:
    if hasattr(booking.status, "value"):
        return str(booking.status.value)
    return str(booking.status)


def transition_booking_status(
    db: Session,
    booking_id: uuid.UUID,
    next_status: str,
    user: AuthUser,
    reason: Optional[str] = None,
    otp_code: Optional[str] = None,
) -> Booking:
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with ID '{booking_id}' was not found.",
        )

    # 1. Strict Ownership Check: A provider can only transition their own assigned booking
    if user.role == "provider":
        if booking.provider_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: You cannot transition a booking assigned to another provider.",
            )

    curr_status = normalize_status(get_current_status_val(booking))
    next_status_normalized = normalize_status(next_status)

    # 2. Check if current state is terminal
    if curr_status in TERMINAL_STATES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid transition: Booking is in terminal state '{curr_status}' and cannot be altered.",
        )

    # 3. Enforce Strict State Machine Transition Rules
    allowed_next = ALLOWED_TRANSITIONS.get(curr_status, set())
    if next_status_normalized not in allowed_next:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Invalid state transition: Cannot transition booking from '{curr_status}' to '{next_status_normalized}'. "
                f"Allowed transitions from '{curr_status}' are: {list(allowed_next) or 'None (terminal)'}."
            ),
        )

    # Use normalized status for all subsequent checks and persistence
    next_status = next_status_normalized

    # 4. Enforce Start OTP Generation on On The Way / Arrived
    if next_status in [BookingStatus.ON_THE_WAY.value, BookingStatus.ARRIVED.value]:
        active_start = get_active_otp(booking.id, "START", db)
        if not active_start:
            generate_secure_otp(booking.id, "START", db)

    if next_status == BookingStatus.ARRIVED.value:
        tl_arrived = {
            "event": "Provider arrived at service location",
            "actor": user.full_name or user.email,
            "role": user.role,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        cur_tl = list(booking.timeline or [])
        cur_tl.append(tl_arrived)
        booking.timeline = cur_tl

    # 5. FIRST OTP: Starting the Service
    if next_status == BookingStatus.STARTED.value:
        if curr_status != BookingStatus.ARRIVED.value and user.role == "provider":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid state transition: Must mark 'Arrived' before starting service. Current status: '{curr_status}'.",
            )

        # Provider must provide valid Start OTP
        if user.role == "provider" or otp_code is not None:
            is_valid, msg = verify_and_consume_otp(booking.id, "START", otp_code, db)
            if not is_valid:
                tl_fail = {
                    "event": "Failed Service Start OTP Verification Attempt",
                    "actor": user.full_name or user.email,
                    "role": user.role,
                    "error": msg,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                cur_tl = list(booking.timeline or [])
                cur_tl.append(tl_fail)
                booking.timeline = cur_tl
                db.add(booking)
                db.commit()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=msg,
                )

            tl_otp = {
                "event": "Service Start OTP Verified",
                "actor": user.full_name or user.email,
                "role": user.role,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            cur_tl = list(booking.timeline or [])
            cur_tl.append(tl_otp)
            booking.timeline = cur_tl
            booking.otp_code = None  # Invalidate start code

        # Automatically generate Completion OTP for the customer to access
        generate_secure_otp(booking.id, "COMPLETE", db)

    # 6. SECOND OTP: Completing the Service
    if next_status == BookingStatus.COMPLETED.value:
        if curr_status != BookingStatus.STARTED.value and user.role == "provider":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid state transition: Service must be 'Started' before it can be 'Completed'. Current status: '{curr_status}'.",
            )

        # Provider must provide valid Completion OTP
        if user.role == "provider" or otp_code is not None:
            is_valid, msg = verify_and_consume_otp(booking.id, "COMPLETE", otp_code, db)
            if not is_valid:
                tl_fail = {
                    "event": "Failed Service Completion OTP Verification Attempt",
                    "actor": user.full_name or user.email,
                    "role": user.role,
                    "error": msg,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                cur_tl = list(booking.timeline or [])
                cur_tl.append(tl_fail)
                booking.timeline = cur_tl
                db.add(booking)
                db.commit()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=msg,
                )

            tl_otp = {
                "event": "Service Completion OTP Verified",
                "actor": user.full_name or user.email,
                "role": user.role,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            cur_tl = list(booking.timeline or [])
            cur_tl.append(tl_otp)
            booking.timeline = cur_tl

        # Issue Category-Specific Warranty (10-15 days for eligible home maintenance, excluding beauty)
        try:
            from app.services.booking.warranty_service import issue_booking_warranty
            issue_booking_warranty(booking, db)
        except Exception as e:
            pass
        try:
            from app.models.provider import ProviderLocation
            if booking.provider_id:
                loc = db.query(ProviderLocation).filter(ProviderLocation.provider_id == booking.provider_id).first()
                if loc:
                    loc.is_active = False
                    db.add(loc)
        except Exception:
            pass

        # IMPORTANT: Keep payment status separate from booking status!
        # Do not mark payment as completed/paid here. Payment remains in its current state
        # (e.g. Pending or Collection Reported) until reported and admin-verified.

    # 7. Release reserved slot if cancelled or rejected
    if next_status in [BookingStatus.REJECTED.value, BookingStatus.CANCELLED.value]:
        try:
            from app.models.provider import Availability
            if booking.provider_id and booking.scheduled_time:
                dt = booking.scheduled_time
                if hasattr(dt, "tzinfo") and dt.tzinfo is not None:
                    dt = dt.replace(tzinfo=None)
                req_date = dt.date()
                req_time = dt.time()
                reserved_slot = (
                    db.query(Availability)
                    .filter(
                        Availability.provider_id == booking.provider_id,
                        Availability.slot_date == req_date,
                        Availability.start_time <= req_time,
                        Availability.end_time >= req_time,
                        Availability.status == "RESERVED",
                    )
                    .first()
                )
                if reserved_slot:
                    reserved_slot.status = "FREE"
                    db.add(reserved_slot)
        except Exception:
            pass

    # 8. Append timeline audit event
    now_iso = datetime.now(timezone.utc).isoformat()
    timeline_event = {
        "event": f"Job status updated to {next_status}",
        "previous_status": curr_status,
        "status": next_status,
        "actor": user.full_name or user.email,
        "role": user.role,
        "reason": reason or "",
        "timestamp": now_iso,
    }
    current_timeline = list(booking.timeline or [])
    current_timeline.append(timeline_event)
    booking.timeline = current_timeline

    booking.status = next_status
    booking.updated_at = datetime.now(timezone.utc)

    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(booking, "timeline")

    db.commit()
    db.refresh(booking)

    # Automated Email & WhatsApp Notification Trigger
    try:
        from app.services.notification import notify_booking_event
        event_map = {
            BookingStatus.ACCEPTED.value: "booking.accepted",
            BookingStatus.REJECTED.value: "booking.rejected",
            BookingStatus.ASSIGNED.value: "booking.assigned",
            BookingStatus.STARTED.value: "service.started",
            BookingStatus.COMPLETED.value: "service.completed",
            BookingStatus.CANCELLED.value: "booking.cancelled",
        }
        if next_status in event_map:
            notify_booking_event(
                db,
                booking,
                event_map[next_status],
                extra_context={"notes": reason, "previous_status": curr_status},
            )
    except Exception as exc:
        # Never break or rollback successful state transition if notification fails
        pass

    return booking
