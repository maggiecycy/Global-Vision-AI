from fastapi import APIRouter, status, HTTPException
from app.worker.tasks import mock_scrape_task, ping_task, real_scrape_task # 👈 1. 确保导入了新任务

router = APIRouter()

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

# --- 🚀 Step 4: 核心业务接口 ---
@router.post(
    "/real-scrape",
    status_code=status.HTTP_202_ACCEPTED,
)
def trigger_real_scrape(limit: int = 5) -> dict:
    """
    触发真实的 RSS 抓取 + DeepSeek AI 情感分析任务。
    至此，后端引擎实现闭环。
    """
    try:
        async_result = real_scrape_task.delay(limit)
        return {
            "task_id": async_result.id,
            "status": "Real scrape task accepted",
        }
    except Exception as e:
        # 如果 delay 失败（比如 Redis 断了），抛出 500
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to enqueue task: {str(e)}"
        )