import time
import asyncio
import random
from datetime import datetime, timedelta, timezone
from app.core.celery_app import celery_app
from app.core.config import RSS_SOURCES
from app.db.session import SessionLocal
from app.models import Article, AIResult, Source
from app.services.scraper import ScraperService
from app.services.ai_service import AIService
from app.services.email_service import send_brief_email
from app.core.config import settings
from sqlalchemy.orm import joinedload

# --- 诊断工具 ---
@celery_app.task(name="app.worker.tasks.ping_task")
def ping_task() -> str:
    return "pong"

@celery_app.task(name="app.worker.tasks.mock_scrape_task")
def mock_scrape_task(limit: int) -> str:
    time.sleep(3)
    return f"mock scrape finished with limit={limit}"


def _get_or_create_source(db, rss_config: dict) -> Source:
    """根据 RSS 配置获取或创建 Source 记录。"""
    url = rss_config["url"]
    source = db.query(Source).filter(Source.url == url).first()
    if source:
        return source
    source = Source(
        name=rss_config["name"],
        url=url,
        language=rss_config["language"],
        category=rss_config["category"],
        is_active=True,
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


# Step 10: failure_count 超过此值则跳过该源，避免反复请求无法抓取的源
SKIP_SOURCE_FAILURE_THRESHOLD = 3


# --- Step 11: 卫报专用 - 只遍历勾选分类，每频道固定 1 条 ---
def _run_scrape(db, selected_categories: list | None = None):
    processed_count = 0
    skipped_count = 0
    limit_per_source = 1  # 卫报精准看板：每频道只抓最新 1 条
    sources_to_scrape = RSS_SOURCES
    if selected_categories:
        cat_set = set(selected_categories)
        sources_to_scrape = [c for c in RSS_SOURCES if c.get("category") in cat_set]
    if not sources_to_scrape:
        return "⚠️ 请至少勾选一个卫报频道（World / Politics / Technology / Science / Environment / Football）。"

    for idx, rss_config in enumerate(sources_to_scrape):
        if not rss_config.get("is_active", True):
            continue
        source = _get_or_create_source(db, rss_config)
        if (source.failure_count or 0) >= SKIP_SOURCE_FAILURE_THRESHOLD:
            print(f"⏭️ 跳过 {rss_config['name']}（failure_count={source.failure_count} >= {SKIP_SOURCE_FAILURE_THRESHOLD}）")
            continue
        rss_url = rss_config["url"]
        lang = rss_config["language"]

        try:
            articles = ScraperService.fetch_rss_articles(rss_url, limit_per_source)
        except Exception as fetch_err:
            source.failure_count = (source.failure_count or 0) + 1
            db.commit()
            print(f"⚠️ {rss_config['name']} 抓取异常: {fetch_err}，failure_count={source.failure_count}")
            continue

        if not articles:
            source.failure_count = (source.failure_count or 0) + 1
            db.commit()
            print(f"⚠️ {rss_config['name']} 未返回条目，failure_count={source.failure_count}")
            continue

        source.failure_count = 0
        db.commit()

        for item in articles:
            existing = db.query(Article).filter(Article.url == item['link']).first()
            if existing:
                skipped_count += 1
                continue

            new_article = Article(
                source_id=source.id,
                title_en=item['title'],
                snippet=item['summary'],
                url=item['link'],
                language=lang,
            )
            db.add(new_article)
            db.commit()
            db.refresh(new_article)

            try:
                print(f"🧠 Processing [{new_article.title_en}]...")
                analysis = asyncio.run(AIService.analyze_article(new_article.title_en, new_article.snippet))
                category_raw = analysis.get('category') or ''
                category_tag = (category_raw.strip() or '未分类') if isinstance(category_raw, str) else '未分类'
                core_logic = analysis.get('core_logic') or '分析完成'
                # Step 9: AI 返回 5 个核心关键词，兼容旧格式
                kw_raw = analysis.get('keywords')
                if isinstance(kw_raw, list):
                    keywords_list = [str(x).strip() for x in kw_raw[:5] if x]
                else:
                    keywords_list = [category_tag]
                if not keywords_list:
                    keywords_list = [category_tag]
                raw_sent = analysis.get('sentiment_score') or analysis.get('sentiment')
                sentiment_score = None
                try:
                    if raw_sent is not None:
                        v = float(raw_sent)
                        sentiment_score = v if 1 <= v <= 10 else 5.0
                except (TypeError, ValueError):
                    sentiment_score = 5.0

                ai_res = AIResult(
                    article_id=new_article.id,
                    title_zh=new_article.title_en,
                    summary_zh=core_logic,
                    keywords=keywords_list,
                    category_tag=category_tag,
                    sentiment_score=sentiment_score,
                )
                db.add(ai_res)
                db.commit()
                processed_count += 1
                print(f"✅ Article {new_article.id} ({rss_config['name']}) analyzed and saved!")
            except Exception as ai_err:
                print(f"⚠️ AI Saving Error (article_id={new_article.id}, url={new_article.url}): {repr(ai_err)}")
                db.rollback()
                continue

        # 每抓完一个源，随机休眠 1-3 秒，防止 IP 被封
        if idx < len(sources_to_scrape) - 1:
            delay = random.uniform(1, 3)
            time.sleep(delay)

    if processed_count > 0:
        return f"✅ 成功处理 {processed_count} 条新文章" + (f"，跳过 {skipped_count} 条（已在库中）" if skipped_count else "")
    if skipped_count > 0:
        return f"📋 本批所有源共跳过 {skipped_count} 条（已在库中），无新文章。等 RSS 更新后再试或先清空再抓。"
    return "✅ 本批无新文章可处理"


@celery_app.task(name="app.worker.tasks.real_scrape_task")
def real_scrape_task(selected_categories: list | None = None):
    """卫报精准看板：只抓勾选频道，每频道 1 条 + AI 简报；跳过 failure_count 过高的源。"""
    db = SessionLocal()
    try:
        return _run_scrape(db, selected_categories)
    except Exception as e:
        db.rollback()
        print(f"❌ Worker Error: {e}")
        raise e
    finally:
        db.close()


@celery_app.task(name="app.worker.tasks.clear_and_real_scrape_task")
def clear_and_real_scrape_task(limit: int = 15):
    """先清空文章与 AI 结果，再抓取本批 RSS。每次触发都会得到新文章（适合联调/演示）。"""
    db = SessionLocal()
    try:
        db.query(AIResult).delete()
        db.query(Article).delete()
        db.commit()
        print("🗑️ 已清空文章与 AI 结果表")
    except Exception as e:
        db.rollback()
        print(f"❌ Clear Error: {e}")
        raise e
    finally:
        db.close()

    db2 = SessionLocal()
    try:
        return _run_scrape(db2, None)  # 清空后抓取：全部 6 个卫报频道，每频道 1 条
    except Exception as e:
        db2.rollback()
        print(f"❌ Worker Error: {e}")
        raise e
    finally:
        db2.close()


@celery_app.task(name="app.worker.tasks.send_daily_digest_task")
def send_daily_digest_task() -> str:
    """
    每 12 小时发送一次简报邮件：
    - 查询过去 12 小时内最新 20 条 Article
    - 需要包含 ai_result + source 关联数据
    - 发送至 settings.RECEIVER_EMAIL
    """
    if not settings.RECEIVER_EMAIL:
        raise RuntimeError("RECEIVER_EMAIL is not configured")

    db = SessionLocal()
    try:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=12)
        q = (
            db.query(Article)
            .options(joinedload(Article.ai_result), joinedload(Article.source))
            .filter(Article.created_at >= cutoff)
            .order_by(Article.created_at.desc())
            .limit(20)
        )
        articles = q.all()

        items: list[dict] = []
        for a in articles:
            src_name = (a.source.name if a.source else "Unknown Source")
            cat = (a.ai_result.category_tag if a.ai_result else "Uncategorized")
            summary = (a.ai_result.summary_zh if a.ai_result else "（无 AI 简报）")
            items.append(
                {
                    "title": a.title_en,
                    "summary": summary,
                    "url": a.url,
                    "meta": f"{src_name} · {cat}",
                }
            )

        subject = f"Global Vision Digest · {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        send_brief_email(settings.RECEIVER_EMAIL, subject, items=items)
        return f"✅ Email sent to {settings.RECEIVER_EMAIL} with {len(articles)} articles"
    finally:
        db.close()