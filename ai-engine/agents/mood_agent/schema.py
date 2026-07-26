from pydantic import BaseModel


class MoodInput(BaseModel):
    user_id: str
    text: str | None = None
    mood_tap: str | None = None
    latest_only: bool = False


class MoodOutput(BaseModel):
    valence: float
    arousal: float
    label: str
    emotion_scores: dict[str, float]
