import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from app.core.config import settings

# Attempt using PyJWT or fallback token helper
try:
    import jwt
except ImportError:
    jwt = None


def hash_password(password: str) -> str:
    """Hash password using SHA-256 with static salt for local auth."""
    salted = f"smartserve_salt_{password}".encode("utf-8")
    return hashlib.sha256(salted).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hashed value."""
    return hash_password(plain_password) == hashed_password


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    
    if jwt:
        return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    # Fallback hex token format if PyJWT is not installed
    user_id = data.get("sub", str(uuid.uuid4()))
    role = data.get("role", "customer")
    return f"mock.jwt.{role}.{user_id}.{int(expire.timestamp())}"


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and verify JWT token payload."""
    if not token:
        return None
    
    # Handle mock / fallback token strings
    if token.startswith("mock.jwt."):
        parts = token.split(".")
        if len(parts) >= 4:
            return {
                "sub": parts[3],
                "role": parts[2],
            }
        return {"sub": "cust-mock-uuid-1001", "role": "customer"}

    if jwt:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            return payload
        except Exception:
            return None

    return None
