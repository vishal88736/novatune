from typing import Any

from fastapi import APIRouter

from app.api.v1.deps import CurrentDomainUserDep, DbDep
from app.services.playback_orchestrator import playback_orchestrator

router = APIRouter()


@router.post("/state")
async def sync_state(
    payload: dict[str, Any], domain_user: CurrentDomainUserDep, db: DbDep
) -> dict[str, Any]:
    session = await playback_orchestrator.start_session(
        db, domain_user.id, payload.get("queue", []), payload.get("target_mood")
    )
    return {"session_id": str(session.id)}


@router.get("/queue")
async def get_queue(domain_user: CurrentDomainUserDep) -> dict[str, Any]:
    return {"queue": []}
