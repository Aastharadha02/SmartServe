"""Add services table

Revision ID: b1_services_table
Revises: a1_users_customers_auth
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "b1_services_table"
down_revision: Union[str, None] = "a1_users_customers_auth"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "services",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("category", sa.String(length=255), nullable=False),
        sa.Column("subcategory", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("base_price", sa.Float(), nullable=False),
        sa.Column("max_demand_increase", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("max_discount", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("distinct_features", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("suggested_addons", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_services_category", "services", ["category"], unique=False)
    op.create_index("ix_services_subcategory", "services", ["subcategory"], unique=False)
    op.create_index("ix_services_name", "services", ["name"], unique=False)


def downgrade():
    op.drop_index("ix_services_name", table_name="services")
    op.drop_index("ix_services_subcategory", table_name="services")
    op.drop_index("ix_services_category", table_name="services")
    op.drop_table("services")
