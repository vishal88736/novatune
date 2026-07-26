from app.workers.celery_app import celery_app


@celery_app.task(name="app.workers.tasks_trend.crawl_trends")
def crawl_trends() -> dict:
    """Scheduled crawl feeding the Trend Analysis Agent's cached snapshots."""
    return {"status": "crawled"}
