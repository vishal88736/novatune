"""
Parses an uploaded playlist's resolved tracks, tags genre/mood composition
via the LLM (fast tier, structured JSON), and summarizes how it shifts the
user's taste profile — then hands off to the Taste Profiling Agent to
persist the delta and to the embedding pipeline to index each track.
"""

from typing import Any
import json

from agents.base import AgentContext, AgentResult, BaseAgent
from agents.playlist_upload_analysis_agent.prompts import GENRE_MOOD_TAGGING_PROMPT, TASTE_DELTA_PROMPT
from providers.llm.provider_factory import get_llm_provider


class PlaylistUploadAnalysisAgent(BaseAgent):
    name = "playlist_upload_analysis_agent"

    def __init__(self) -> None:
        self._llm = get_llm_provider()

    async def run(self, ctx: AgentContext) -> AgentResult:
        tracks: list[dict[str, Any]] = ctx.payload.get("tracks", [])
        track_list = "\n".join(f"{t.get('title')} — {t.get('artist')}" for t in tracks[:100])

        raw = await self._llm.complete(
            "You output only strict JSON.",
            GENRE_MOOD_TAGGING_PROMPT.format(track_list=track_list or "No tracks provided"),
            model_tier="fast",
            json_mode=True,
            temperature=0.2,
            max_tokens=600,
        )
        try:
            breakdown = json.loads(raw)
        except json.JSONDecodeError:
            breakdown = {"genre_breakdown": {}, "mood_breakdown": {}}

        summary = await self._llm.complete(
            "You are a concise, warm music analyst.",
            TASTE_DELTA_PROMPT.format(
                existing_profile=ctx.shared_state.get("genre_affinity", {}),
                new_breakdown=breakdown.get("genre_breakdown", {}),
            ),
            model_tier="fast",
            temperature=0.5,
            max_tokens=120,
        )

        return AgentResult(
            agent_name=self.name,
            data={
                "genre_breakdown": breakdown.get("genre_breakdown", {}),
                "mood_breakdown": breakdown.get("mood_breakdown", {}),
                "taste_delta_summary": summary,
            },
            trace={"track_count": len(tracks)},
        )
