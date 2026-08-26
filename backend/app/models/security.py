import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    actor_email = Column(String(255), nullable=False)
    actor_role = Column(String(50), nullable=False)
    
    action = Column(String(255), nullable=False, index=True)
    target_resource = Column(String(255), nullable=True)
    ip_address = Column(String(100), nullable=True)
    risk_level = Column(String(50), nullable=False, default="Info", index=True) # Info, Warning, Critical
    
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), index=True)

class FailedLoginAttempt(Base):
    __tablename__ = "failed_login_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, index=True)
    ip_address = Column(String(100), nullable=True)
    attempt_count = Column(Integer, nullable=False, default=1)
    last_attempt = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    locked_until = Column(DateTime(timezone=True), nullable=True)

class AdminRole(Base):
    __tablename__ = "admin_roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    role_name = Column(String(100), nullable=False) # super_admin, operations_admin, support_admin
    permissions = Column(JSON, nullable=False, default=list)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
