from enum import Enum as PyEnum
from app.models.payment import PaymentStatus, PaymentMethod, OTPType, BookingPayment, BookingOTP

class BookingStatus(str, PyEnum):
    REQUESTED = "Requested"
    ASSIGNED = "Assigned"
    ACCEPTED = "Accepted"
    ON_THE_WAY = "On The Way"
    ARRIVED = "Arrived"
    STARTED = "Started"
    COMPLETED = "Completed"
    PAID = "Paid"
    CANCELLED = "Cancelled"
    REJECTED = "Rejected"
    EXPIRED = "Expired"

def __getattr__(name):
    if name == "Booking":
        from app.models.customer import Booking
        return Booking
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = [
    "BookingStatus",
    "PaymentStatus",
    "PaymentMethod",
    "OTPType",
    "BookingPayment",
    "BookingOTP",
    "Booking"
]




