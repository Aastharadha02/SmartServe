from enum import Enum as PyEnum

class BookingStatus(str, PyEnum):
    REQUESTED = "Requested"
    ASSIGNED = "Assigned"
    ACCEPTED = "Accepted"
    STARTED = "Started"
    COMPLETED = "Completed"
    PAID = "Paid"
    CANCELLED = "Cancelled"
    REJECTED = "Rejected"
    EXPIRED = "Expired"

class PaymentStatus(str, PyEnum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"
    REFUNDED = "Refunded"

def __getattr__(name):
    if name == "Booking":
        from app.models.customer import Booking
        return Booking
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = ["BookingStatus", "PaymentStatus", "Booking"]



