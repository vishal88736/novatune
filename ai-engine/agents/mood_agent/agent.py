"""
The Mood Agent normalizes any input modality (free text, or a mood-wheel
tap) into the same 27-dim GoEmotions vector + valence/arousal projection
that every other agent consumes.
"""

import json

from agents.base import AgentContext, AgentResult, BaseAgent
from agents.mood_agent.prompts import TAP_TO_EMOTION_PROMPT
from providers.emotion.goemotions_provider import goemotions_provider
from providers.llm.provider_factory import get_llm_provider


class MoodAgent(BaseAgent):
    name = "mood_agent"

    def __init__(self) -> None:
        self._llm = get_llm_provider()

    async def run(self, ctx: AgentContext) -> AgentResult:
        text = ctx.payload.get("text")
        mood_tap = ctx.payload.get("mood_tap")

        if text:
            scores = goemotions_provider.classify(text)
        elif mood_tap:
            raw = await self._llm.complete(
                "You output only strict JSON.",
                TAP_TO_EMOTION_PROMPT.format(label=mood_tap),
                model_tier="fast",
                json_mode=True,
                temperature=0.3,
            )
            try:
                scores = json.loads(raw)
            except json.JSONDecodeError:
                scores = {"neutral": 1.0}
        else:
            scores = {"neutral": 1.0}

        valence, arousal = goemotions_provider.to_valence_arousal(scores)
        label = goemotions_provider.dominant_label(scores)

        return AgentResult(
            agent_name=self.name,
            data={
                "valence": valence,
                "arousal": arousal,
                "label": label.capitalize(),
                "emotion_scores": scores,
            },
            trace={"source": "text" if text else "mood_tap"},
        )
