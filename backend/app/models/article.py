from datetime import datetime
from sqlalchemy import ARRAY, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class AIResult(Base):
    __tablename__ = "ai_results"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    article_id: Mapped[int] = mapped_column(
        ForeignKey("articles.id", ondelete="CASCADE"), 
        unique=True, 
        nullable=False
    )
    
    # 👈 核心：这个字段必须存在，且 nullable=False 对应数据库约束
    title_zh: Mapped[str] = mapped_column(String(512), nullable=False)
    summary_zh: Mapped[str] = mapped_column(Text, nullable=False)
    keywords: Mapped[list[str]] = mapped_column(ARRAY(String(64)), nullable=False)
    category_tag: Mapped[str] = mapped_column(String(100), nullable=False)
    discussion_point: Mapped[str] = mapped_column(Text, nullable=False, default="")
    sentiment_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    article: Mapped["Article"] = relationship("Article", back_populates="ai_result")

class Article(Base):
    __tablename__ = "articles"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # 👈 核心修复：添加 ForeignKey 关联 sources 表
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"), nullable=False, index=True)

    title_en: Mapped[str] = mapped_column(String(512), nullable=False)
    snippet: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str] = mapped_column(String(2048), nullable=False, unique=True, index=True)

    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    language: Mapped[str] = mapped_column(String(10), nullable=False, default="zh")

    ai_result: Mapped[AIResult] = relationship(
        AIResult, 
        back_populates="article", 
        uselist=False, 
        cascade="all, delete-orphan"
    )
    
    # 注意：这里需要确保你的 Source 模型里也有对应的 back_populates="articles"
    source: Mapped["Source"] = relationship("Source", back_populates="articles")