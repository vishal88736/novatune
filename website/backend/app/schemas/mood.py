from pydantic import BaseModel, Field


class MoodCheckinRequest(BaseModel):
    text: str | None = Field(default=None, max_length=2000)
    mood_tap: str | None = Field(default=None, max_length=50)


class MoodCheckinResponse(BaseModel):
    valence: float
    arousal: float
    label: str
    emotion_scores: dict[str, float]
