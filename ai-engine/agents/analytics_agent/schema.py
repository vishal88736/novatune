from pydantic import BaseModel


class AnalyticsInput(BaseModel):
    user_id: str
    query: str = "overview"  # overview | mood_timeline | genre_radar


class AnalyticsOutput(BaseModel):
    total_listen_minutes: int = 0
    top_genres: dict[str, float] = {}
    mood_distribution: dict[str, float] = {}
    timeline: list[dict] = []
    radar: list[dict] = []
