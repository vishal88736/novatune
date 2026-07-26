from fastapi import APIRouter

from app.api.v1.deps import CurrentUserDep
from app.services.ai_engine_client import ai_engine_client

router = APIRouter()


@router.get("/{track_id}")
async def explain_track(track_id: str, current_user: CurrentUserDep) -> dict:
    return await ai_engine_client.invoke_agent(
        "explainability_agent", {"user_id": current_user.id, "track_id": track_id}
    )
