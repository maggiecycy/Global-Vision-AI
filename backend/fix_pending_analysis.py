"""
补课脚本：为数据库里所有 ai_result 为空的 Article 重新触发 AI 分析。

用法（在 backend 目录下）：
  export DATABASE_URL="postgresql://user@localhost:5432/global_vision_dev"   # 或写入 .env
  python fix_pending_analysis.py
"""
import os
from pathlib import Path

# 先加载环境变量：当前目录 + 项目根 .env，再导入 app（避免 DATABASE_URL 未设置）
try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None
if load_dotenv:
    load_dotenv()  # backend/.env
    root_env = Path(__file__).resolve().parent.parent / ".env"
    if root_env.exists():
        load_dotenv(root_env)

from app.db.session import SessionLocal
from app.models import Article
from sqlalchemy.orm import joinedload


def main() -> None:
    from app.core.config import settings
    if not settings.database_url:
        print("❌ DATABASE_URL 未设置。请任选其一：")
        print("   1. 在 backend/.env 或项目根 .env 中写入 DATABASE_URL=postgresql://user@localhost:5432/库名")
        print("   2. 或在终端执行：export DATABASE_URL=\"postgresql://caoyan@localhost:5432/global_vision_dev\"")
        raise SystemExit(1)
    db = SessionLocal()
    try:
        pending = (
            db.query(Article)
            .options(joinedload(Article.ai_result))
            .filter(Article.ai_result == None)  # noqa: E711
            .order_by(Article.id.asc())
            .all()
        )
        if not pending:
            print("✅ 没有待补课的文章（全部已有 ai_result）。")
            return

        print(f"🔎 找到 {len(pending)} 条 ai_result 为空的文章，开始补课...")

        # 这里复用当前系统的分析函数（同步调用），避免依赖“拆分任务”不存在的问题。
        # 如未来你新增 analyze_article_task（按 article_id 分发），再改为 delay 即可。
        from app.services.ai_service import AIService
        from app.models import AIResult
        import asyncio

        processed = 0
        failed = 0
        for a in pending:
            try:
                print(f"🧠 Processing [{a.title_en}] (article_id={a.id})...")
                analysis = asyncio.run(AIService.analyze_article(a.title_en, a.snippet))
                category_raw = analysis.get("category") or ""
                category_tag = (category_raw.strip() or "未分类") if isinstance(category_raw, str) else "未分类"
                core_logic = analysis.get("core_logic") or "分析完成"

                kw_raw = analysis.get("keywords")
                if isinstance(kw_raw, list):
                    keywords_list = [str(x).strip() for x in kw_raw[:5] if x]
                else:
                    keywords_list = [category_tag]
                if not keywords_list:
                    keywords_list = [category_tag]

                raw_sent = analysis.get("sentiment_score") or analysis.get("sentiment")
                sentiment_score = None
                try:
                    if raw_sent is not None:
                        v = float(raw_sent)
                        sentiment_score = v if 1 <= v <= 10 else 5.0
                except (TypeError, ValueError):
                    sentiment_score = 5.0

                ai_res = AIResult(
                    article_id=a.id,
                    title_zh=a.title_en,
                    summary_zh=core_logic,
                    keywords=keywords_list,
                    category_tag=category_tag,
                    sentiment_score=sentiment_score,
                )
                db.add(ai_res)
                db.commit()
                processed += 1
                print(f"✅ 补课完成 article_id={a.id}")
            except Exception as e:
                db.rollback()
                failed += 1
                print(f"❌ 补课失败 article_id={a.id}: {repr(e)}")

        print(f"🏁 Done. processed={processed}, failed={failed}")
    finally:
        db.close()


if __name__ == "__main__":
    main()

