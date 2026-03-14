from fastapi import APIRouter, status

from app.worker.tasks import mock_scrape_task, ping_task

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

