"""
Serves dashboard aggregates. The heavy lifting (daily rollups) happens in
website/backend's scheduled Celery task; this agent mostly reshapes cached
rollups for each dashboard view and can optionally add a one-line LLM
narrative summary.
"""

from typing import Any

from agents.base import AgentContext, AgentResult, BaseAgent


class AnalyticsAgent(BaseAgent):
    name = "analytics_agent"

    async def run(self, ctx: AgentContext) -> AgentResult:
        query = ctx.payload.get("query", "overview")
        rollups: dict[str, Any] = ctx.shared_state.get("rollups", {})

        if query == "mood_timeline":
            return AgentResult(agent_name=self.name, data={"timeline": rollups.get("timeline", [])}, trace={})

        if query == "genre_radar":
            return AgentResult(agent_name=self.name, data={"radar": rollups.get("radar", [])}, trace={})

        return AgentResult(
            agent_name=self.name,
            data={
                "total_listen_minutes": rollups.get("total_listen_minutes", 0),
                "top_genres": rollups.get("top_genres", {}),
                "mood_distribution": rollups.get("mood_distribution", {}),
            },
            trace={"query": query},
        )
