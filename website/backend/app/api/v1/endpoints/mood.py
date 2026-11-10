from typing import Any, cast

from fastapi import APIRouter

from app.api.v1.deps import CurrentUserDep
from app.schemas.mood import MoodCheckinRequest, MoodCheckinResponse
from app.services.ai_engine_client import ai_engine_client

router = APIRouter()


@router.post("/checkin", response_model=MoodCheckinResponse)
async def checkin(payload: MoodCheckinRequest, current_user: CurrentUserDep) -> MoodCheckinResponse:
    """Routes a manual or text-derived mood signal to the Mood Agent."""
    result = await ai_engine_client.invoke_agent(
        "mood_agent",
        {
            "user_id": current_user.id,
            "text": payload.text,
            "mood_tap": payload.mood_tap,
        },
    )
    return MoodCheckinResponse(**result)


@router.get("/current", response_model=MoodCheckinResponse)
async def current_mood(current_user: CurrentUserDep) -> MoodCheckinResponse:
    result = await ai_engine_client.invoke_agent("mood_agent", {"user_id": current_user.id, "latest_only": True})
    return MoodCheckinResponse(**result)


@router.get("/history")
async def mood_history(current_user: CurrentUserDep) -> list[dict[str, Any]]:
    result = await ai_engine_client.invoke_agent("memory_agent", {"user_id": current_user.id, "query": "mood_history"})
    return cast(list[dict[str, Any]], result.get("history", []))
