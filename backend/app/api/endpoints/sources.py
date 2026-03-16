"""Step 9: 新闻源健康检查接口（与抓取一致：20s 超时 + User-Agent + 代理）"""
import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Source
from app.core.config import RSS_SOURCES
from app.services.scraper import USER_AGENT, DEFAULT_TIMEOUT, _get_proxy

router = APIRouter()


@router.get("/status")
def get_sources_status(db: Session = Depends(get_db)):
    """
    返回所有新闻源的连通性健康状态。
    使用与抓取相同的超时、User-Agent 与代理透传。
    """
    db_sources = {s.url: s for s in db.query(Source).all()}

    results = []
    for config in RSS_SOURCES:
        name = config["name"]
        url = config["url"]
        db_src = db_sources.get(url)
        failure_count = db_src.failure_count if db_src else 0

        ok = False
        try:
            with httpx.Client(
                timeout=DEFAULT_TIMEOUT,
                headers={"User-Agent": USER_AGENT},
                proxy=_get_proxy(),
                follow_redirects=True,
            ) as client:
                resp = client.get(url)
                ok = 200 <= resp.status_code < 400
        except Exception:
            ok = False

        results.append({
            "name": name,
            "url": url,
            "status": "ok" if ok else "fail",
            "failure_count": failure_count,
        })

    return {"sources": results}
