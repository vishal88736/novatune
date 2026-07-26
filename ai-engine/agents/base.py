"""
Every agent implements this uniform contract. No agent may reach into
another agent's internals — cross-agent communication happens only through
the shared AgentContext (backed by the Redis context bus) or through
explicit return values passed by the orchestrator.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentContext:
    user_id: str
    session_id: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    shared_state: dict[str, Any] = field(default_factory=dict)  # populated from context bus


@dataclass
class AgentResult:
    agent_name: str
    data: dict[str, Any]
    trace: dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    name: str = "base_agent"

    @abstractmethod
    async def run(self, ctx: AgentContext) -> AgentResult:
        """Executes the agent's core logic and returns a structured result."""
