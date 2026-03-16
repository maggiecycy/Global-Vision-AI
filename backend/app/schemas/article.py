from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, HttpUrl


class SourceBase(BaseModel):
    """来源信息，用于前端展示、来源分布图与国旗展示"""
    id: int
    name: str
    language: str

    model_config = ConfigDict(from_attributes=True)


class AIResultBase(BaseModel):
    summary_zh: str
    category_tag: str
    keywords: list[str] = []
    sentiment_score: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class ArticleBase(BaseModel):
    source_id: int
    title_en: str
    snippet: str
    url: HttpUrl
    published_at: Optional[datetime] = None


class ArticleCreate(ArticleBase):
    """Payload used when creating an Article."""


class ArticleResponse(ArticleBase):
    id: int
    created_at: datetime
    language: str = "zh"
    ai_result: Optional[AIResultBase] = None
    source: Optional[SourceBase] = None

    model_config = ConfigDict(from_attributes=True)
