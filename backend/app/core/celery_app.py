from celery import Celery

celery_app = Celery(
    "global_vision_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["app.worker.tasks"]  # 👈 核心：告诉 Celery 去这里找任务
)

# 保持简单的默认配置即可
celery_app.conf.update(
    task_track_started=True,
    result_expires=3600,
)