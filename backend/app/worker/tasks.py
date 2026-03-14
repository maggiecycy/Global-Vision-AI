import time
import asyncio
from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.article import Article
from app.models.ai_result import AIResult
from app.services.scraper import ScraperService
from app.services.ai_service import AIService

# --- 原有的测试任务 (诊断工具) ---

@celery_app.task(name="app.worker.tasks.ping_task")
def ping_task() -> str:
    return "pong"

@celery_app.task(name="app.worker.tasks.mock_scrape_task")
def mock_scrape_task(limit: int) -> str:
    time.sleep(3)
    return f"mock scrape finished with limit={limit}"

# --- 🚀 Step 4: 核心真实业务任务 ---

@celery_app.task(name="app.worker.tasks.real_scrape_task")
def real_scrape_task(limit: int = 5):
    db = SessionLocal()
    try:
        # 1. 抓取逻辑 (换成国内可直接访问的源测试)
        rss_url = "https://www.oschina.net/news/rss"
        articles = ScraperService.fetch_rss_articles(rss_url, limit)
        
        processed_count = 0
        for item in articles:
            # 查重 (根据 URL)
            existing = db.query(Article).filter(Article.url == item['link']).first()
            if existing: 
                continue
            
            # 2. 存入文章 (注意：这里必须精准对应你的 Model 字段名)
            new_article = Article(
                source_id=1,
                title_en=item['title'],  # 👈 对应你模型里的 title_en
                snippet=item['summary'], # 👈 对应你模型里的 snippet
                url=item['link']
            )
            db.add(new_article)
            db.commit()
            db.refresh(new_article)
            
            # 3. AI 分析 (由于你的 AI 分析是异步的，我们在同步任务中包装它)
            # 3. AI 分析 (此时 DeepSeek 200 OK，已拿到 analysis 字典)
            try:
                analysis = asyncio.run(AIService.analyze_article(new_article.title_en, new_article.snippet))
                
                # 4. 存入分析结果 (根据你刚才发我的 AIResult 模型字段精准对齐)
                ai_res = AIResult(
                    article_id=new_article.id,
                    # 模型里的必填字段，我们把 AI 的结果先填进去
                    title_zh=new_article.title_en,         # 暂时用英文标题占位
                    summary_zh=analysis.get('core_logic', '无'), 
                    category_tag=analysis.get('category', '其他'),
                    discussion_point=analysis.get('core_logic', '无'),
                    # 注意：这里我们不再传 sentiment，因为你的模型里没有这个字段！
                )
                db.add(ai_res)
                db.commit()
                processed_count += 1
                print(f"✅ Article {new_article.id} analyzed and saved to your schema!")
            except Exception as ai_err:
                print(f"⚠️ Schema mismatch: {ai_err}")
                db.rollback()
                continue
            
        return f"✅ Successfully processed {processed_count} new articles"
    except Exception as e:
        db.rollback()
        print(f"❌ Critical Error: {e}")
        raise e
    finally:
        db.close()