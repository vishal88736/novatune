from agents.base import AgentContext
from orchestrator.context_bus import context_bus


async def build_context(user_id: str, session_id: str | None, payload: dict) -> AgentContext:
    shared_state = await context_bus.get(session_id) if session_id else {}
    return AgentContext(user_id=user_id, session_id=session_id, payload=payload, shared_state=shared_state)
