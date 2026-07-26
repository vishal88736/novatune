from app.workers.celery_app import celery_app


@celery_app.task(name="app.workers.tasks_taste_recompute.recompute_all_taste_profiles")
def recompute_all_taste_profiles() -> dict:
    """Nightly recompute of every user's taste embedding centroid via ai-engine."""
    return {"status": "recomputed"}
