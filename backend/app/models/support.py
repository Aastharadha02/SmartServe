from enum import Enum as PyEnum
from app.models.customer import SupportTicket, TicketMessage

class TicketPriority(str, PyEnum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    URGENT = "Urgent"

class TicketStatus(str, PyEnum):
    OPEN = "Open"
    IN_PROGRESS = "In_Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"

__all__ = ["SupportTicket", "TicketMessage", "TicketPriority", "TicketStatus"]

