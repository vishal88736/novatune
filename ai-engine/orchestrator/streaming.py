"""
Formats agent output as Server-Sent Events consumed by website/backend's
/chat/message endpoint, which streams straight through to the browser.
"""

import json
from collections.abc import AsyncGenerator


def sse_event(event_type: str, **fields) -> bytes:
    payload = json.dumps({"type": event_type, **fields})
    return f"data: {payload}\n\n".encode()


async def format_stream(token_generator: AsyncGenerator[str, None]) -> AsyncGenerator[bytes, None]:
    async for token in token_generator:
        yield sse_event("token", content=token)
    yield sse_event("done")
