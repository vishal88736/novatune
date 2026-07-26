from fastapi import APIRouter

from app.api.v1.deps import CurrentUserDep
from app.schemas.memory import JourneyResponse, MemoryEntryOut
from app.services.ai_engine_client import ai_engine_client

router = APIRouter()


@router.get("/journey", response_model=JourneyResponse)
async def journey(current_user: CurrentUserDep) -> JourneyResponse:
    result = await ai_engine_client.invoke_agent("memory_agent", {"user_id": current_user.id, "query": "journey"})
    return JourneyResponse(**result)


@router.get("/entries", response_model=list[MemoryEntryOut])
async def entries(current_user: CurrentUserDep) -> list[dict]:
    result = await ai_engine_client.invoke_agent("memory_agent", {"user_id": current_user.id, "query": "entries"})
    return result.get("entries", [])
