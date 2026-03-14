import os
from dotenv import load_dotenv
from pydantic import BaseModel

# 显式加载 .env 文件
load_dotenv()

class Settings(BaseModel):
    # 数据库配置
    database_url: str = os.getenv("DATABASE_URL", "")
    
    # AI 模型配置 (新增)
    # 这里的名字必须和你在 ai_service.py 里调用的名字一模一样
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    
    # 以后如果你有其他密钥（比如 OpenAI 或 数据库密码），也在这里添加

settings = Settings()