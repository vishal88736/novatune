from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    session_id: str
    message: str = Field(max_length=2000)


class ChatMessageResponse(BaseModel):
    reply: str
    intent: str
    agents_invoked: list[str]
