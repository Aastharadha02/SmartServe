from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class AuditLogResponse(BaseModel):
    id: str
    actor_email: str
    actor_role: str
    action: str
    target_resource: Optional[str] = None
    ip_address: Optional[str] = None
    risk_level: str
    metadata_json: Optional[Dict[str, Any]] = None
    created_at: str

class FailedLoginAttemptResponse(BaseModel):
    id: str
    email: str
    ip_address: Optional[str] = None
    attempt_count: int
    last_attempt: str
    locked_until: Optional[str] = None
