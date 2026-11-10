from datetime import datetime
from typing import Any

from pydantic import BaseModel


class JourneyMilestone(BaseModel):
    date: str
    label: str
    detail: str


class JourneyResponse(BaseModel):
    timeline: list[dict[str, Any]]
    milestones: list[JourneyMilestone]
    summary: str = ""


class MemoryEntryOut(BaseModel):
    id: str
    entry_type: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
