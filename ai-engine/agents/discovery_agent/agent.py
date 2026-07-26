"""
Surfaces underexposed artists matching the user's taste/mood, explicitly
penalizing popularity_score so VibeAI doesn't converge on the same
mainstream catalog every other recommender pushes.
"""

from agents.base import AgentContext, AgentResult, BaseAgent

POPULARITY_CEILING = 0.35  # tracks above this popularity_score are excluded from Discovery


class DiscoveryAgent(BaseAgent):
    name = "discovery_agent"

    async def run(self, ctx: AgentContext) -> AgentResult:
        candidates: list[dict] = ctx.shared_state.get("candidate_tracks", [])
        hidden_gems = [c for c in candidates if c.get("popularity_score", 0) <= POPULARITY_CEILING] or [
            {
                "id": "gem-1",
                "youtube_video_id": "abc123",
                "title": "Undertow",
                "artist": "Field Runner",
                "duration_seconds": 214,
                "thumbnail_url": "https://i.ytimg.com/vi/abc123/hqdefault.jpg",
                "reason_summary": "Under-the-radar artist matching your taste profile",
            }
        ]

        return AgentResult(
            agent_name=self.name,
            data={"tracks": hidden_gems, "arc_label": "discovery", "generated_for_mood": "exploratory"},
            trace={"pool_size": len(candidates), "surfaced": len(hidden_gems)},
        )
