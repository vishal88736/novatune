"""
Mood Agent — Analyzes user text input to extract emotional state,
energy level, intent, and music style recommendation.
Uses OpenAI / Gemini API via abstracted LLM service.
"""

import json
import re
from typing import Dict, Any
from services.llm_service import call_llm
from models.schemas import MoodAnalysis, EnergyLevel, Intent


MOOD_SYSTEM_PROMPT = """You are an expert emotional music psychologist and AI music therapist.
Analyze the user's text and extract their emotional state for music recommendation.

Always respond with ONLY valid JSON — no markdown, no explanation, just JSON.

Return this exact structure:
{
  "mood": "<primary emotion: tired|anxious|happy|sad|energized|calm|angry|melancholic|hopeful|stressed|bored|excited|nostalgic|neutral>",
  "energy": "<low|medium|high>",
  "intent": "<focus|relax|workout|sleep|party|explore|heal>",
  "music_style": "<descriptive style e.g. 'ambient lo-fi instrumental' or 'upbeat electronic pop'>",
  "productivity_need": <float 0.0-1.0>,
  "relaxation_level": <float 0.0-1.0>,
  "emotional_keywords": ["<keyword1>", "<keyword2>"],
  "reasoning": "<one sentence explanation>"
}

Consider:
- Time-of-day cues ("late night", "morning")
- Task cues ("studying", "working out", "driving")
- Intensity cues ("exhausted", "a little", "very")
- Multiple emotions simultaneously
"""


async def analyze_mood(user_input: str, context: Dict[str, Any] = None) -> MoodAnalysis:
    """
    Analyze user's text input and return a structured MoodAnalysis.
    
    Args:
        user_input: Free-form text describing how the user feels
        context: Optional dict with extra context (time_of_day, previous_mood, etc.)
    
    Returns:
        MoodAnalysis pydantic model
    """
    context_str = ""
    if context:
        context_str = f"\n\nAdditional context: {json.dumps(context)}"
    
    prompt = f"User says: \"{user_input}\"{context_str}\n\nAnalyze this and return JSON."
    
    raw_response = await call_llm(
        system_prompt=MOOD_SYSTEM_PROMPT,
        user_prompt=prompt,
        max_tokens=500,
    )
    
    # Parse LLM JSON response safely
    parsed = _safe_parse_json(raw_response)
    
    return MoodAnalysis(
        mood=parsed.get("mood", "neutral"),
        energy=EnergyLevel(parsed.get("energy", "medium")),
        intent=Intent(parsed.get("intent", "explore")),
        music_style=parsed.get("music_style", "instrumental"),
        productivity_need=float(parsed.get("productivity_need", 0.5)),
        relaxation_level=float(parsed.get("relaxation_level", 0.5)),
        raw_input=user_input,
    )


def _safe_parse_json(raw: str) -> Dict[str, Any]:
    """Safely parse JSON from LLM output, handling markdown fences."""
    # Strip markdown code fences if present
    clean = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
    
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        # Fallback: extract JSON block via regex
        match = re.search(r"\{.*\}", clean, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass
    
    # Ultimate fallback
    return {
        "mood": "neutral",
        "energy": "medium",
        "intent": "explore",
        "music_style": "instrumental",
        "productivity_need": 0.5,
        "relaxation_level": 0.5,
    }