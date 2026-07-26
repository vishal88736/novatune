import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AnalyticsDailyRollup(Base):
    __tablename__ = "analytics_daily_rollups"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True
    )
    date: Mapped[date] = mapped_column(Date, primary_key=True)
    total_listen_minutes: Mapped[int] = mapped_column(Integer, default=0)
    top_genres: Mapped[dict] = mapped_column(JSONB, default=dict)
    mood_distribution: Mapped[dict] = mapped_column(JSONB, default=dict)
