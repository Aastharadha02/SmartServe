"""Add coupons and coupon redemptions tables, plus booking coupon columns

Revision ID: k1_coupons_and_redemptions
Revises: j1_booking_notifications, g1_warranty_photos_combined
Create Date: 2026-11-01 17:26:00.000000
"""
from typing import Sequence, Union
import uuid
from datetime import datetime, timezone
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "k1_coupons_and_redemptions"
down_revision: Union[str, Sequence[str], None] = ("j1_booking_notifications", "g1_warranty_photos_combined")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create coupons table
    op.create_table(
        "coupons",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("code", sa.String(50), nullable=False, unique=True),
        sa.Column("description", sa.String(255), nullable=True),
        sa.Column("discount_type", sa.String(20), nullable=False, server_default="FIXED"),
        sa.Column("discount_value", sa.Numeric(10, 2), nullable=False, server_default="0.00"),
        sa.Column("max_discount_amount", sa.Numeric(10, 2), nullable=True),
        sa.Column("min_order_amount", sa.Numeric(10, 2), nullable=False, server_default="0.00"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("valid_from", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("valid_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("max_uses", sa.Integer(), nullable=True),
        sa.Column("max_uses_per_customer", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("applicable_categories", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("applicable_services", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("is_spin_reward", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("customers.id", ondelete="CASCADE"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_coupons_code", "coupons", ["code"], unique=True)
    op.create_index("ix_coupons_customer_id", "coupons", ["customer_id"])

    # 2. Create coupon_redemptions table
    op.create_table(
        "coupon_redemptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("coupon_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("coupons.id", ondelete="CASCADE"), nullable=False),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("customers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("booking_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("bookings.id", ondelete="SET NULL"), nullable=True),
        sa.Column("combined_booking_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("combined_bookings.id", ondelete="SET NULL"), nullable=True),
        sa.Column("discount_applied", sa.Numeric(10, 2), nullable=False),
        sa.Column("order_amount_before_discount", sa.Numeric(10, 2), nullable=False),
        sa.Column("final_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("redeemed_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_coupon_redemptions_coupon_id", "coupon_redemptions", ["coupon_id"])
    op.create_index("ix_coupon_redemptions_customer_id", "coupon_redemptions", ["customer_id"])
    op.create_index("ix_coupon_redemptions_booking_id", "coupon_redemptions", ["booking_id"])
    op.create_index("ix_coupon_redemptions_combined_booking_id", "coupon_redemptions", ["combined_booking_id"])

    # 3. Add columns to bookings
    conn = op.get_bind()
    conn.execute(sa.text("ALTER TABLE bookings ADD COLUMN IF NOT EXISTS coupon_code VARCHAR(50);"))
    conn.execute(sa.text("ALTER TABLE bookings ADD COLUMN IF NOT EXISTS coupon_discount NUMERIC(10, 2) NOT NULL DEFAULT 0.00;"))

    # 4. Add columns to combined_bookings
    conn.execute(sa.text("ALTER TABLE combined_bookings ADD COLUMN IF NOT EXISTS coupon_code VARCHAR(50);"))
    conn.execute(sa.text("ALTER TABLE combined_bookings ADD COLUMN IF NOT EXISTS coupon_discount NUMERIC(10, 2) NOT NULL DEFAULT 0.00;"))

    # 5. Seed standard coupons
    coupons_table = sa.table(
        "coupons",
        sa.column("id", postgresql.UUID(as_uuid=True)),
        sa.column("code", sa.String),
        sa.column("description", sa.String),
        sa.column("discount_type", sa.String),
        sa.column("discount_value", sa.Numeric),
        sa.column("max_discount_amount", sa.Numeric),
        sa.column("min_order_amount", sa.Numeric),
        sa.column("is_active", sa.Boolean),
        sa.column("max_uses_per_customer", sa.Integer),
        sa.column("is_spin_reward", sa.Boolean),
    )

    op.bulk_insert(
        coupons_table,
        [
            {
                "id": uuid.uuid4(),
                "code": "WELCOME50",
                "description": "Flat ₹50 off on first home service order",
                "discount_type": "FIXED",
                "discount_value": 50.00,
                "max_discount_amount": None,
                "min_order_amount": 299.00,
                "is_active": True,
                "max_uses_per_customer": 1,
                "is_spin_reward": False,
            },
            {
                "id": uuid.uuid4(),
                "code": "SERVE75",
                "description": "Flat ₹75 loyalty discount on home service bookings",
                "discount_type": "FIXED",
                "discount_value": 75.00,
                "max_discount_amount": None,
                "min_order_amount": 399.00,
                "is_active": True,
                "max_uses_per_customer": 2,
                "is_spin_reward": False,
            },
            {
                "id": uuid.uuid4(),
                "code": "FESTIVE10",
                "description": "10% off up to ₹150 on home maintenance",
                "discount_type": "PERCENTAGE",
                "discount_value": 10.00,
                "max_discount_amount": 150.00,
                "min_order_amount": 499.00,
                "is_active": True,
                "max_uses_per_customer": 3,
                "is_spin_reward": False,
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("coupon_redemptions")
    op.drop_table("coupons")
    conn = op.get_bind()
    conn.execute(sa.text("ALTER TABLE bookings DROP COLUMN IF EXISTS coupon_code;"))
    conn.execute(sa.text("ALTER TABLE bookings DROP COLUMN IF EXISTS coupon_discount;"))
    conn.execute(sa.text("ALTER TABLE combined_bookings DROP COLUMN IF EXISTS coupon_code;"))
    conn.execute(sa.text("ALTER TABLE combined_bookings DROP COLUMN IF EXISTS coupon_discount;"))

