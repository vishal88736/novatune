"""
The Conversation Agent is VibeAI's entry point and "face" — it classifies
intent, streams a natural reply, and (via the orchestrator's planner) fans
out to whichever specialist agents the turn actually needs.
"""

import json
from collections.abc import AsyncGenerator

from agents.base import AgentContext, AgentResult, BaseAgent
from agents.conversation_agent.prompts import INTENT_CLASSIFICATION_PROMPT, SYSTEM_PROMPT
from orchestrator.context_bus import context_bus
from orchestrator.planner import plan_for_intent
from providers.llm.provider_factory import get_llm_provider


class ConversationAgent(BaseAgent):
    name = "conversation_agent"

    def __init__(self) -> None:
        self._llm = get_llm_provider()

    async def classify_intent(self, message: str) -> str:
        raw = await self._llm.complete(
            SYSTEM_PROMPT,
            INTENT_CLASSIFICATION_PROMPT.format(message=message),
            model_tier="fast",
            json_mode=True,
            temperature=0.1,
            max_tokens=50,
        )
        try:
            return json.loads(raw).get("intent", "chit_chat")
        except json.JSONDecodeError:
            return "chit_chat"

    async def run(self, ctx: AgentContext) -> AgentResult:
        message = ctx.payload.get("message", "")
        intent = await self.classify_intent(message)
        agents_to_run = plan_for_intent(intent)

        reply = await self._llm.complete(SYSTEM_PROMPT, message, model_tier="reasoning")

        if ctx.session_id:
            await context_bus.update(ctx.session_id, {"last_intent": intent})

        return AgentResult(
            agent_name=self.name,
            data={"reply": reply, "intent": intent, "agents_invoked": agents_to_run},
            trace={"intent": intent},
        )

    async def stream_reply(self, ctx: AgentContext) -> AsyncGenerator[str, None]:
        message = ctx.payload.get("message", "")
        async for token in self._llm.stream(SYSTEM_PROMPT, message, model_tier="reasoning"):
            yield token
