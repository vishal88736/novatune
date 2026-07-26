import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TasteProfile(Base):
    __tablename__ = "taste_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True
    )
    genre_affinity: Mapped[dict] = mapped_column(JSONB, default=dict)
    artist_affinity: Mapped[dict] = mapped_column(JSONB, default=dict)
    embedding_ref: Mapped[str | None] = mapped_column(nullable=True)
    last_computed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
