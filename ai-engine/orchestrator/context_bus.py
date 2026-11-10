"""
Redis-backed short-term context shared by every agent invoked within a
single conversational turn — avoids each agent redundantly re-fetching the
same user/session state (current mood, recent memory excerpt, etc).
"""

import json
from typing import Any, cast

from redis.asyncio import Redis

from service.config import settings

TTL_SECONDS = 60 * 60


class ContextBus:
    def __init__(self) -> None:
        self._redis = Redis.from_url(settings.redis_url, decode_responses=True)

    def _key(self, session_id: str) -> str:
        return f"session:ctx:{session_id}"

    async def get(self, session_id: str) -> dict[str, Any]:
        raw = await self._redis.get(self._key(session_id))
        return cast(dict[str, Any], json.loads(raw)) if raw else {}

    async def update(self, session_id: str, patch: dict[str, Any]) -> dict[str, Any]:
        current = await self.get(session_id)
        current.update(patch)
        await self._redis.set(self._key(session_id), json.dumps(current), ex=TTL_SECONDS)
        return current

    async def clear(self, session_id: str) -> None:
        await self._redis.delete(self._key(session_id))


context_bus = ContextBus()
