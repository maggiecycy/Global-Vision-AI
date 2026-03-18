# 🌍 Global Vision AI: Full-Stack Intelligence Aggregator

> **A Production-Grade Distributed System for Digital Nomads & Language Learners.**
> **由 AI 驱动的全栈新闻情报系统，专为全球游民与跨语言学习者设计。**

[![Vercel Deployment](https://img.shields.io/badge/Frontend-Vercel-black?logo=vercel)](https://global-vision-ai.vercel.app/)
[![Hugging Face Space](https://img.shields.io/badge/Backend-Hugging_Face-ffbd45?logo=huggingface)](https://huggingface.co/spaces/maggiecycy/Global-Vision-Backend)
[![Database](https://img.shields.io/badge/Database-Supabase-3ec98e?logo=supabase)](https://supabase.com/)

---

## 🏗️ 系统架构 / System Architecture

本项目采用**四层分布式架构**，实现了高性能的异步任务处理与数据持久化：

* **Frontend (Next.js 14)**: 响应式仪表盘，利用 Tailwind CSS 和 Recharts 实现动态词云与精报统计看板。
* **Backend (FastAPI)**: 异步路由服务。通过 **Supervisord** 在云端同时驱动 Web 服务、Redis 与并行爬虫。
* **Task Queue (Celery + Redis)**: 实现定时抓取、AI 总结与邮件推送的异步解耦，确保系统高可用。
* **Persistence (PostgreSQL/Supabase)**: 结构化数据存储，通过 **Alembic** 管理数据库迁移版本。

---

## 🌟 项目动机 / Project Motivation

### English
In an era of information overload, high-quality news is often buried under noise. This project bridges the gap between **Tech Insights** and **Language Acquisition**, allowing users to consume real-world French news through an AI-powered lens.

### 中文
在信息碎片化的时代，高质量情报常被噪音淹没。本项目打破了**科技视野**与**语言习得**之间的壁垒，利用生成式 AI 帮助用户在真实的法语新闻语境中沉浸式积累全球视野。

---

## ✨ 核心功能 / Key Features

* **AI-Driven Insights**: 自动对《卫报》等媒体进行深度摘要，精准去除点击诱饵。
* **Mot du Jour**: 自动从新闻背景中识别法语核心词汇，并提供双语对照解释。
* **Distributed Scheduling**: 每天定时执行抓取，并通过邮件推送全天情报摘要。
* **Heartbeat Mechanism**: 通过 GitHub Actions 实现“起搏器”逻辑，确保云端服务永不掉线。

---

## 🛠️ 技术栈 / Tech Stack

| 类别 | 技术 |
| :--- | :--- |
| **前端** | Next.js, TypeScript, Tailwind CSS, Recharts |
| **后端** | FastAPI, Python 3.11, Pydantic |
| **异步/任务** | Celery, Redis, Supervisord |
| **数据库** | PostgreSQL (Supabase), SQLAlchemy, Alembic |
| **基础设施** | Vercel, Hugging Face, Docker, GitHub Actions |

---

## 🚀 快速启动 / Quick Start

```bash
# 克隆项目
git clone [https://github.com/maggiecycy/Global-Vision-AI.git](https://github.com/maggiecycy/Global-Vision-AI.git)

# 安装依赖 (后端)
cd backend && pip install -r requirements.txt

# 启动前端
cd ../frontend && npm install && npm run dev