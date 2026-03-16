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
        
        # 强制 JSON 结构，字段名与 tasks 保存逻辑一致
        prompt = f"""
你是一个冷静的新闻分析专家。请分析以下新闻并**仅**输出合法 JSON，不要包含任何其他文字。

标题: {title}
摘要: {summary}

必须包含且仅包含以下五个字段（字段名不可改）：
1. "sentiment_score": 浮点数 1.0-10.0，1 最悲观，10 最乐观
2. "category": 字符串，从【科技、全球、社会、财经、开源、安全、政策、其他】中选最贴切的一项，不要总选「科技」
3. "core_logic": 字符串，一句话总结该新闻的底层逻辑或要点
4. "keywords": 字符串数组，提取该新闻的 5 个核心关键词（技术名、产品名、主题等），如 ["AI", "大模型", "开源"]

示例格式：{{"sentiment_score": 6.5, "category": "开源", "core_logic": "某项目发布新版本...", "keywords": ["AI", "开源", "大模型", "LLM", "DeepSeek"]}}
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
                return {"sentiment_score": 5.0, "category": "未知", "core_logic": "分析失败", "keywords": ["未分类"]}