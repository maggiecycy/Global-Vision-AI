import os
from dotenv import load_dotenv
from pydantic import BaseModel

# 显式加载 .env 文件
load_dotenv()

class Settings(BaseModel):
    # 数据库配置
    database_url: str = os.getenv("DATABASE_URL", "")
    
    # AI 模型配置 (新增)
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    
    # 以后如果你有其他密钥，也在这里添加
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASS: str = os.getenv("SMTP_PASS", "")
    SMTP_USE_TLS: bool = os.getenv("SMTP_USE_TLS", "true").lower() in {"1", "true", "yes", "y"}

    RECEIVER_EMAIL: str = os.getenv("RECEIVER_EMAIL", "")

    # Resend（HF 封 587，用 HTTP API 替代 SMTP）
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY", "")
    RESEND_FROM: str = os.getenv("RESEND_FROM", "")  # 如 "Global Vision <onboarding@resend.dev>"


# --- Final Source Update: 黄金清单 RSS 源 ---
RSS_SOURCES = [
    # --- 🇬🇧 The Guardian (English - 极简/高质量) ---
    {"name": "The Guardian", "url": "https://www.theguardian.com/world/rss", "language": "en", "category": "World"},
    {"name": "The Guardian", "url": "https://www.theguardian.com/us-news/rss", "language": "en", "category": "U.S."},
    {"name": "The Guardian", "url": "https://www.theguardian.com/technology/rss", "language": "en", "category": "Tech"},
    {"name": "The Guardian", "url": "https://www.theguardian.com/science/rss", "language": "en", "category": "Science"},
    {"name": "The Guardian", "url": "https://www.theguardian.com/sport/rss", "language": "en", "category": "Sports"},
    {"name": "The Guardian", "url": "https://www.theguardian.com/fashion/rss", "language": "en", "category": "Fashion"},
    {"name": "The Guardian", "url": "https://www.theguardian.com/travel/rss", "language": "en", "category": "Travel"},

    # --- 🇫🇷 French Sources (法语进修 - 免费/精准) ---
    {"name": "France Info", "url": "https://www.francetvinfo.fr/titres.rss", "language": "fr", "category": "World"},
    {"name": "Numerama", "url": "https://www.numerama.com/feed/", "language": "fr", "category": "Tech"},
    {"name": "France 24", "url": "https://www.france24.com/fr/rss", "language": "fr", "category": "World"},
    {"name": "BFM Business", "url": "https://www.bfmtv.com/rss/economie/", "language": "fr", "category": "Business"},
    {"name": "Journal du Geek", "url": "https://www.journaldugeek.com/feed/", "language": "fr", "category": "Tech"},
    {"name": "20 Minutes", "url": "https://www.20minutes.fr/feeds/rss-culture.xml", "language": "fr", "category": "Arts"},
]

settings = Settings()
