import httpx
import feedparser
from typing import List, Dict

class ScraperService:
    @staticmethod
    def fetch_rss_articles(url: str, limit: int = 5) -> List[Dict]:
        """抓取并解析 RSS 源"""
        try:
            # 这里的 headers 是为了防止被反爬
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
            response = httpx.get(url, headers=headers, timeout=10.0)
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