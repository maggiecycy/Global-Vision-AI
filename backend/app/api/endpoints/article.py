from typing import List
from collections import Counter
import re
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
# 👈 核心修复：从模型文件中同时导入 Article 和 AIResult
from app.models.article import Article, AIResult 
from app.schemas.article import ArticleCreate, ArticleResponse

router = APIRouter()

_WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9][A-Za-zÀ-ÖØ-öø-ÿ0-9\-']{1,}")
_CJK_RE = re.compile(r"[\u4e00-\u9fff]{2,}")
_URL_RE = re.compile(r"https?://\\S+")
_JUNK_TOKENS = {
    # domain / html / rss noise
    "https", "http", "com", "www", "href", "html", "images", "browser", "theguardian",
    "theguardiancom", "amp", "rss", "feed",
}
_STOPWORDS = {
    # EN common
    "about", "after", "again", "against", "all", "also", "am", "among", "an", "and", "any", "are", "as", "at",
    "be", "been", "before", "being", "between", "both", "but", "by",
    "can", "could",
    "did", "do", "does", "doing", "down", "during",
    "each", "even", "ever",
    "for", "from", "further",
    "had", "has", "have", "having", "he", "her", "here", "hers", "him", "his", "how",
    "i", "if", "in", "into", "is", "it", "its",
    "just",
    "may", "me", "more", "most", "my",
    "no", "nor", "not", "now",
    "of", "off", "on", "once", "only", "or", "other", "our", "out", "over",
    "same", "she", "should", "so", "some", "such",
    "than", "that", "the", "their", "them", "then", "there", "these", "they", "this", "those", "through", "to", "too",
    "under", "until", "up",
    "very",
    "was", "we", "were", "what", "when", "where", "which", "who", "why", "will", "with", "would",
    "you", "your",
    # FR common
    "avec", "pour", "dans", "sur", "chez", "comme", "plus", "moins", "tres", "très", "tout", "toute", "tous",
    "une", "un", "des", "du", "de", "la", "le", "les", "et", "ou", "mais", "donc", "or", "ni", "car",
    "ce", "cet", "cette", "ces", "son", "sa", "ses", "leur", "leurs",
    "est", "sont", "été", "etre", "être", "avoir",
    # CN minimal stop
    "我们", "你们", "他们", "她们", "以及", "但是", "因为", "所以", "如果", "一个", "一些", "这个", "那个", "这些", "那些", "正在", "已经",
}


def _tokenize_mixed(text: str) -> list[str]:
    """
    非依赖版混合分词（英/法/中）：
    - 拉丁字母/数字：提取长度>=2 的 token，统一小写
    - 中文：提取连续 CJK 串后做 2-gram（长度>=2），覆盖常见词语片段
    """
    if not text:
        return []

    # Remove URLs early to avoid domain garbage
    text = _URL_RE.sub(" ", text)

    tokens: list[str] = []
    tokens += [m.group(0).lower() for m in _WORD_RE.finditer(text)]

    for m in _CJK_RE.finditer(text):
        s = m.group(0)
        if len(s) == 2:
            tokens.append(s)
        else:
            for i in range(len(s) - 1):
                tokens.append(s[i : i + 2])
    return tokens


def _is_meaningful_token(t: str) -> bool:
    if not t:
        return False
    t2 = t.strip().lower()
    if not t2 or t2 in _JUNK_TOKENS or t2 in _STOPWORDS:
        return False
    # numeric-only or contains digits heavily (e.g., 2026, 16)
    if t2.isdigit():
        return False
    if any(ch.isdigit() for ch in t2) and len(t2) <= 4:
        return False
    # ultra short latin noise
    if len(t2) <= 2 and re.fullmatch(r"[a-z]{1,2}", t2):
        return False
    # hex-ish / color-ish noise like 'red' is ambiguous; keep if long enough unless in junk list
    return True


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
    limit: int = 50,
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


@router.get("/keywords")
def list_keywords(db: Session = Depends(get_db)) -> list[dict]:
    """
    提取过去 24 小时内标题/摘要的高频关键词（混合英法中）。
    返回格式：[{text: \"Quantum\", value: 10}, ...]
    """
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    # 优先：AIResult.keywords（更接近 key entities / 名词短语）
    ai_rows = (
        db.query(AIResult.keywords)
        .join(Article, Article.id == AIResult.article_id)
        .filter(Article.created_at >= cutoff)
        .all()
    )
    # 兜底：title/snippet 轻量分词
    text_rows = (
        db.query(Article.title_en, Article.snippet)
        .filter(Article.created_at >= cutoff)
        .all()
    )

    counter: Counter[str] = Counter()
    for (kw_list,) in ai_rows:
        if not kw_list:
            continue
        for kw in kw_list:
            t = str(kw).strip()
            if not t:
                continue
            # AI keywords 给予更高权重（更接近实体/名词）
            if _is_meaningful_token(t):
                counter[t] += 4

    for title, snippet in text_rows:
        text = f"{title or ''} {snippet or ''}"
        for t in _tokenize_mixed(text):
            if not _is_meaningful_token(t):
                continue
            counter[t] += 1

    top = counter.most_common(20)
    return [{"text": k, "value": v} for k, v in top]


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