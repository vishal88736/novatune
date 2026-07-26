from fastapi import APIRouter

from app.api.v1.deps import CurrentUserDep
from app.schemas.analytics import AnalyticsOverview
from app.services.ai_engine_client import ai_engine_client

router = APIRouter()


@router.get("/overview", response_model=AnalyticsOverview)
async def overview(current_user: CurrentUserDep) -> AnalyticsOverview:
    result = await ai_engine_client.invoke_agent("analytics_agent", {"user_id": current_user.id, "query": "overview"})
    return AnalyticsOverview(**result)


@router.get("/mood-timeline")
async def mood_timeline(current_user: CurrentUserDep) -> list[dict]:
    result = await ai_engine_client.invoke_agent(
        "analytics_agent", {"user_id": current_user.id, "query": "mood_timeline"}
    )
    return result.get("timeline", [])


@router.get("/genre-radar")
async def genre_radar(current_user: CurrentUserDep) -> list[dict]:
    result = await ai_engine_client.invoke_agent(
        "analytics_agent", {"user_id": current_user.id, "query": "genre_radar"}
    )
    return result.get("radar", [])
