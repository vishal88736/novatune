from pydantic import BaseModel


class TasteProfilingInput(BaseModel):
    user_id: str
    force_recompute: bool = False


class TasteProfilingOutput(BaseModel):
    genre_affinity: dict[str, float]
    artist_affinity: dict[str, float]
    embedding_ref: str | None = None
