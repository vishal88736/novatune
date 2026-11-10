"""
Formats agent output as Server-Sent Events consumed by website/backend's
/chat/message endpoint, which streams straight through to the browser.
"""

import json
import logging
from collections.abc import AsyncGenerator
from typing import Any

logger = logging.getLogger(__name__)


def sse_event(event_type: str, **fields: Any) -> bytes:
    payload = json.dumps({"type": event_type, **fields})
    return f"data: {payload}\n\n".encode()


async def format_stream(token_generator: AsyncGenerator[str, None]) -> AsyncGenerator[bytes, None]:
    """
    Streams tokens as SSE `token` events, terminated by a `done` event.

    If the agent fails mid-stream the failure is reported as an `error`
    event rather than being allowed to tear the connection down, so the
    client can tell the user what happened instead of waiting forever.
    """
    try:
        async for token in token_generator:
            yield sse_event("token", content=token)
    except Exception as exc:  # noqa: BLE001 - surfaced to the client as an event
        logger.exception("Agent stream failed")
        yield sse_event("error", message=str(exc) or exc.__class__.__name__)
        return
    yield sse_event("done")
