"""
Planner-based routing: the Conversation Agent's intent classification
decides which subset of the remaining 10 agents get invoked for a given
turn, rather than running every agent on every request.
"""

INTENT_TO_PIPELINE: dict[str, list[str]] = {
    "mood_checkin": ["mood_agent", "taste_profiling_agent", "recommendation_agent", "sequencing_agent", "explainability_agent", "memory_agent"],
    "recommendation_request": ["taste_profiling_agent", "recommendation_agent", "sequencing_agent", "explainability_agent"],
    "playlist_question": ["playlist_upload_analysis_agent", "taste_profiling_agent"],
    "discovery_request": ["discovery_agent", "explainability_agent"],
    "chit_chat": [],
}


def plan_for_intent(intent: str) -> list[str]:
    return INTENT_TO_PIPELINE.get(intent, [])
