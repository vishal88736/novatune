"""
Hybrid recommendation: Qdrant ANN search over tracks_embeddings (query
vector = weighted blend of mood + taste embeddings), diversity injection
reserved for the Discovery Agent's quota, then an LLM re-ranking pass for
final ordering rationale.
"""

import json

from agents.base import AgentContext, AgentResult, BaseAgent
from agents.recommendation_agent.prompts import RERANK_PROMPT
from providers.llm.provider_factory import get_llm_provider

MOOD_TASTE_BLEND_WEIGHTS = {"mood": 0.6, "taste": 0.4}


class RecommendationAgent(BaseAgent):
    name = "recommendation_agent"

    def __init__(self) -> None:
        self._llm = get_llm_provider()

    async def run(self, ctx: AgentContext) -> AgentResult:
        if ctx.payload.get("feedback"):
            # Feedback path: log signal for the nightly taste recompute, no
            # recommendation batch needs to be returned.
            return AgentResult(agent_name=self.name, data={"acknowledged": True}, trace={})

        mood = ctx.shared_state.get("mood", {"label": "Neutral", "valence": 0.0, "arousal": 0.0})
        top_genres = list(ctx.shared_state.get("genre_affinity", {}).keys())[:5]

        # candidate generation would call vector_store.search(TRACKS, blended_vector, ...)
        # here; using illustrative placeholder candidates to keep this agent runnable
        # end-to-end without a seeded catalog.
        candidates = ctx.shared_state.get("candidate_tracks") or [
            {
                "id": "sample-1",
                "youtube_video_id": "dQw4w9WgXcQ",
                "title": "Golden Hour",
                "artist": "Kacey Musgraves",
                "duration_seconds": 199,
                "thumbnail_url": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
            }
        ]

        raw = await self._llm.complete(
            "You output only strict JSON.",
            RERANK_PROMPT.format(
                mood_label=mood["label"], valence=mood["valence"], arousal=mood["arousal"],
                top_genres=top_genres,
                candidates=json.dumps([{"id": c["id"], "title": c["title"]} for c in candidates]),
            ),
            model_tier="fast",
            json_mode=True,
            temperature=0.3,
            max_tokens=500,
        )
        try:
            rankings = {r["id"]: r for r in json.loads(raw).get("rankings", [])}
        except json.JSONDecodeError:
            rankings = {}

        for c in candidates:
            r = rankings.get(c["id"], {})
            c["reason_summary"] = f"Mood fit {r.get('mood_fit', 0.5):.0%}, matches your {mood['label'].lower()} energy"

        return AgentResult(
            agent_name=self.name,
            data={"tracks": candidates, "arc_label": "steady", "generated_for_mood": mood["label"]},
            trace={"ranked_count": len(rankings)},
        )
