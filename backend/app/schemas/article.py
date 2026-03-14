from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, HttpUrl


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

    model_config = ConfigDict(from_attributes=True)

