import uuid
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class NotificationResponse(BaseModel):
    id: uuid.UUID
    booking_id: Optional[uuid.UUID] = None
    booking_reference: Optional[str] = None
    customer_id: Optional[uuid.UUID] = None
    event_type: str
    channel: str
    recipient: str
    delivery_status: str
    retry_count: int
    last_attempt_at: datetime
    provider_message_id: Optional[str] = None
    error_message: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CustomerNotificationItem(BaseModel):
    id: uuid.UUID
    booking_reference: Optional[str] = None
    event_type: str
    channel: str
    recipient: str
    delivery_status: str
    last_attempt_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RescheduleBookingPayload(BaseModel):
    new_date: str  # YYYY-MM-DD
    new_time: str  # e.g. "09:00 AM" or "14:00"
    reason: Optional[str] = None
