
---

```markdown
# 🌍 Global Vision: AI-Powered News Aggregator
> **A bilingual intelligence dashboard designed for Digital Nomads & French Learners (AI-driven).**

---

## 🏗️ System Architecture (Core Logic)

* **View Layer (`app.py`)** Streamlit-based interactive dashboard featuring dynamic sidebars, category filtering, and real-time news rendering (responsive UI).

* **Service Layer (`ai_agent.py`)** Integrated with LLM (DeepSeek/OpenAI) to perform context-aware summarization, "clickbait" filtering, and linguistic extraction (French-Chinese mapping).

* **Data Layer (`data_fetcher.py`, `config.py`)** Handles RSS stream ingestion, anti-crawler strategy implementation (User-Agent spoofing), and modular source configuration.

---

## 🌟 Project Motivation / 项目动机

### English
In an era of algorithmic feeds and information overload, it is difficult to find high-quality, objective news sources, especially for those trying to master a second language (e.g., French). Traditional news aggregators focus on "engagement" rather than "value."

This project was developed as an **"Information Filter."** By combining **Generative AI** with curated RSS feeds, it empowers users to reclaim control over their information diet. It bridges the gap between **Tech Insights** and **Language Acquisition**, allowing users to learn French vocabulary in the context of real-world technology and business news.

### 中文
在算法推荐和信息过载的时代，获取高质量、客观的新闻变得愈发困难。传统聚合器往往关注“点击率”而非“信息价值”。

本项目旨在构建一个**“智能信息过滤器”**。通过结合 **生成式 AI** 与精选 RSS 源，它帮助用户重夺信息主动权。本项目打破了**科技视野**与**语言习得**之间的壁垒，让用户能够在真实的科技与商业新闻语境中，沉浸式地积累全球视野。

---

## 🏗️ Technical Architecture / 技术架构

The project follows a modular design pattern emphasizing **Stability & Extensibility**:

* **Anti-Crawler Mechanism (`data_fetcher.py`)** Implements custom headers and session handling to bypass strict anti-scraping measures from top-tier media (e.g., *Les Echos*, *HuffPost*).

* **Prompt Engineering (`config.py`)** Uses structured System Prompts to enforce JSON output, ensuring strict data formatting for downstream UI rendering.

* **State Management** Streamlit session state is optimized to reduce redundant API calls during user interaction.

---

## ✨ Key Features / 功能说明

* **AI-Driven Summarization** Compresses lengthy articles into 50-80 word core insights, removing noise and fluff.

* **Contextual French Learning (Mot du Jour)** Automatically identifies key French terms (nouns/verbs) from the news context and provides definitions.

* **Dual-Track Tech News** Segregates content into "Hard Tech" (*Journal du Geek*) and "Digital Culture" (*Le Monde Pixels*) for targeted reading.

* **Privacy-First Design** No local database required; all processing happens in-memory with secure API key management via Streamlit Secrets.

---

## 🚀 Quick Start / 快速启动指南

### 1. Installation / 安装

```bash
git clone [https://github.com/maggiecycy/Global-Vision-AI.git](https://github.com/maggiecycy/Global-Vision-AI.git)
cd Global-Vision-AI
pip install -r requirements.txt

```

### 2. Configuration / 配置

Create `.env` (local) or `.streamlit/secrets.toml` (production):

```toml
# API Configuration
API_KEY = "your_llm_api_key"
BASE_URL = "[https://api.deepseek.com](https://api.deepseek.com)"

```

### 3. Run / 运行

```bash
streamlit run app.py

```

---

## 🧭 Roadmap / 未来规划

* **User Mood Tracking** Recommend news based on the user's current emotional state (integrating logic from *Mood Journal*).
* **Anki Integration** One-click export of "Mot du Jour" vocabulary to Anki flashcards.
* **Multi-Language Support** Expanding to German and Italian sources (EU-oriented).

---

## 🧑‍💻 Author

**Maggie Cao**

* Computer Science @ Beijing Technology and Business University
* ISTJ | CS Student & Aspiring AI Developer

**Focus Areas**

* **Full-Stack AI Application** (Streamlit + LLM)
* **Cross-Cultural Tech** & Language Learning Tools
* **System Architecture** & Data Engineering

---

## 🛡️ License

MIT License

```

```