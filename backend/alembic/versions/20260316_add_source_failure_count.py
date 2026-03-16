"""add source failure_count

Revision ID: 20260316_fc
Revises: 20260316_seq
Create Date: 2026-03-16

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260316_fc"
down_revision: Union[str, Sequence[str], None] = "20260316_seq"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("sources", sa.Column("failure_count", sa.Integer(), nullable=False, server_default="0"))


def downgrade() -> None:
    op.drop_column("sources", "failure_count")
