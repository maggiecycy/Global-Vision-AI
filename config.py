# config.py

# 1. RSS 源配置 
RSS_URLS = {
    # The Guardian 对爬虫非常友好，且无需订阅即可读取全文 HTML
    "全球 (World)": "https://www.theguardian.com/world/rss",
    "美国 (U.S.)": "https://www.theguardian.com/us-news/rss",
    "商业 (Business)": "https://www.cnbc.com/id/10001147/device/rss/rss.html",  # CNBC 商业新闻完全免费
    "科技 (Tech)": "https://www.theguardian.com/technology/rss",  # 或者是 TechCrunch: https://techcrunch.com/feed/
    "科学 (Science)": "https://www.theguardian.com/science/rss",
    "健康 (Health)": "http://rss.cnn.com/rss/cnn_health.rss",  # CNN 健康板块也是免费的
    "体育 (Sports)": "https://www.theguardian.com/sport/rss",
    "艺术 (Arts)": "https://www.theguardian.com/artanddesign/rss",
    "时尚 (Fashion)": "https://www.theguardian.com/fashion/rss",
    "旅游 (Travel)": "https://www.theguardian.com/travel/rss",

    # --- 🇫🇷 法语源 (已替换为免费源) ---
    # Le Monde 是强付费墙，替换为 France Info (公立免费) 和其他垂直免费站
    "法·头条 (France Info)": "https://www.francetvinfo.fr/titres.rss",   # 替换了 Le Monde Une
    "法·科技 (Numerama)": "https://www.numerama.com/feed/",             # 替换了 Le Monde Pixels，Numerama 是法国顶级免费科技媒
    "法·极客 (J d Geek)": "https://www.journaldugeek.com/feed/",        # 保持不变，本来就免费
    "法·商业 (BFM Eco)": "https://www.bfmtv.com/rss/economie/",         # 保持不变，BFM 免费
    "法·国际 (France 24)": "https://www.france24.com/fr/rss",           # 保持不变，公立免费
    "法·文化 (20 Minutes)": "https://www.20minutes.fr/feeds/rss-culture.xml" # 保持不变，免费
}

# 2. 代理配置
# 如果以后 VPN 端口变了，只改这里就行
PROXIES = {
    "http": "http://127.0.0.1:15732", 
    "https": "http://127.0.0.1:15732"
}

# AI Prompt 模板
SYSTEM_PROMPT = """
你是一位拥有20年经验的国际新闻主编，擅长从复杂的全球新闻中提炼核心价值。
你的受众是具备高知背景的科技与文化爱好者，并且精通中英/中法翻译。

请处理用户输入的新闻数据，并严格按照以下 JSON 格式输出：
{
    "title_zh": "中文标题（要求：信达雅，吸引人但拒绝标题党）",
    "summary_zh": "中文摘要（要求：50-80字，直击要害，包含新闻背景或影响）",
    "keywords": ["关键词1", "关键词2", "关键词3"],
    "category_tag": "新闻分类标签（如：AI革命/地缘政治/经济风向）",
    "discussion_point": "一句话锐评或值得思考的问题（用于社交媒体分享或深度对话素材）"
    "french_learning": {
        "key_term": "原文中的核心法语单词（不要人名、地名或纯数字，除非极具代表性）",
        "meaning": "中文解释"
    }
}

注意：
1. 保持客观、专业、有洞察力的语调。
2. 必须返回纯粹的 JSON 格式，不要包含 Markdown 代码块标记（如 ```json）。
3. 【判断语言】：如果新闻内容是英语且与法国无关（如美国、全球板块），**绝对不要**输出 "french_learning" 字段（保持该字段为 null 或直接不返回）。
4. 【选词标准】：如果需要提取法语词，优先选择具有学习价值的**名词或动词**（如 "manifestation", "réforme"），避免仅仅提取数字，除非它们是理解新闻的关键。
"""