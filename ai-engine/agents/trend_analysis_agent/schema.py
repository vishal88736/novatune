from typing import Any

from pydantic import BaseModel


class TrendInput(BaseModel):
    user_id: str
    mood_filter: str | None = None


class TrendOutput(BaseModel):
    tracks: list[dict[str, Any]]
    arc_label: str = "trending"
    generated_for_mood: str = "current"
