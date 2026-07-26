from fastapi import APIRouter

from app.api.v1.deps import CurrentUserDep
from app.schemas.recommendation import RecommendationBatch
from app.services.ai_engine_client import ai_engine_client

router = APIRouter()


@router.get("/hidden-gems", response_model=RecommendationBatch)
async def hidden_gems(current_user: CurrentUserDep) -> RecommendationBatch:
    result = await ai_engine_client.invoke_agent("discovery_agent", {"user_id": current_user.id})
    return RecommendationBatch(**result)


@router.get("/trending", response_model=RecommendationBatch)
async def trending(current_user: CurrentUserDep, mood: str | None = None) -> RecommendationBatch:
    result = await ai_engine_client.invoke_agent(
        "trend_analysis_agent", {"user_id": current_user.id, "mood_filter": mood}
    )
    return RecommendationBatch(**result)
