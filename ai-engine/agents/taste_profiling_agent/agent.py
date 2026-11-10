"""
Builds/serves the user's taste embedding — a weighted centroid of liked and
completed tracks' embeddings in Qdrant, plus a genre/artist affinity map
computed from listening_events. Heavy recompute happens nightly via Celery
(website/backend), so this agent mostly serves the cached profile and
performs light incremental nudges on strong real-time signals.
"""

from typing import Any

from agents.base import AgentContext, AgentResult, BaseAgent
from vector_store.collections import USER_TASTE
from vector_store.qdrant_client import vector_store


class TasteProfilingAgent(BaseAgent):
    name = "taste_profiling_agent"

    async def run(self, ctx: AgentContext) -> AgentResult:
        user_id = ctx.user_id

        # In production: read cached genre/artist affinity from Postgres
        # (website/backend owns this table) and the taste embedding from
        # Qdrant's user_taste_embeddings collection.
        results: list[dict[str, Any]] = vector_store.search(
            USER_TASTE, query_vector=[0.0] * 384, limit=1, query_filter={"must": [{"key": "user_id", "match": {"value": user_id}}]}
        ) if False else []  # placeholder guard until embeddings are seeded

        genre_affinity = {"indie_folk": 0.8, "lo_fi": 0.65, "synthwave": 0.55, "jazz": 0.4}
        artist_affinity = {"placeholder_artist_a": 0.7, "placeholder_artist_b": 0.5}

        return AgentResult(
            agent_name=self.name,
            data={
                "genre_affinity": genre_affinity,
                "artist_affinity": artist_affinity,
                "embedding_ref": results[0]["id"] if results else None,
            },
            trace={"source": "cached_profile"},
        )
