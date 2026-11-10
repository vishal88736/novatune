"""Provider-agnostic LLM interface. Agents depend only on this contract,
never on a concrete vendor SDK, so the backing model can be swapped via
config without touching agent logic."""

from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator


class LLMProvider(ABC):
    @abstractmethod
    async def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        model_tier: str = "fast",
        json_mode: bool = False,
        temperature: float = 0.6,
        max_tokens: int = 1024,
    ) -> str:
        """Single-shot completion. `model_tier` is 'fast' or 'reasoning'."""

    @abstractmethod
    async def stream(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        model_tier: str = "reasoning",
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        """Token-by-token streaming completion, used by the Conversation Agent."""
        # Declared as an async generator so subclasses that `yield` match
        # this signature; the body is never executed.
        if False:  # pragma: no cover
            yield ""

    @abstractmethod
    async def transcribe(self, audio_bytes: bytes, filename: str = "audio.wav") -> str:
        """Speech-to-text transcription."""
