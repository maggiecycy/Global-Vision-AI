# ai_agent.py
import os
import json
from typing import Any, List, Optional

from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field
import config

# 1. 加载密钥
load_dotenv()

# --- Pydantic schema: enforce stable output to UI ---
class FrenchLearning(BaseModel):
    model_config = ConfigDict(extra="ignore")

    key_term: str = Field(default="", description="原文中的核心法语单词")
    meaning: str = Field(default="", description="中文解释")


class AIResult(BaseModel):
    """
    Keep field names aligned with `config.SYSTEM_PROMPT` and `app.py`.
    Even if LLM omits fields, defaults will prevent KeyError in the UI.
    """

    model_config = ConfigDict(extra="ignore")

    title_zh: str = Field(default="AI 暂未生成标题", description="中文标题")
    summary_zh: str = Field(default="AI 暂未生成摘要", description="中文摘要")
    keywords: List[str] = Field(default_factory=list, description="关键词列表")
    category_tag: str = Field(default="", description="新闻分类标签")
    discussion_point: str = Field(default="", description="讨论点/锐评")
    french_learning: Optional[FrenchLearning] = Field(default=None, description="可选法语学习字段")


def _safe_fallback(title: str, summary: str = "AI 暂未生成摘要") -> dict:
    return AIResult(title_zh=title, summary_zh=summary).model_dump()


# 2. 初始化客户端
# DeepSeek 是国内服务，直接连，不需要任何代理设置！
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"), 
    base_url="https://api.deepseek.com"
)

def process_news_with_ai(title: str, snippet: str) -> dict:
    """
    最基础的 AI 处理函数
    """
    try:
        # 3. 发送请求
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": config.SYSTEM_PROMPT},
                # 直接发送，不搞那些清洗，相信 AI 的解析能力
                {"role": "user", "content": f"Title: {title}\nSnippet: {snippet}"}
            ],
            response_format={"type": "json_object"},
            stream=False
        )
        
        # 4. 解析结果
        content = response.choices[0].message.content or "{}"

        # 强制校验/补全字段：彻底杜绝 UI 侧 KeyError
        validated = AIResult.model_validate_json(content)
        return validated.model_dump()

    except Exception as e:
        # 打印简单报错，方便看一眼
        print(f"❌ AI 出错或格式校验失败: {e}")
        # 如果出错，返回带默认值的安全结构，保证前端永远可渲染
        return _safe_fallback(title=title)