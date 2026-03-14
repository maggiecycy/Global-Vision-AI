from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AIResult(Base):
    __tablename__ = "ai_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    article_id: Mapped[int] = mapped_column(
        ForeignKey("articles.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    title_zh: Mapped[str] = mapped_column(String(512), nullable=False)
    summary_zh: Mapped[str] = mapped_column(Text, nullable=False)

    # PostgreSQL native array is convenient for tags/keywords.
    keywords: Mapped[list[str]] = mapped_column(ARRAY(String(64)), nullable=False, default=list)

    category_tag: Mapped[str] = mapped_column(String(128), nullable=False, default="", index=True)
    discussion_point: Mapped[str] = mapped_column(Text, nullable=False, default="")

    french_key_term: Mapped[str | None] = mapped_column(String(128), nullable=True)
    french_meaning: Mapped[str | None] = mapped_column(String(256), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    article = relationship("Article", back_populates="ai_result")

