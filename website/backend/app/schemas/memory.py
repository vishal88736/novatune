from datetime import datetime

from pydantic import BaseModel


class JourneyMilestone(BaseModel):
    date: str
    label: str
    detail: str


class JourneyResponse(BaseModel):
    timeline: list[dict]
    milestones: list[JourneyMilestone]


class MemoryEntryOut(BaseModel):
    id: str
    entry_type: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
