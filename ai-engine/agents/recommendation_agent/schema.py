from typing import Any

from pydantic import BaseModel


class RecommendationInput(BaseModel):
    user_id: str
    feedback: dict[str, Any] | None = None


class TrackCandidate(BaseModel):
    id: str
    youtube_video_id: str
    title: str
    artist: str
    duration_seconds: int
    thumbnail_url: str
    reason_summary: str | None = None


class RecommendationOutput(BaseModel):
    tracks: list[TrackCandidate]
    arc_label: str
    generated_for_mood: str
