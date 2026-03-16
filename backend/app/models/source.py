from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)

    # e.g. "en", "fr"
    language: Mapped[str] = mapped_column(String(8), nullable=False)

    # e.g. "科技", "商业"
    category: Mapped[str] = mapped_column(String(64), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Step 9: 容错管理，抓取失败 +1，成功则重置为 0
    failure_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    articles = relationship("Article", back_populates="source")

