import enum
import uuid

from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class PlaylistSource(str, enum.Enum):
    upload_csv = "upload_csv"
    upload_url = "upload_url"
    spotify_export = "spotify_export"
    manual = "manual"


class PlaylistStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    analyzed = "analyzed"
    failed = "failed"


class Playlist(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "playlists"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    source: Mapped[PlaylistSource] = mapped_column(Enum(PlaylistSource))
    raw_file_ref: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[PlaylistStatus] = mapped_column(Enum(PlaylistStatus), default=PlaylistStatus.pending)


class PlaylistTrack(Base):
    __tablename__ = "playlist_tracks"

    playlist_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("playlists.id"), primary_key=True
    )
    track_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tracks.id"), primary_key=True
    )
    position: Mapped[int] = mapped_column(Integer, default=0)
