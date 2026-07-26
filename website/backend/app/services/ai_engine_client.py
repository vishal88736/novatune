"""
Typed HTTP client for website/backend -> ai-engine/service.

This is the ONLY way website/backend talks to the AI/agent layer. It never
imports Groq, Qdrant, or Sentence Transformer clients directly — those live
exclusively inside ai-engine, so the "brain" can be redeployed, rescaled, or
swapped independently of the product API.
"""

from collections.abc import AsyncGenerator

import httpx

from app.core.config import settings
from app.core.exceptions import AIEngineUnavailableError


class AIEngineClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or settings.ai_engine_base_url

    async def invoke_agent(self, agent_name: str, payload: dict) -> dict:
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                resp = await client.post(f"{self.base_url}/agents/{agent_name}/invoke", json=payload)
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPError as exc:
                raise AIEngineUnavailableError() from exc

    async def stream_conversation(
        self, session_id: str, user_id: str, message: str
    ) -> AsyncGenerator[bytes, None]:
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/agents/conversation_agent/stream",
                json={"session_id": session_id, "user_id": user_id, "message": message},
            ) as resp:
                async for chunk in resp.aiter_bytes():
                    yield chunk

    async def run_recommendation_pipeline(self, user_id: str, mood_vector: dict) -> dict:
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                resp = await client.post(
                    f"{self.base_url}/pipeline/recommendation/run",
                    json={"user_id": user_id, "mood_vector": mood_vector},
                )
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPError as exc:
                raise AIEngineUnavailableError() from exc


ai_engine_client = AIEngineClient()
