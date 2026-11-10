import enum
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class ListeningSession(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "listening_sessions"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    target_mood: Mapped[str | None] = mapped_column(String(50), nullable=True)
    resulting_mood: Mapped[str | None] = mapped_column(String(50), nullable=True)
    queue: Mapped[list[Any]] = mapped_column(JSONB, default=list)  # ordered track_id list


class EventType(str, enum.Enum):
    play = "play"
    skip = "skip"
    like = "like"
    dislike = "dislike"
    replay = "replay"
    complete = "complete"


class ListeningEvent(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "listening_events"

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("listening_sessions.id"), index=True
    )
    track_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tracks.id"))
    event_type: Mapped[EventType] = mapped_column(Enum(EventType))
    timestamp_in_track: Mapped[int | None] = mapped_column(Integer, nullable=True)
