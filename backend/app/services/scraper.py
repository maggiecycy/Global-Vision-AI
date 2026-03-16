import os
import httpx
import feedparser
from typing import List, Dict

# 伪装为 Chrome 120+，避免卫报识别为 Python 请求
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
DEFAULT_TIMEOUT = 20.0  # 跨国访问统一 20 秒


def _get_proxy() -> str | None:
    """显式读取 http_proxy 并供 httpx 透传（卫报跨国访问/反爬）。"""
    return os.getenv("http_proxy") or os.getenv("HTTP_PROXY")


class ScraperService:
    @staticmethod
    def fetch_rss_articles(url: str, limit: int = 5) -> List[Dict]:
        """抓取并解析 RSS 源（User-Agent 伪装 + 20s 超时 + 代理透传）"""
        try:
            headers = {"User-Agent": USER_AGENT}
            proxy = _get_proxy()
            response = httpx.get(
                url,
                headers=headers,
                timeout=DEFAULT_TIMEOUT,
                proxy=proxy,
                follow_redirects=True,
            )
            feed = feedparser.parse(response.text)
            
            articles = []
            for entry in feed.entries[:limit]:
                articles.append({
                    "title": entry.title,
                    "link": entry.link,
                    "summary": entry.get("summary", ""),
                    "published_at": entry.get("published", "")
                })
            return articles
        except Exception as e:
            print(f"❌ Scraping failed for {url}: {e}")
            return []