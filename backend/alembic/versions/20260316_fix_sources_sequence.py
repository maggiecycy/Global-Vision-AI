"""fix sources id sequence

Revision ID: 20260316_seq
Revises: 20260316_s71
Create Date: 2026-03-16

"""
from typing import Sequence, Union

from alembic import op

revision: str = "20260316_seq"
down_revision: Union[str, Sequence[str], None] = "20260316_s71"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 将 sources.id 序列重置为当前表中最大 id，避免插入时主键冲突
    op.execute(
        "SELECT setval(pg_get_serial_sequence('sources', 'id'), COALESCE((SELECT MAX(id) FROM sources), 1));"
    )


def downgrade() -> None:
    pass  # 序列重置不可逆，无操作
