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


# --- Step 11: 卫报专用精准看板 - 仅卫报频道 ---
RSS_SOURCES = [
    {"name": "The Guardian", "category": "World", "url": "https://www.theguardian.com/world/rss", "language": "en"},
    {"name": "The Guardian", "category": "Politics", "url": "https://www.theguardian.com/politics/rss", "language": "en"},
    {"name": "The Guardian", "category": "Technology", "url": "https://www.theguardian.com/technology/rss", "language": "en"},
    {"name": "The Guardian", "category": "Science", "url": "https://www.theguardian.com/science/rss", "language": "en"},
    {"name": "The Guardian", "category": "Environment", "url": "https://www.theguardian.com/environment/rss", "language": "en"},
    {"name": "The Guardian", "category": "Football", "url": "https://www.theguardian.com/football/rss", "language": "en"},
]

settings = Settings()
