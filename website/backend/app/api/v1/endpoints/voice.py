from typing import Any

from fastapi import APIRouter, File, UploadFile

from app.api.v1.deps import CurrentUserDep
from app.services.ai_engine_client import ai_engine_client

router = APIRouter()


@router.post("/transcribe")
async def transcribe(current_user: CurrentUserDep, file: UploadFile = File(...)) -> dict[str, Any]:
    """
    Forwards recorded audio to ai-engine, which transcribes via Groq Whisper
    (whisper-large-v3-turbo) and routes the transcript into the Conversation
    Agent as if it were a typed message.
    """
    audio_bytes = await file.read()
    result = await ai_engine_client.invoke_agent(
        "conversation_agent",
        {"user_id": current_user.id, "audio_base64": audio_bytes.hex(), "mode": "voice"},
    )
    return result
