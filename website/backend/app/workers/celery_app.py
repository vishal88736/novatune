from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

celery_app = Celery(
    "vibeai",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        "app.workers.tasks_playlist",
        "app.workers.tasks_trend",
        "app.workers.tasks_taste_recompute",
        "app.workers.tasks_analytics",
    ],
)

celery_app.conf.update(task_serializer="json", result_serializer="json", accept_content=["json"])

celery_app.conf.beat_schedule = {
    "nightly-taste-recompute": {
        "task": "app.workers.tasks_taste_recompute.recompute_all_taste_profiles",
        "schedule": crontab(hour=3, minute=0),
    },
    "trend-crawl-every-6h": {
        "task": "app.workers.tasks_trend.crawl_trends",
        "schedule": crontab(hour="*/6", minute=0),
    },
    "daily-analytics-rollup": {
        "task": "app.workers.tasks_analytics.rollup_daily_analytics",
        "schedule": crontab(hour=2, minute=30),
    },
}
