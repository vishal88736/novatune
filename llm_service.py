"""
LLM Service — Abstracted interface supporting OpenAI GPT and Google Gemini.
Set LLM_PROVIDER in .env to switch between providers.
"""

import os
import asyncio
from typing import Optional
import httpx
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # "openai" or "gemini"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")


async def call_llm(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 500,
    temperature: float = 0.7,
) -> str:
    """
    Call the configured LLM provider with a system + user prompt.
    
    Args:
        system_prompt: System/instruction prompt
        user_prompt: User message
        max_tokens: Maximum tokens in response
        temperature: Creativity level (0.0 = deterministic, 1.0 = creative)
    
    Returns:
        Raw text response from the LLM
    """
    if LLM_PROVIDER == "gemini":
        return await _call_gemini(system_prompt, user_prompt, max_tokens, temperature)
    else:
        return await _call_openai(system_prompt, user_prompt, max_tokens, temperature)


async def _call_openai(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
    temperature: float,
) -> str:
    """Call OpenAI Chat Completions API."""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not set in environment")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": OPENAI_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
        )
        
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


async def _call_gemini(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
    temperature: float,
) -> str:
    """Call Google Gemini API."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set in environment")
    
    full_prompt = f"{system_prompt}\n\n{user_prompt}"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent",
            params={"key": GEMINI_API_KEY},
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{"parts": [{"text": full_prompt}]}],
                "generationConfig": {
                    "maxOutputTokens": max_tokens,
                    "temperature": temperature,
                },
            },
        )
        
        response.raise_for_status()
        data = response.json()
        
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as e:
            raise ValueError(f"Unexpected Gemini response structure: {e}")