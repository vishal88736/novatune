from fastapi import APIRouter

from app.api.v1.deps import CurrentUserDep
from app.schemas.recommendation import RecommendationBatch, RecommendationFeedback
from app.services.ai_engine_client import ai_engine_client

router = APIRouter()


@router.get("", response_model=RecommendationBatch)
async def get_recommendations(current_user: CurrentUserDep) -> RecommendationBatch:
    """
    Fetches the current mood-and-taste-aware batch from the AI engine's
    recommendation pipeline (Recommendation + Sequencing Agents).
    """
    result = await ai_engine_client.invoke_agent("recommendation_agent", {"user_id": current_user.id})
    return RecommendationBatch(**result)


@router.post("/feedback", status_code=204)
async def submit_feedback(payload: RecommendationFeedback, current_user: CurrentUserDep) -> None:
    """Feeds like/dislike/skip signals back into the Recommendation + Taste Profiling agents."""
    await ai_engine_client.invoke_agent(
        "recommendation_agent",
        {"user_id": current_user.id, "feedback": payload.model_dump()},
    )
