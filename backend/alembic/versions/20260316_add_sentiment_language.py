"""add sentiment_score and language

Revision ID: 20260316_s71
Revises: 7869285745f9
Create Date: 2026-03-16

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260316_s71"
down_revision: Union[str, Sequence[str], None] = "7869285745f9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("ai_results", sa.Column("sentiment_score", sa.Float(), nullable=True))
    op.add_column("articles", sa.Column("language", sa.String(10), nullable=False, server_default="zh"))


def downgrade() -> None:
    op.drop_column("articles", "language")
    op.drop_column("ai_results", "sentiment_score")
