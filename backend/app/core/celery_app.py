from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "global_vision_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["app.worker.tasks"]  # 👈 核心：告诉 Celery 去这里找任务
)

# 保持简单的默认配置；定时任务按北京时间
celery_app.conf.update(
    task_track_started=True,
    result_expires=3600,
    timezone="Asia/Shanghai",
    enable_utc=True,
)

# --- Step 14: 全自动闭环（Beat 调度）---
# 每 12 小时抓取一次；10 分钟后发邮件；每天凌晨 3 点清理 7 天前数据
celery_app.conf.beat_schedule = {
    "scrape-every-12-hours": {
        "task": "app.worker.tasks.real_scrape_task",
        "schedule": crontab(minute=0, hour="*/12"),
        "args": ([],),
    },
    "email-every-12-hours": {
        "task": "app.worker.tasks.send_daily_digest_task",
        "schedule": crontab(minute=10, hour="*/12"),
        "args": (),
    },
    "cleanup-daily-at-3am": {
        "task": "app.worker.tasks.cleanup_old_articles_task",
        "schedule": crontab(minute=0, hour=3),
        "args": (),
    },
}