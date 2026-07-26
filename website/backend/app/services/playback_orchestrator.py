"""
Coordinates the Sequencing Agent's output into a persisted ListeningSession
and keeps `queue` state in sync as the frontend reports playback events.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.session import ListeningSession


class PlaybackOrchestrator:
    async def start_session(
        self, db: AsyncSession, user_id: uuid.UUID, queue: list[str], target_mood: str | None
    ) -> ListeningSession:
        session = ListeningSession(
            user_id=user_id,
            started_at=datetime.now(timezone.utc),
            target_mood=target_mood,
            queue=queue,
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session


playback_orchestrator = PlaybackOrchestrator()
