from pydantic import BaseModel


class PlaylistAnalysisInput(BaseModel):
    user_id: str
    playlist_id: str
    tracks: list[dict]  # [{title, artist}, ...] resolved from the upload


class PlaylistAnalysisOutput(BaseModel):
    genre_breakdown: dict[str, float]
    mood_breakdown: dict[str, float]
    taste_delta_summary: str
