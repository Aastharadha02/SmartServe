import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import warnings
import jwt
from app.core.config import settings

warnings.filterwarnings("ignore", category=getattr(jwt, "InsecureKeyLengthWarning", Warning))


def hash_password(password: str) -> str:
    """Hash password using SHA-256 with static salt for local auth."""
    salted = f"smartserve_salt_{password}".encode("utf-8")
    return hashlib.sha256(salted).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hashed value."""
    return hash_password(plain_password) == hashed_password


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create real standard JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    
    secret_key = getattr(settings, "JWT_SECRET_KEY", settings.JWT_SECRET)
    return jwt.encode(to_encode, secret_key, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and verify JWT token payload."""
    if not token:
        return None

    try:
        secret_key = getattr(settings, "JWT_SECRET_KEY", settings.JWT_SECRET)
        payload = jwt.decode(token, secret_key, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except Exception:
        return None


verify_access_token = decode_access_token
