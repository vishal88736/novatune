from sqlalchemy import ARRAY, Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Track(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "tracks"

    youtube_video_id: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(300))
    artist: Mapped[str] = mapped_column(String(300))
    duration_seconds: Mapped[int] = mapped_column(Integer)
    thumbnail_url: Mapped[str] = mapped_column(String(500))
    genre_tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    mood_tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    popularity_score: Mapped[float] = mapped_column(Float, default=0.0)
    is_hidden_gem: Mapped[bool] = mapped_column(Boolean, default=False)
    qdrant_point_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
