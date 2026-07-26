from pydantic import BaseModel


class ExplainabilityInput(BaseModel):
    user_id: str
    track_id: str


class ExplainabilityOutput(BaseModel):
    track_title: str
    narrative: str
    signals: list[dict]
