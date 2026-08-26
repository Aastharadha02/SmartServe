from typing import Optional, Dict, Any
from pydantic import BaseModel

class TotpSetupResponse(BaseModel):
    secret: str
    provisioning_uri: str

class TotpVerifyRequest(BaseModel):
    code: str

class ActiveSessionResponse(BaseModel):
    id: str
    user_id: str
    token_jti: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    is_revoked: bool
    created_at: str
    expires_at: str

class SuspiciousActivityResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    anomaly_type: str
    risk_score: float
    details_json: Optional[Dict[str, Any]] = None
    created_at: str
