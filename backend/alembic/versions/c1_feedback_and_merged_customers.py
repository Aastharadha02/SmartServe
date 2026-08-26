"""Add feedback table and merge auth fields into customers table

Revision ID: c1_feedback_and_merged_customers
Revises: b1_services_table
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "c1_feedback_and_merged_customers"
down_revision: Union[str, None] = "b1_services_table"
branch_labels = None
depends_on = None


def upgrade():
    # 1. Update customers table to merge identity / auth fields
    op.add_column("customers", sa.Column("email", sa.String(255), nullable=True))
    op.add_column("customers", sa.Column("password_hash", sa.String(255), nullable=True))
    op.add_column("customers", sa.Column("role", sa.String(50), nullable=False, server_default="customer"))
    op.add_column("customers", sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")))
    op.add_column("customers", sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False))

    # Populate email and password_hash from users table if available
    op.execute(
        """
        UPDATE customers c
        SET email = u.email,
            password_hash = u.password_hash
        FROM users u
        WHERE c.user_id = u.id
        """
    )
    # Set default values for any standalone customers
    op.execute("UPDATE customers SET email = CONCAT('customer_', id, '@smartserve.com') WHERE email IS NULL")
    op.execute("UPDATE customers SET password_hash = 'default_hash' WHERE password_hash IS NULL")

    op.alter_column("customers", "email", nullable=False)
    op.alter_column("customers", "password_hash", nullable=False)
    op.alter_column("customers", "user_id", nullable=True)
    op.create_index("ix_customers_email", "customers", ["email"], unique=True)

    # 2. Create feedback table
    op.create_table(
        "feedback",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("customer_id", sa.UUID(), nullable=False),
        sa.Column("provider_id", sa.UUID(), nullable=True),
        sa.Column("service_id", sa.UUID(), nullable=True),
        sa.Column("rating", sa.Float(), nullable=False),
        sa.Column("review_text", sa.Text(), nullable=True),
        sa.Column("sentiment_score", sa.Float(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["provider_id"], ["providers.user_id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["service_id"], ["services.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_feedback_customer_id", "feedback", ["customer_id"], unique=False)
    op.create_index("ix_feedback_provider_id", "feedback", ["provider_id"], unique=False)
    op.create_index("ix_feedback_service_id", "feedback", ["service_id"], unique=False)


def downgrade():
    op.drop_index("ix_feedback_service_id", table_name="feedback")
    op.drop_index("ix_feedback_provider_id", table_name="feedback")
    op.drop_index("ix_feedback_customer_id", table_name="feedback")
    op.drop_table("feedback")

    op.drop_index("ix_customers_email", table_name="customers")
    op.drop_column("customers", "created_at")
    op.drop_column("customers", "is_active")
    op.drop_column("customers", "role")
    op.drop_column("customers", "password_hash")
    op.drop_column("customers", "email")
