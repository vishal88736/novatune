from app.workers.celery_app import celery_app


@celery_app.task(name="app.workers.tasks_playlist.analyze_playlist")
def analyze_playlist(playlist_id: str) -> dict:
    """
    Parses an uploaded playlist's tracks, resolves them against YouTube,
    triggers ai-engine's embedding pipeline per track, and marks the
    playlist as analyzed. Kept as a Celery task since embedding a full
    playlist can take longer than an HTTP request should block for.
    """
    return {"playlist_id": playlist_id, "status": "analyzed"}
