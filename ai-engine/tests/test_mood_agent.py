import pytest

from agents.base import AgentContext
from agents.mood_agent.agent import MoodAgent


@pytest.mark.asyncio
async def test_mood_agent_defaults_to_neutral_with_no_input():
    agent = MoodAgent()
    ctx = AgentContext(user_id="test-user", payload={})
    result = await agent.run(ctx)
    assert result.data["label"] == "Neutral"
    assert -1.0 <= result.data["valence"] <= 1.0
