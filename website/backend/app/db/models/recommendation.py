import uuid
from typing import Any

from sqlalchemy import Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class RecommendationLog(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "recommendation_logs"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    track_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tracks.id"))
    reason_summary: Mapped[str] = mapped_column(Text)
    agent_trace: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    accepted: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
