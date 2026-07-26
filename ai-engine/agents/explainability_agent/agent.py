"""
Generates the human-readable "why this track, why now" narrative shown in
the Explain drill-down. Uses the fast LLM tier since this sits on a
latency-sensitive click path (the user is actively waiting to see the
rationale after tapping a track).
"""

from agents.base import AgentContext, AgentResult, BaseAgent
from agents.explainability_agent.prompts import EXPLANATION_PROMPT
from providers.llm.provider_factory import get_llm_provider


class ExplainabilityAgent(BaseAgent):
    name = "explainability_agent"

    def __init__(self) -> None:
        self._llm = get_llm_provider()

    async def run(self, ctx: AgentContext) -> AgentResult:
        track = ctx.shared_state.get("track") or {
            "title": "Golden Hour", "artist": "Kacey Musgraves",
        }
        mood = ctx.shared_state.get("mood", {"label": "Neutral"})
        signals = ctx.shared_state.get("signals") or [
            {"label": "Mood match", "weight": 0.86},
            {"label": "Taste affinity", "weight": 0.71},
            {"label": "Novelty", "weight": 0.35},
            {"label": "Arc position fit", "weight": 0.62},
        ]

        narrative = await self._llm.complete(
            "You write short, warm, specific explanations. No corporate tone.",
            EXPLANATION_PROMPT.format(
                track_title=track["title"], artist=track["artist"],
                mood_label=mood["label"], signals=signals,
            ),
            model_tier="fast",
            temperature=0.6,
            max_tokens=150,
        )

        return AgentResult(
            agent_name=self.name,
            data={"track_title": track["title"], "narrative": narrative, "signals": signals},
            trace={"track_id": ctx.payload.get("track_id")},
        )
