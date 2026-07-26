"""
Groq implementation of LLMProvider. Groq's LPU inference gives very low
first-token latency, which is why the 'fast' tier (llama-3.1-8b-instant) is
used for anything user-latency-sensitive (mood tagging, explanations,
re-ranking), while the 'reasoning' tier (llama-3.3-70b-versatile) is
reserved for the Conversation Agent's actual dialogue turns.
"""

import io
from collections.abc import AsyncGenerator

from groq import AsyncGroq

from providers.llm.base_provider import LLMProvider
from service.config import settings


class GroqProvider(LLMProvider):
    def __init__(self) -> None:
        self._client = AsyncGroq(api_key=settings.groq_api_key)
        self._models = {
            "fast": settings.groq_fast_model,
            "reasoning": settings.groq_conversation_model,
        }

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
        response = await self._client.chat.completions.create(
            model=self._models[model_tier],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"} if json_mode else None,
        )
        return response.choices[0].message.content or ""

    async def stream(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        model_tier: str = "reasoning",
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        stream = await self._client.chat.completions.create(
            model=self._models[model_tier],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    async def transcribe(self, audio_bytes: bytes, filename: str = "audio.wav") -> str:
        buffer = io.BytesIO(audio_bytes)
        buffer.name = filename
        transcription = await self._client.audio.transcriptions.create(
            file=buffer,
            model=settings.groq_whisper_model,
        )
        return transcription.text


groq_provider = GroqProvider()
