"""Add catalog performance indexes on services table

Revision ID: l1_catalog_performance_indexes
Revises: k1_coupons_and_redemptions
Create Date: 2026-11-02 10:25:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "l1_catalog_performance_indexes"
down_revision: Union[str, Sequence[str], None] = "k1_coupons_and_redemptions"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create composite index on (is_active, category, subcategory) for fast category aggregation
    op.create_index(
        "ix_services_active_cat_sub",
        "services",
        ["is_active", "category", "subcategory"],
        if_not_exists=True,
    )
    # Create composite index on (is_active, category) for fast filtered catalog lookups
    op.create_index(
        "ix_services_active_cat",
        "services",
        ["is_active", "category"],
        if_not_exists=True,
    )


def downgrade() -> None:
    op.drop_index("ix_services_active_cat", table_name="services", if_exists=True)
    op.drop_index("ix_services_active_cat_sub", table_name="services", if_exists=True)
