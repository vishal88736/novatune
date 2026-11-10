import json
from collections.abc import AsyncGenerator
from typing import Any

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.api.v1.deps import CurrentUserDep
from app.schemas.chat import ChatMessageRequest
from app.services.ai_engine_client import ai_engine_client

router = APIRouter()


def _sse_error(message: str) -> bytes:
    payload = json.dumps({"type": "error", "message": message})
    return f"data: {payload}\n\n".encode()


async def _guarded_stream(
    generator: AsyncGenerator[bytes, None],
) -> AsyncGenerator[bytes, None]:
    """
    Forwards the agent stream, converting a failure into an SSE `error` frame.

    Without this the connection is torn down mid-flight and the browser is
    left waiting on a reply that will never arrive.
    """
    try:
        async for chunk in generator:
            yield chunk
    except Exception as exc:  # noqa: BLE001 - reported to the client as an event
        yield _sse_error(str(exc) or exc.__class__.__name__)


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
    return StreamingResponse(
        _guarded_stream(generator), media_type="text/event-stream"
    )


@router.get("/history")
async def get_history(current_user: CurrentUserDep, session_id: str) -> dict[str, Any]:
    # Chat history persistence delegated to the Memory Agent's session log.
    return {"session_id": session_id, "messages": []}
