from pydantic import BaseModel


class ConversationInput(BaseModel):
    user_id: str
    session_id: str
    message: str


class ConversationOutput(BaseModel):
    reply: str
    intent: str
    agents_invoked: list[str]
