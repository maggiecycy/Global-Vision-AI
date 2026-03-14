import httpx
import json
from app.core.config import settings
from typing import Dict

class AIService:
    @staticmethod
    async def analyze_article(title: str, summary: str) -> Dict:
        """调用 DeepSeek API 进行情绪和逻辑分析"""
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # 精心设计的 Prompt
        prompt = f"""
        你是一个冷静的新闻分析专家。请分析以下新闻：
        标题: {title}
        摘要: {summary}
        
        请输出 JSON 格式，包含：
        1. sentiment: (1-10分，1最悲观，10最乐观)
        2. category: (科技/全球/社会等)
        3. core_logic: (一句话总结其底层逻辑)
        """
        
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"}
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers=headers, timeout=30.0)
                result = response.json()
                return json.loads(result['choices'][0]['message']['content'])
            except Exception as e:
                print(f"❌ AI Analysis failed: {e}")
                return {"sentiment": 5, "category": "未知", "core_logic": "分析失败"}