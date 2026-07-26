import pytest

from agents.base import AgentContext
from agents.discovery_agent.agent import DiscoveryAgent


@pytest.mark.asyncio
async def test_discovery_filters_high_popularity_tracks():
    agent = DiscoveryAgent()
    tracks = [
        {"id": "mainstream", "popularity_score": 0.9},
        {"id": "hidden", "popularity_score": 0.1},
    ]
    ctx = AgentContext(user_id="u1", payload={}, shared_state={"candidate_tracks": tracks})
    result = await agent.run(ctx)
    ids = [t["id"] for t in result.data["tracks"]]
    assert "hidden" in ids
    assert "mainstream" not in ids
