"""
Mood API — POST /analyze-mood
"""

from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import Optional, Dict, Any
from agents.mood_agent import analyze_mood
from database.connection import get_db
from datetime import datetime
import uuid

router = APIRouter()


class MoodRequest(BaseModel):
    user_id: str
    text: str
    context: Optional[Dict[str, Any]] = None  # e.g. {"time_of_day": "evening"}


class MoodResponse(BaseModel):
    mood: str
    energy: str
    intent: str
    music_style: str
    productivity_need: float
    relaxation_level: float
    raw_input: str


@router.post("/analyze-mood", response_model=MoodResponse)
async def analyze_mood_endpoint(request: MoodRequest):
    """
    Analyze user's text input to detect emotional state and music needs.
    
    Example input:
      { "user_id": "user123", "text": "I feel mentally exhausted but need to study" }
    
    Example output:
      { "mood": "tired", "energy": "low", "intent": "focus", "music_style": "ambient lo-fi" }
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text input cannot be empty")
    
    try:
        analysis = await analyze_mood(request.text, request.context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mood analysis failed: {str(e)}")
    
    # Persist to mood history
    db = get_db()
    if db is not None:
        await db.mood_history.insert_one({
            "entry_id": str(uuid.uuid4()),
            "user_id": request.user_id,
            "analysis": analysis.dict(),
            "playlist_generated": False,
            "created_at": datetime.utcnow(),
        })
    
    return MoodResponse(
        mood=analysis.mood,
        energy=analysis.energy.value,
        intent=analysis.intent.value,
        music_style=analysis.music_style,
        productivity_need=analysis.productivity_need,
        relaxation_level=analysis.relaxation_level,
        raw_input=request.text,
    )