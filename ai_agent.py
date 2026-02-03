# ai_agent.py
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import config

# 1. 加载密钥
load_dotenv()

# 2. 初始化客户端
# DeepSeek 是国内服务，直接连，不需要任何代理设置！
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"), 
    base_url="https://api.deepseek.com"
)

def process_news_with_ai(title, snippet):
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
        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        # 打印简单报错，方便看一眼
        print(f"❌ AI 出错: {e}")
        # 如果出错，返回原文，保证程序不崩
        return {
            "title_zh": title, 
            "summary_zh": "AI 暂未生成摘要", 
            "discussion_point": ""
        }