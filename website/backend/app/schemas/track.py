from uuid import UUID

from pydantic import BaseModel


class TrackOut(BaseModel):
    id: UUID
    youtube_video_id: str
    title: str
    artist: str
    duration_seconds: int
    thumbnail_url: str
    reason_summary: str | None = None

    model_config = {"from_attributes": True}
