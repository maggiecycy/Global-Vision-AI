from typing import List, Optional

from fastapi import APIRouter, Query, status, HTTPException
from app.core.config import RSS_SOURCES
from app.worker.tasks import (
    mock_scrape_task,
    ping_task,
    real_scrape_task,
    clear_and_real_scrape_task,
)

router = APIRouter()


@router.get("/categories")
def list_categories() -> dict:
    """返回所有可选的分类（用于前端多选）。"""
    categories = sorted({c["category"] for c in RSS_SOURCES})
    return {"categories": categories}


@router.post(
    "/test-task",
    status_code=status.HTTP_202_ACCEPTED,
)
def trigger_mock_task(limit: int = 10) -> dict:
    """
    Fire-and-forget test endpoint to verify Celery/Redis pipeline.
    """
    async_result = mock_scrape_task.delay(limit)
    return {
        "task_id": async_result.id,
        "status": "Task accepted",
    }

@router.get("/ping", status_code=status.HTTP_200_OK)
def ping() -> dict:
    """
    Optional quick health check that enqueues a trivial ping task.
    """
    async_result = ping_task.delay()
    return {"task_id": async_result.id}

# --- Step 11: 卫报专用 - 仅传勾选分类，每频道固定 1 条 ---
@router.post(
    "/real-scrape",
    status_code=status.HTTP_202_ACCEPTED,
)
def trigger_real_scrape(
    selected_categories: Optional[List[str]] = Query(None, description="勾选的卫报频道：World, Politics, Technology, Science, Environment, Football"),
) -> dict:
    """
    卫报精准看板：只抓取勾选频道，每频道最新 1 条 + AI 简报。
    """
    try:
        async_result = real_scrape_task.delay(selected_categories or [])
        return {
            "task_id": async_result.id,
            "status": "Real scrape task accepted",
            "selected_categories": selected_categories,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to enqueue task: {str(e)}"
        )


@router.post(
    "/clear-and-real-scrape",
    status_code=status.HTTP_202_ACCEPTED,
)
def trigger_clear_and_real_scrape(limit: int = 15) -> dict:
    """
    先清空文章与 AI 结果，再抓取 RSS + AI 分析。
    每次调用都会得到新文章，适合清空后「重新抓取」联调。
    """
    try:
        async_result = clear_and_real_scrape_task.delay(limit)
        return {
            "task_id": async_result.id,
            "status": "Clear + real scrape task accepted",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to enqueue task: {str(e)}"
        )