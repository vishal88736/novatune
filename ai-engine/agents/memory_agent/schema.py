from pydantic import BaseModel


class MemoryInput(BaseModel):
    user_id: str
    query: str = "journey"  # journey | entries | mood_history
    write_entry: dict | None = None


class MemoryOutput(BaseModel):
    entries: list[dict] = []
    timeline: list[dict] = []
    milestones: list[dict] = []
