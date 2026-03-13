"""
Import all models here so Alembic can discover them via metadata.
"""

from app.db.base import Base  # noqa: F401
from app.models import AIResult, Article, Source  # noqa: F401

