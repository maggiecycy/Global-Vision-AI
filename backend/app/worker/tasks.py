import time

from app.core.celery_app import celery_app


@celery_app.task(name="app.worker.tasks.ping_task")
def ping_task() -> str:
    return "pong"


@celery_app.task(name="app.worker.tasks.mock_scrape_task")
def mock_scrape_task(limit: int) -> str:
    # 模拟一个耗时的抓取/处理任务（这里只是 sleep）
    time.sleep(3)
    return f"mock scrape finished with limit={limit}"

