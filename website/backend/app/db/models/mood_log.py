import enum
import uuid

from sqlalchemy import Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class MoodSource(str, enum.Enum):
    manual_checkin = "manual_checkin"
    chat_inferred = "chat_inferred"
    behavior_inferred = "behavior_inferred"


class MoodLog(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "mood_logs"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    source: Mapped[MoodSource] = mapped_column(Enum(MoodSource))
    emotion_vector: Mapped[dict] = mapped_column(JSONB)  # 27-dim GoEmotions scores
    valence: Mapped[float] = mapped_column(Float)
    arousal: Mapped[float] = mapped_column(Float)
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
