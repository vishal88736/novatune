import enum
import uuid

from sqlalchemy import Enum, Float, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class MemoryEntryType(str, enum.Enum):
    fact = "fact"
    preference = "preference"
    emotional_milestone = "emotional_milestone"
    journey_summary = "journey_summary"


class MemoryEntry(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "memory_entries"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    entry_type: Mapped[MemoryEntryType] = mapped_column(Enum(MemoryEntryType))
    content: Mapped[str] = mapped_column(Text)
    embedding_ref: Mapped[str | None] = mapped_column(nullable=True)  # points into Qdrant
    importance_score: Mapped[float] = mapped_column(Float, default=0.5)
