# data_fetcher.py
import feedparser
import requests
import config

def fetch_rss_data(category, limit=5): # 🟢 新增 limit 参数，默认5
    """
    负责联网抓取数据，支持自定义数量
    """
    url = config.RSS_URLS.get(category)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        print(f"🕷️ 正在抓取: {category} ...")
        # 记得这里我们用了 config.PROXIES，如果你之前删了代理配置，记得改回 proxies=None
        response = requests.get(url, headers=headers, proxies=config.PROXIES, timeout=10)
        
        feed = feedparser.parse(response.text)
        return feed.entries[:limit] # 🟢 使用 limit 截取
        
    except Exception as e:
        print(f"❌ 网络请求失败: {e}")
        return []