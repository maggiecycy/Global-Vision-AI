from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleResponse

router = APIRouter()


@router.post(
    "/",
    response_model=ArticleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_article(payload: ArticleCreate, db: Session = Depends(get_db)) -> Article:
    article = Article(
        source_id=payload.source_id,
        title_en=payload.title_en,
        snippet=payload.snippet,
        url=str(payload.url),
        published_at=payload.published_at,
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


@router.get(
    "/",
    response_model=List[ArticleResponse],
)
def list_articles(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
) -> list[Article]:
    queryset = (
        db.query(Article)
        .order_by(Article.published_at.desc().nullslast(), Article.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return queryset


@router.get(
    "/{article_id}",
    response_model=ArticleResponse,
)
def get_article(article_id: int, db: Session = Depends(get_db)) -> Article:
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    return article

