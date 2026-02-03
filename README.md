好的，Maggie！为了让你的 GitHub 项目看起来更加国际化，同时方便中文招聘者（或者你自己复习）快速理解，我把这份 **README.md** 升级为了 **中英双语版 (Bilingual Version)**。

这种格式在 GitHub 上非常受欢迎，既展示了你的英语能力，又体现了对不同受众的体贴。

你可以直接复制下面的内容覆盖你现在的 `README.md`。

---

```markdown
# 🌍 Global Vision: AI-Powered News Aggregator | AI 驱动的双语新闻聚合助手

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)
![AI](https://img.shields.io/badge/AI-Powered-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

> **"Stay informed, learn French, and escape the algorithm."**
> **“拒绝算法喂养，在获取资讯的同时，沉浸式掌握第二外语。”**

**Global Vision** is a personalized news dashboard built with Python and Streamlit. Unlike traditional aggregators, it uses **Generative AI** to read, summarize, and extract value from global RSS feeds, filtering out clickbait and noise.
**Global Vision** 是一个基于 Python 和 Streamlit 构建的个性化新闻看板。与传统聚合器不同，它利用**生成式 AI** 实时读取、总结全球主流媒体的 RSS 信息流，自动过滤标题党和无效信息，提炼核心价值。

This project was specifically designed to bridge the gap between **Tech Insights** and **French Language Learning**, making it the perfect tool for digital nomads and global citizens.
本项目专为**科技爱好者**和**法语学习者**设计，旨在打破信息获取与语言学习之间的壁垒，是“数字游民”和“世界公民”的理想工具。

---

## 📸 App Preview | 应用预览

![Dashboard Screenshot](preview.jpg)

---

## ✨ Key Features | 核心功能

### 🤖 1. AI-Driven Intelligence (AI 智能情报分析)
- **Smart Summarization**: Compresses lengthy articles into 50-80 word core insights using LLM.
  - **智能摘要**：利用大模型将长篇大论压缩为 50-80 字的硬核干货。
- **Contextual Analysis**: AI generates "Discussion Points" to spark critical thinking.
  - **深度洞察**：AI 生成“问题切入点”，激发批判性思维，拒绝被动阅读。
- **Tagging System**: Automatically categorizes news (e.g., #AIRevolution, #Geopolitics).
  - **自动标签**：自动提取新闻分类与核心关键词。

### 🇫🇷 2. Immersive French Learning (沉浸式法语学习)
- **Dual-Track Tech News (双轨制科技阅读)**:
  - *Le Monde Pixels* for digital culture & ethics (数字人文与伦理).
  - *Journal du Geek* for consumer tech & trends (消费电子与前沿趋势).
- **"Mot du Jour" (Word of the Day / 每日一词)**: 
  - The AI automatically identifies key French terms (nouns/verbs) from the news context and provides definitions, turning reading into a learning session.
  - **语境单词提取**：AI 自动识别新闻中的核心法语术语（优先名词/动词），并生成中文解释，实现“在读新闻中背单词”。

### 🛡️ 3. Robust Engineering (硬核工程实现)
- **Anti-Crawler Bypass**: Implements custom `User-Agent` headers and session handling to successfully fetch data from strict media sources (e.g., *Les Echos*, *HuffPost*).
  - **反爬虫突破**：通过自定义请求头伪装和会话管理，成功抓取 *Les Echos* 等高防护媒体源的数据。
- **Dynamic Configuration**: Modular design allows easy addition of new RSS sources via `config.py`.
  - **动态配置**：模块化设计，只需修改配置文件即可一键添加新的 RSS 数据源。

---

## 🛠️ Tech Stack | 技术栈

- **Frontend**: [Streamlit](https://streamlit.io/) (Interactive UI / 交互式前端)
- **Backend**: Python 3.x
- **Data Fetching**: `feedparser`, `requests` (Handling Anti-scraping / 处理反爬策略)
- **AI Integration**: OpenAI / DeepSeek API (Prompt Engineering / 提示词工程)
- **Version Control**: Git & GitHub

---

## 🚀 Quick Start | 快速开始

### Prerequisites (前置要求)
- Python 3.8+
- An API Key (OpenAI compatible)

### Installation (安装步骤)

1. **Clone the repository (克隆仓库)**
   ```bash
   git clone [https://github.com/maggiecycy/Global-Vision-AI.git](https://github.com/maggiecycy/Global-Vision-AI.git)
   cd Global-Vision-AI

```

2. **Install dependencies (安装依赖)**
```bash
pip install -r requirements.txt

```


3. **Configure Environment (配置环境)**
Create a `.env` file in the root directory to keep your keys safe:
在根目录新建 `.env` 文件以保护你的密钥安全：
```env
# .env
API_KEY=your_api_key_here
BASE_URL=your_api_base_url

```


4. **Run the App (运行应用)**
```bash
streamlit run app.py

```



---

## 📂 Project Structure | 项目结构

```text
Global-Vision-AI/
├── app.py              # Main application entry point (前端 UI 逻辑)
├── data_fetcher.py     # RSS fetching & Anti-crawler (爬虫与反爬处理)
├── ai_agent.py         # AI processing & Prompt Engineering (AI 智能体)
├── config.py           # Configuration (RSS源与系统提示词配置)
├── requirements.txt    # Python dependencies (依赖列表)
└── README.md           # Documentation (项目文档)

```

## 🔮 Future Roadmap | 未来规划

* [ ] **User Mood Tracking**: Recommend news based on the user's current emotional state. (基于情绪的新闻推荐)
* [ ] **Anki Integration**: One-click export of "Mot du Jour" to Anki flashcards. (一键导出单词到 Anki)
* [ ] **Multi-Language Support**: Expanding to German and Italian sources. (扩展德语和意大利语源)

## 👩‍💻 Author | 作者

**Maggie (Cao Yan)**
*CS Major | Aspiring Global Citizen*
*计算机专业大二学生 | 准数字游民*

---

*Built with ❤️, Python, and a lot of coffee.*

```

---