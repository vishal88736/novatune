from typing import Any

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.api.v1.deps import CurrentUserDep
from app.schemas.chat import ChatMessageRequest
from app.services.ai_engine_client import ai_engine_client

router = APIRouter()


@router.post("/message")
async def send_message(payload: ChatMessageRequest, current_user: CurrentUserDep) -> StreamingResponse:
    """
    Streams the Conversation Agent's reply (and intermediate agent-status
    events) back to the client as Server-Sent Events. website/frontend's
    /api/stream route proxies directly to this endpoint.
    """
    generator = ai_engine_client.stream_conversation(
        session_id=payload.session_id, user_id=current_user.id, message=payload.message
    )
    return StreamingResponse(generator, media_type="text/event-stream")


@router.get("/history")
async def get_history(current_user: CurrentUserDep, session_id: str) -> dict[str, Any]:
    # Chat history persistence delegated to the Memory Agent's session log.
    return {"session_id": session_id, "messages": []}
