import secrets
import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from app.models.payment import BookingOTP, OTPType
from app.models.customer import Booking


def generate_secure_otp(
    booking_id: uuid.UUID,
    otp_type: str,
    db: Session,
    expires_in_minutes: int = 180,
    digits: int = 4,
) -> BookingOTP:
    """
    Securely generate a numeric OTP for a booking (START or COMPLETE).
    Invalidates any previous unused OTPs of the same type for this booking.
    """
    otp_type_norm = str(otp_type).strip().upper()
    now_utc = datetime.now(timezone.utc)

    # Invalidate previous unconsumed OTPs for this booking & type
    previous_otps = (
        db.query(BookingOTP)
        .filter(
            BookingOTP.booking_id == booking_id,
            BookingOTP.otp_type == otp_type_norm,
            BookingOTP.is_used == False,
        )
        .all()
    )
    for prev in previous_otps:
        prev.is_used = True
        prev.used_at = now_utc
        db.add(prev)

    # Cryptographically secure random 4-digit code (1000 - 9999)
    min_val = 10 ** (digits - 1)
    max_val = (10 ** digits) - 1
    code_int = secrets.randbelow(max_val - min_val + 1) + min_val
    code_str = str(code_int)

    new_otp = BookingOTP(
        id=uuid.uuid4(),
        booking_id=booking_id,
        otp_type=otp_type_norm,
        otp_code=code_str,
        is_used=False,
        used_at=None,
        expires_at=now_utc + timedelta(minutes=expires_in_minutes),
        failed_attempts=0,
        max_attempts=5,
        is_locked=False,
        created_at=now_utc,
    )
    db.add(new_otp)

    # Also sync start OTP to legacy booking.otp_code if type is START
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking:
        if otp_type_norm == "START":
            booking.otp_code = code_str
            db.add(booking)

    db.commit()
    db.refresh(new_otp)
    return new_otp


def get_active_otp(
    booking_id: uuid.UUID,
    otp_type: str,
    db: Session,
) -> Optional[BookingOTP]:
    """Retrieve the current active (unused & non-expired & non-locked) OTP."""
    otp_type_norm = str(otp_type).strip().upper()
    now_utc = datetime.now(timezone.utc)
    return (
        db.query(BookingOTP)
        .filter(
            BookingOTP.booking_id == booking_id,
            BookingOTP.otp_type == otp_type_norm,
            BookingOTP.is_used == False,
            BookingOTP.is_locked == False,
            BookingOTP.expires_at > now_utc,
        )
        .order_by(BookingOTP.created_at.desc())
        .first()
    )


def verify_and_consume_otp(
    booking_id: uuid.UUID,
    otp_type: str,
    input_code: Optional[str],
    db: Session,
) -> Tuple[bool, str]:
    """
    Validate and consume an OTP.
    Enforces expiration, attempt limits, single-use, lockouts, and timing-safe comparison.
    """
    if not input_code or not str(input_code).strip():
        return False, f"A valid 4-digit {otp_type.lower()} OTP is required."

    clean_code = str(input_code).strip()
    otp_type_norm = str(otp_type).strip().upper()
    now_utc = datetime.now(timezone.utc)

    # Fetch latest OTP record for this booking and type
    otp_record = (
        db.query(BookingOTP)
        .filter(
            BookingOTP.booking_id == booking_id,
            BookingOTP.otp_type == otp_type_norm,
        )
        .order_by(BookingOTP.created_at.desc())
        .first()
    )

    if not otp_record:
        # Fallback check against legacy booking.otp_code only for START OTP
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if booking and otp_type_norm == "START" and booking.otp_code:
            if secrets.compare_digest(booking.otp_code.strip(), clean_code):
                booking.otp_code = None
                db.add(booking)
                db.commit()
                return True, "Start OTP verified successfully."
        return False, f"No active {otp_type.lower()} OTP found for this booking."

    if otp_record.is_used:
        return False, f"This {otp_type.lower()} OTP has already been used and cannot be reused."

    if otp_record.is_locked or otp_record.failed_attempts >= otp_record.max_attempts:
        return False, f"Too many incorrect attempts. This {otp_type.lower()} OTP is locked for security."

    if now_utc > otp_record.expires_at:
        return False, f"This {otp_type.lower()} OTP has expired. Please request a new OTP."

    # Timing-safe comparison to prevent timing attacks
    if not secrets.compare_digest(otp_record.otp_code.strip(), clean_code):
        otp_record.failed_attempts += 1
        if otp_record.failed_attempts >= otp_record.max_attempts:
            otp_record.is_locked = True
        db.add(otp_record)
        db.commit()
        remaining = max(0, otp_record.max_attempts - otp_record.failed_attempts)
        if otp_record.is_locked:
            return False, f"Incorrect {otp_type.lower()} OTP. Maximum attempts reached. OTP is locked."
        return False, f"Incorrect {otp_type.lower()} OTP. {remaining} attempt{'s' if remaining != 1 else ''} remaining."

    # Mark as successfully used
    otp_record.is_used = True
    otp_record.used_at = now_utc
    db.add(otp_record)

    # Invalidate legacy booking.otp_code if start
    if otp_type_norm == "START":
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if booking:
            booking.otp_code = None
            db.add(booking)

    db.commit()
    return True, f"Service {otp_type.lower()} OTP verified successfully."
