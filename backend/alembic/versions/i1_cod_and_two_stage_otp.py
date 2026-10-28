"""Add COD Payments and Two-Stage OTP verification tables and columns

Revision ID: i1_cod_and_two_stage_otp
Revises: h1_oauth_accounts
Create Date: 2026-10-17

Additive migration:
1. Adds payment_method column to bookings table (defaulting to 'COD')
2. Creates booking_payments table for cash collection reports, admin review, discrepancy tracking, and audit trails
3. Creates booking_otps table for two-stage OTP verification (START and COMPLETE) with attempt limits, expirations, and lockout
4. Backfills payments and active start OTPs for existing bookings
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = 'i1_cod_and_two_stage_otp'
down_revision = 'h1_oauth_accounts'
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


def column_exists(conn, table, col):
    try:
        res = conn.execute(sa.text(
            f"SELECT column_name FROM information_schema.columns "
            f"WHERE table_schema='public' AND table_name='{table}' AND column_name='{col}'"
        ))
        return bool(res.scalar())
    except Exception:
        return False


def upgrade():
    conn = op.get_bind()

    # 1. Add payment_method column to bookings if missing
    if not column_exists(conn, 'bookings', 'payment_method'):
        op.add_column(
            'bookings',
            sa.Column('payment_method', sa.String(50), nullable=False, server_default='COD')
        )

    # 2. Create booking_payments table
    if not table_exists(conn, 'booking_payments'):
        op.create_table(
            'booking_payments',
            sa.Column('id', UUID(as_uuid=True), primary_key=True),
            sa.Column('booking_id', UUID(as_uuid=True), sa.ForeignKey('bookings.id', ondelete='CASCADE'), nullable=False),
            sa.Column('customer_id', UUID(as_uuid=True), sa.ForeignKey('customers.id', ondelete='CASCADE'), nullable=False),
            sa.Column('provider_id', UUID(as_uuid=True), sa.ForeignKey('providers.user_id', ondelete='SET NULL'), nullable=True),
            sa.Column('payment_method', sa.String(50), nullable=False, server_default='COD'),
            sa.Column('agreed_amount', sa.Numeric(10, 2), nullable=False, server_default='0.00'),
            sa.Column('reported_amount', sa.Numeric(10, 2), nullable=True),
            sa.Column('status', sa.String(50), nullable=False, server_default='Pending'),
            sa.Column('discrepancy_flag', sa.Boolean(), nullable=False, server_default=sa.text('false')),
            sa.Column('discrepancy_amount', sa.Numeric(10, 2), nullable=False, server_default='0.00'),
            sa.Column('collected_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('collection_notes', sa.Text(), nullable=True),
            sa.Column('reviewed_by_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
            sa.Column('reviewed_by_name', sa.String(255), nullable=True),
            sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('rejection_reason', sa.Text(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        )
        op.create_index('ix_booking_payments_booking_id', 'booking_payments', ['booking_id'])
        op.create_index('ix_booking_payments_customer_id', 'booking_payments', ['customer_id'])
        op.create_index('ix_booking_payments_provider_id', 'booking_payments', ['provider_id'])
        op.create_index('ix_booking_payments_status', 'booking_payments', ['status'])

    # 3. Create booking_otps table
    if not table_exists(conn, 'booking_otps'):
        op.create_table(
            'booking_otps',
            sa.Column('id', UUID(as_uuid=True), primary_key=True),
            sa.Column('booking_id', UUID(as_uuid=True), sa.ForeignKey('bookings.id', ondelete='CASCADE'), nullable=False),
            sa.Column('otp_type', sa.String(20), nullable=False),
            sa.Column('otp_code', sa.String(20), nullable=False),
            sa.Column('is_used', sa.Boolean(), nullable=False, server_default=sa.text('false')),
            sa.Column('used_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
            sa.Column('failed_attempts', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('max_attempts', sa.Integer(), nullable=False, server_default='5'),
            sa.Column('is_locked', sa.Boolean(), nullable=False, server_default=sa.text('false')),
            sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        )
        op.create_index('ix_booking_otps_booking_id', 'booking_otps', ['booking_id'])
        op.create_index('ix_booking_otps_otp_type', 'booking_otps', ['otp_type'])

    # 4. Backfill existing bookings into booking_payments
    try:
        conn.execute(sa.text("""
            INSERT INTO booking_payments (
                id, booking_id, customer_id, provider_id, payment_method, agreed_amount, status, created_at, updated_at
            )
            SELECT 
                gen_random_uuid(), b.id, b.customer_id, b.provider_id, 'COD', b.total_price,
                CASE 
                    WHEN b.payment_status IN ('Paid', 'Completed') THEN 'Paid'
                    ELSE 'Pending'
                END,
                b.created_at, b.updated_at
            FROM bookings b
            WHERE NOT EXISTS (
                SELECT 1 FROM booking_payments bp WHERE bp.booking_id = b.id
            )
        """))
    except Exception as e:
        print(f"[Migration Notice] Backfill booking_payments: {e}")

    # 5. Backfill existing start OTPs into booking_otps
    try:
        conn.execute(sa.text("""
            INSERT INTO booking_otps (
                id, booking_id, otp_type, otp_code, is_used, expires_at, created_at
            )
            SELECT 
                gen_random_uuid(), b.id, 'START', b.otp_code,
                CASE WHEN b.status IN ('Started', 'Completed', 'Paid') THEN true ELSE false END,
                b.created_at + interval '24 hours',
                b.created_at
            FROM bookings b
            WHERE b.otp_code IS NOT NULL AND b.otp_code != ''
            AND NOT EXISTS (
                SELECT 1 FROM booking_otps bo WHERE bo.booking_id = b.id AND bo.otp_type = 'START'
            )
        """))
    except Exception as e:
        print(f"[Migration Notice] Backfill booking_otps: {e}")


def downgrade():
    conn = op.get_bind()
    if table_exists(conn, 'booking_otps'):
        op.drop_table('booking_otps')
    if table_exists(conn, 'booking_payments'):
        op.drop_table('booking_payments')
    if column_exists(conn, 'bookings', 'payment_method'):
        op.drop_column('bookings', 'payment_method')
