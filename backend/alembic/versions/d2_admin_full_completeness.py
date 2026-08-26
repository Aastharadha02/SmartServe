"""admin full completeness schema extensions

Revision ID: d2_admin_full_completeness
Revises: d1_admin_bookings_support_audit
Create Date: 2026-08-26 13:35:00.000000

"""
from alembic import op
import sqlalchemy as sqla
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd2_admin_full_completeness'
down_revision = 'd1_admin_bookings_support_audit'
branch_labels = None
depends_on = None

def upgrade() -> None:
    conn = op.get_bind()
    
    # Helper to check if column exists
    def column_exists(table_name, column_name):
        res = conn.execute(sqla.text(
            f"SELECT column_name FROM information_schema.columns WHERE table_name='{table_name}' AND column_name='{column_name}'"
        ))
        return bool(res.scalar())

    # 1. New tables
    op.create_table(
        'customer_flags',
        sqla.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sqla.Column('customer_id', postgresql.UUID(as_uuid=True), sqla.ForeignKey('customers.id', ondelete='CASCADE'), nullable=False),
        sqla.Column('flag_type', sqla.String(100), nullable=False),
        sqla.Column('reason', sqla.Text(), nullable=False),
        sqla.Column('flagged_by', postgresql.UUID(as_uuid=True), sqla.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sqla.Column('created_at', sqla.DateTime(timezone=True), nullable=False)
    )

    op.create_table(
        'email_templates',
        sqla.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sqla.Column('template_key', sqla.String(100), unique=True, nullable=False),
        sqla.Column('subject', sqla.String(255), nullable=False),
        sqla.Column('body_html', sqla.Text(), nullable=False),
        sqla.Column('updated_at', sqla.DateTime(timezone=True), nullable=False)
    )

    op.create_table(
        'email_logs',
        sqla.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sqla.Column('recipient_email', sqla.String(255), nullable=False),
        sqla.Column('subject', sqla.String(255), nullable=False),
        sqla.Column('template_key', sqla.String(100), nullable=True),
        sqla.Column('status', sqla.String(50), nullable=False, server_default='Sent'),
        sqla.Column('sent_at', sqla.DateTime(timezone=True), nullable=False)
    )

    op.create_table(
        'active_sessions',
        sqla.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sqla.Column('user_id', postgresql.UUID(as_uuid=True), sqla.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sqla.Column('token_jti', sqla.String(255), unique=True, nullable=False),
        sqla.Column('ip_address', sqla.String(50), nullable=True),
        sqla.Column('user_agent', sqla.String(500), nullable=True),
        sqla.Column('is_revoked', sqla.Boolean(), nullable=False, server_default='false'),
        sqla.Column('created_at', sqla.DateTime(timezone=True), nullable=False),
        sqla.Column('expires_at', sqla.DateTime(timezone=True), nullable=False)
    )

    op.create_table(
        'suspicious_activities',
        sqla.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sqla.Column('user_id', postgresql.UUID(as_uuid=True), sqla.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sqla.Column('anomaly_type', sqla.String(100), nullable=False),
        sqla.Column('risk_score', sqla.Float(), nullable=False, server_default='0.5'),
        sqla.Column('details_json', postgresql.JSONB(astext_type=sqla.Text()), nullable=True),
        sqla.Column('created_at', sqla.DateTime(timezone=True), nullable=False)
    )

    # 2. Add columns to existing tables safely
    if not column_exists('users', 'totp_secret'):
        op.add_column('users', sqla.Column('totp_secret', sqla.String(64), nullable=True))
    if not column_exists('users', 'is_2fa_enabled'):
        op.add_column('users', sqla.Column('is_2fa_enabled', sqla.Boolean(), nullable=False, server_default='false'))

    if not column_exists('feedback', 'sentiment_score'):
        op.add_column('feedback', sqla.Column('sentiment_score', sqla.Numeric(3, 2), nullable=True))
    if not column_exists('feedback', 'ai_category'):
        op.add_column('feedback', sqla.Column('ai_category', sqla.String(100), nullable=True))

    if not column_exists('certificates', 'document_number'):
        op.add_column('certificates', sqla.Column('document_number', sqla.String(100), nullable=True))
    if not column_exists('certificates', 'expiry_date'):
        op.add_column('certificates', sqla.Column('expiry_date', sqla.DateTime(timezone=True), nullable=True))
    if not column_exists('certificates', 'extracted_name'):
        op.add_column('certificates', sqla.Column('extracted_name', sqla.String(255), nullable=True))
    if not column_exists('certificates', 'is_duplicate'):
        op.add_column('certificates', sqla.Column('is_duplicate', sqla.Boolean(), nullable=False, server_default='false'))

def downgrade() -> None:
    op.drop_table('suspicious_activities')
    op.drop_table('active_sessions')
    op.drop_table('email_logs')
    op.drop_table('email_templates')
    op.drop_table('customer_flags')
