from enum import Enum as PyEnum
from app.models.customer import Booking

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

__all__ = ["Booking", "BookingStatus", "PaymentStatus"]


