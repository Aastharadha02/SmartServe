"""Add warranty cards, before/after photos, customer_notes, and combined bookings

Revision ID: g1_warranty_photos_combined
Revises: f1_service_emergency_eligible
Create Date: 2026-10-17
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = "g1_warranty_photos_combined"
down_revision: Union[str, None] = "8248923e7c12"
branch_labels = None
depends_on = None


def column_exists(conn, table, col):
    dialect_name = conn.dialect.name
    if dialect_name == "sqlite":
        res = conn.execute(sa.text(f"PRAGMA table_info({table})"))
        cols = [row[1] for row in res.fetchall()]
        return col in cols
    res = conn.execute(sa.text(
        f"SELECT column_name FROM information_schema.columns "
        f"WHERE table_schema='public' AND table_name='{table}' AND column_name='{col}'"
    ))
    return bool(res.scalar())


def table_exists(conn, table):
    dialect_name = conn.dialect.name
    if dialect_name == "sqlite":
        res = conn.execute(sa.text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'"))
        return bool(res.scalar())
    res = conn.execute(sa.text(
        f"SELECT table_name FROM information_schema.tables "
        f"WHERE table_schema='public' AND table_name='{table}'"
    ))
    return bool(res.scalar())


def upgrade() -> None:
    conn = op.get_bind()

    # 1. Add customer_notes, before_photos, after_photos to bookings
    if not column_exists(conn, "bookings", "customer_notes"):
        op.add_column("bookings", sa.Column("customer_notes", sa.Text(), nullable=True))
    if not column_exists(conn, "bookings", "before_photos"):
        op.add_column("bookings", sa.Column("before_photos", sa.JSON(), nullable=True))
    if not column_exists(conn, "bookings", "after_photos"):
        op.add_column("bookings", sa.Column("after_photos", sa.JSON(), nullable=True))
    if not column_exists(conn, "bookings", "service_name"):
        op.add_column("bookings", sa.Column("service_name", sa.String(255), nullable=True))
    if not column_exists(conn, "bookings", "category"):
        op.add_column("bookings", sa.Column("category", sa.String(100), nullable=True))

    # 2. Create booking_warranties table
    if not table_exists(conn, "booking_warranties"):
        op.create_table(
            "booking_warranties",
            sa.Column("id", sa.UUID(), primary_key=True),
            sa.Column("booking_id", sa.UUID(), sa.ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False, unique=True),
            sa.Column("customer_id", sa.UUID(), sa.ForeignKey("customers.id", ondelete="CASCADE"), nullable=False),
            sa.Column("provider_id", sa.UUID(), nullable=True),
            sa.Column("service_name", sa.String(255), nullable=False),
            sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
            sa.Column("claim_status", sa.String(50), nullable=False, server_default="None"),
            sa.Column("claim_description", sa.Text(), nullable=True),
            sa.Column("claim_submitted_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("claim_resolved_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("claim_notes", sa.Text(), nullable=True),
        )
        op.create_index("ix_booking_warranties_booking_id", "booking_warranties", ["booking_id"])
        op.create_index("ix_booking_warranties_customer_id", "booking_warranties", ["customer_id"])

    # 3. Create combined_bookings table
    if not table_exists(conn, "combined_bookings"):
        op.create_table(
            "combined_bookings",
            sa.Column("id", sa.UUID(), primary_key=True),
            sa.Column("customer_id", sa.UUID(), sa.ForeignKey("customers.id", ondelete="CASCADE"), nullable=False),
            sa.Column("status", sa.String(50), nullable=False, server_default="Requested"),
            sa.Column("total_price", sa.Numeric(10, 2), nullable=False, server_default="0.00"),
            sa.Column("discount_applied", sa.Numeric(10, 2), nullable=False, server_default="0.00"),
            sa.Column("final_price", sa.Numeric(10, 2), nullable=False, server_default="0.00"),
            sa.Column("scheduled_time", sa.DateTime(timezone=True), nullable=False),
            sa.Column("address", sa.String(500), nullable=False, server_default="Address on File"),
            sa.Column("customer_notes", sa.Text(), nullable=True),
            sa.Column("payment_status", sa.String(50), nullable=False, server_default="Pending"),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        )
        op.create_index("ix_combined_bookings_customer_id", "combined_bookings", ["customer_id"])

    # 4. Create combined_booking_items table
    if not table_exists(conn, "combined_booking_items"):
        op.create_table(
            "combined_booking_items",
            sa.Column("id", sa.UUID(), primary_key=True),
            sa.Column("combined_booking_id", sa.UUID(), sa.ForeignKey("combined_bookings.id", ondelete="CASCADE"), nullable=False),
            sa.Column("service_id", sa.UUID(), sa.ForeignKey("services.id", ondelete="CASCADE"), nullable=False),
            sa.Column("provider_id", sa.UUID(), nullable=True),
            sa.Column("unit_price", sa.Numeric(10, 2), nullable=False, server_default="0.00"),
            sa.Column("status", sa.String(50), nullable=False, server_default="Requested"),
            sa.Column("scheduled_time", sa.DateTime(timezone=True), nullable=True),
        )
        op.create_index("ix_combined_booking_items_parent", "combined_booking_items", ["combined_booking_id"])


def downgrade() -> None:
    conn = op.get_bind()
    if table_exists(conn, "combined_booking_items"):
        op.drop_table("combined_booking_items")
    if table_exists(conn, "combined_bookings"):
        op.drop_table("combined_bookings")
    if table_exists(conn, "booking_warranties"):
        op.drop_table("booking_warranties")
    if column_exists(conn, "bookings", "after_photos"):
        op.drop_column("bookings", "after_photos")
    if column_exists(conn, "bookings", "before_photos"):
        op.drop_column("bookings", "before_photos")
    if column_exists(conn, "bookings", "customer_notes"):
        op.drop_column("bookings", "customer_notes")

