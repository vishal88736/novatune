from typing import Any

from pydantic import BaseModel


class MemoryInput(BaseModel):
    user_id: str
    query: str = "journey"  # journey | entries | mood_history
    write_entry: dict[str, Any] | None = None


class MemoryOutput(BaseModel):
    entries: list[dict[str, Any]] = []
    timeline: list[dict[str, Any]] = []
    milestones: list[dict[str, Any]] = []
    summary: str = ""
