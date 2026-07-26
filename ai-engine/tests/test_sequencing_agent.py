import pytest

from agents.base import AgentContext
from agents.sequencing_agent.agent import SequencingAgent


@pytest.mark.asyncio
async def test_build_arc_orders_ascending_by_energy_proxy():
    agent = SequencingAgent()
    tracks = [
        {"id": "a", "duration_seconds": 130},
        {"id": "b", "duration_seconds": 200},
        {"id": "c", "duration_seconds": 90},
    ]
    ctx = AgentContext(user_id="u1", payload={"target_arc": "build"}, shared_state={"candidate_tracks": tracks})
    result = await agent.run(ctx)
    assert len(result.data["ordered_track_ids"]) == 3
    assert result.data["arc_label"] == "build"
