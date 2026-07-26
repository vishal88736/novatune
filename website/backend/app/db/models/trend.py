from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.mixins import UUIDPrimaryKeyMixin


class TrendSnapshot(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "trend_snapshots"

    mood_cluster: Mapped[str] = mapped_column(String(50), index=True)
    tracks: Mapped[list] = mapped_column(JSONB, default=list)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
