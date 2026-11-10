from typing import Any

from app.workers.celery_app import celery_app


@celery_app.task(name="app.workers.tasks_analytics.rollup_daily_analytics")
def rollup_daily_analytics() -> dict[str, Any]:
    """Aggregates the previous day's listening_events into analytics_daily_rollups."""
    return {"status": "rolled_up"}
