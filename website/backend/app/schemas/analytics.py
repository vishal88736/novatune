from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    total_listen_minutes: int
    top_genres: dict[str, float]
    mood_distribution: dict[str, float]
