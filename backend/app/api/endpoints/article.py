from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
# 👈 核心修复：从模型文件中同时导入 Article 和 AIResult
from app.models.article import Article, AIResult 
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
    # 确保 source 已加载，供 ArticleResponse 序列化
    _ = article.source
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
        .options(joinedload(Article.ai_result), joinedload(Article.source))
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
    article = (
        db.query(Article)
        .options(joinedload(Article.ai_result), joinedload(Article.source))
        .filter(Article.id == article_id)
        .first()
    )
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    return article


@router.delete("/clear-all", status_code=status.HTTP_204_NO_CONTENT)
def clear_all_articles(db: Session = Depends(get_db)):
    """
    一键清空：先删子表 (AIResult)，再删主表 (Article)。
    """
    try:
        # 👈 核心修复：直接使用导入的模型名
        # 必须先删除有外键关联的 AIResult 记录
        db.query(AIResult).delete() 
        db.query(Article).delete()
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        # 在后端终端打印具体的报错，方便排查
        print(f"CLEANUP ERROR: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database wipe failed: {str(e)}"
        )