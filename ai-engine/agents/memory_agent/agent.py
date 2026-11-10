"""
Owns VibeAI's long-term memory: writes significant emotional milestones and
session summaries, and serves the "emotional journey" timeline the frontend
renders. Short-term turn context lives in the Redis context bus instead
(see orchestrator/context_bus.py) — this agent is for what should persist.
"""

from typing import Any
import json

from agents.base import AgentContext, AgentResult, BaseAgent
from agents.memory_agent.prompts import JOURNEY_SUMMARY_PROMPT, MILESTONE_DETECTION_PROMPT
from providers.llm.provider_factory import get_llm_provider


class MemoryAgent(BaseAgent):
    name = "memory_agent"

    def __init__(self) -> None:
        self._llm = get_llm_provider()

    async def run(self, ctx: AgentContext) -> AgentResult:
        query = ctx.payload.get("query", "journey")

        if query == "journey":
            # Production: pulls mood_logs for the user from website/backend's
            # Postgres store (via an internal read) and runs milestone
            # detection over the week's summary.
            timeline = ctx.shared_state.get("mood_history", [])
            milestones: list[dict[str, Any]] = []
            summary = ""

            if timeline:
                raw = await self._llm.complete(
                    "You output only strict JSON.",
                    MILESTONE_DETECTION_PROMPT.format(mood_summary=json.dumps(timeline[-14:])),
                    model_tier="fast",
                    json_mode=True,
                    temperature=0.3,
                )
                try:
                    parsed = json.loads(raw)
                    if parsed.get("is_milestone"):
                        milestones.append({"date": timeline[-1].get("date", ""), "label": parsed["label"], "detail": parsed["detail"]})
                except json.JSONDecodeError:
                    pass

                summary = await self._llm.complete(
                    "You are a thoughtful, warm friend reflecting on someone's emotional journey. Write one concise paragraph.",
                    JOURNEY_SUMMARY_PROMPT.format(entries=json.dumps(timeline[-14:])),
                    model_tier="reasoning",
                    temperature=0.5,
                    max_tokens=300,
                )

            return AgentResult(
                agent_name=self.name,
                data={"timeline": timeline, "milestones": milestones, "summary": summary},
                trace={"milestone_count": len(milestones)},
            )

        if query == "entries":
            return AgentResult(agent_name=self.name, data={"entries": ctx.shared_state.get("memory_entries", [])}, trace={})

        return AgentResult(agent_name=self.name, data={"history": ctx.shared_state.get("mood_history", [])}, trace={})
