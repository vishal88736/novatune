from pydantic import BaseModel

from app.schemas.track import TrackOut


class RecommendationBatch(BaseModel):
    tracks: list[TrackOut]
    arc_label: str
    generated_for_mood: str


class RecommendationFeedback(BaseModel):
    track_id: str
    action: str  # like | dislike | skip
