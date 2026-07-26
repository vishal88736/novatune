"""
Serves cached trend snapshots (populated by website/backend's scheduled
Celery crawl against the YouTube Data API), optionally filtered by mood
cluster. Clustering itself happens offline in the Celery task using the
same LLM-based grouping prompt defined here.
"""

from agents.base import AgentContext, AgentResult, BaseAgent


class TrendAnalysisAgent(BaseAgent):
    name = "trend_analysis_agent"

    async def run(self, ctx: AgentContext) -> AgentResult:
        mood_filter = ctx.payload.get("mood_filter")
        snapshots: dict[str, list[dict]] = ctx.shared_state.get("trend_snapshots", {})

        tracks = snapshots.get(mood_filter, []) if mood_filter else [
            t for cluster_tracks in snapshots.values() for t in cluster_tracks
        ]

        return AgentResult(
            agent_name=self.name,
            data={"tracks": tracks, "arc_label": "trending", "generated_for_mood": mood_filter or "current"},
            trace={"mood_filter": mood_filter, "result_count": len(tracks)},
        )
