"""
Arranges a candidate track list into an emotional arc rather than leaving
them in raw rank order. Arc shapes:
  - "build": gradually increasing energy (workout, motivation)
  - "wind_down": gradually decreasing energy (evening, post-stress)
  - "plateau": sustained energy near the target (focus, steady mood)
  - "steady": default light shaping when no explicit arc is requested
"""

from typing import Any

from agents.base import AgentContext, AgentResult, BaseAgent


class SequencingAgent(BaseAgent):
    name = "sequencing_agent"

    def _energy_proxy(self, track: dict[str, Any]) -> float:
        # Placeholder: production reads a stored energy/tempo feature per
        # track (derived at ingestion time) rather than duration.
        duration = track.get("duration_seconds", 200)
        return float(duration % 60) / 60

    async def run(self, ctx: AgentContext) -> AgentResult:
        tracks: list[dict[str, Any]] = ctx.shared_state.get("candidate_tracks", [])
        target_arc = ctx.payload.get("target_arc", "steady")

        scored = [(t, self._energy_proxy(t)) for t in tracks]

        if target_arc == "build":
            scored.sort(key=lambda x: x[1])
        elif target_arc == "wind_down":
            scored.sort(key=lambda x: -x[1])
        # "plateau" / "steady": keep original relevance order

        ordered_ids = [t["id"] for t, _ in scored]

        return AgentResult(
            agent_name=self.name,
            data={"ordered_track_ids": ordered_ids, "arc_label": target_arc},
            trace={"track_count": len(ordered_ids)},
        )
