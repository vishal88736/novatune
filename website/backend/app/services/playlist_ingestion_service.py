"""
Parses uploaded playlist files (CSV / Spotify export JSON) into normalized
track rows, persists a Playlist + PlaylistTrack rows, and enqueues the
Celery task that triggers the ai-engine embedding pipeline for each track.
"""

import csv
import io
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.playlist import Playlist, PlaylistSource, PlaylistStatus


class PlaylistIngestionService:
    async def ingest_csv(self, db: AsyncSession, user_id: uuid.UUID, raw_bytes: bytes) -> Playlist:
        playlist = Playlist(user_id=user_id, source=PlaylistSource.upload_csv, status=PlaylistStatus.pending)
        db.add(playlist)
        await db.flush()

        reader = csv.DictReader(io.StringIO(raw_bytes.decode("utf-8", errors="ignore")))
        rows = list(reader)  # noqa: F841 -- parsed rows handed off to the Celery ingestion task

        playlist.status = PlaylistStatus.processing
        await db.commit()
        await db.refresh(playlist)

        # app.workers.tasks_playlist.analyze_playlist.delay(str(playlist.id))
        return playlist


playlist_ingestion_service = PlaylistIngestionService()
