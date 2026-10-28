"""Add notification_logs table for automated booking notifications

Revision ID: j1_automated_booking_notifications
Revises: i1_cod_and_two_stage_otp
Create Date: 2026-10-17

Additive migration:
1. Creates notification_logs table for tracking automated Email and WhatsApp booking events
2. Adds indices on booking_reference, idempotency_key, and delivery_status
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = 'j1_booking_notifications'
down_revision = 'i1_cod_and_two_stage_otp'
branch_labels = None
depends_on = None


def table_exists(conn, table):
    try:
        from alembic import context
        if context.is_offline_mode():
            return False
        res = conn.execute(sa.text(
            f"SELECT table_name FROM information_schema.tables "
            f"WHERE table_schema='public' AND table_name='{table}'"
        ))
        return bool(res.scalar())
    except Exception:
        return False


def upgrade():
    conn = op.get_bind()

    if not table_exists(conn, "notification_logs"):
        op.create_table(
            "notification_logs",
            sa.Column("id", UUID(as_uuid=True), primary_key=True),
            sa.Column("booking_id", UUID(as_uuid=True), sa.ForeignKey("bookings.id", ondelete="CASCADE"), nullable=True),
            sa.Column("booking_reference", sa.String(50), nullable=True),
            sa.Column("customer_id", UUID(as_uuid=True), sa.ForeignKey("customers.id", ondelete="SET NULL"), nullable=True),
            sa.Column("event_type", sa.String(50), nullable=False),
            sa.Column("channel", sa.String(20), nullable=False),
            sa.Column("recipient", sa.String(255), nullable=False),
            sa.Column("delivery_status", sa.String(50), nullable=False, server_default="Pending"),
            sa.Column("idempotency_key", sa.String(128), nullable=False, unique=True),
            sa.Column("retry_count", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("last_attempt_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
            sa.Column("provider_message_id", sa.String(255), nullable=True),
            sa.Column("error_message", sa.String(500), nullable=True),
            sa.Column("metadata_json", sa.JSON(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        )
        op.create_index("ix_notification_logs_booking_id", "notification_logs", ["booking_id"])
        op.create_index("ix_notification_logs_booking_reference", "notification_logs", ["booking_reference"])
        op.create_index("ix_notification_logs_customer_id", "notification_logs", ["customer_id"])
        op.create_index("ix_notification_logs_event_type", "notification_logs", ["event_type"])
        op.create_index("ix_notification_logs_channel", "notification_logs", ["channel"])
        op.create_index("ix_notification_logs_delivery_status", "notification_logs", ["delivery_status"])
        op.create_index("ix_notification_logs_idempotency_key", "notification_logs", ["idempotency_key"])


def downgrade():
    conn = op.get_bind()
    if table_exists(conn, "notification_logs"):
        op.drop_table("notification_logs")
