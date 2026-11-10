from typing import Any

from fastapi import APIRouter

from app.api.v1.deps import CurrentUserDep, DbDep
from app.services.playback_orchestrator import playback_orchestrator

router = APIRouter()


@router.post("/state")
async def sync_state(
    payload: dict[str, Any], current_user: CurrentUserDep, db: DbDep
) -> dict[str, Any]:
    session = await playback_orchestrator.start_session(
        db, current_user.uuid_id, payload.get("queue", []), payload.get("target_mood")
    )
    return {"session_id": str(session.id)}


@router.get("/queue")
async def get_queue(current_user: CurrentUserDep) -> dict[str, Any]:
    return {"queue": []}
