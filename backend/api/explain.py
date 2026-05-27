"""
Explain API — POST /explain-song
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from agents.explanation_agent import explain_recommendation
from agents.memory_agent import get_user_memory
from agents.mood_agent import analyze_mood
from database.connection import get_db
from models.schemas import Track, TasteProfile

router = APIRouter()


class ExplainRequest(BaseModel):
    user_id: str
    youtube_id: str
    title: str
    artist: str
    mood_text: Optional[str] = None
    mood_tags: Optional[List[str]] = []
    genre_tags: Optional[List[str]] = []
    is_hidden_gem: Optional[bool] = False


@router.post("/explain-song")
async def explain_song(request: ExplainRequest):
    """
    Generate a personalized explanation for why a specific track was recommended.
    
    Returns a human-readable sentence explaining the recommendation.
    """
    db = get_db()
    
    # Build track object
    track = Track(
        youtube_id=request.youtube_id,
        title=request.title,
        artist=request.artist,
        channel="",
        mood_tags=request.mood_tags or [],
        genre_tags=request.genre_tags or [],
        is_hidden_gem=request.is_hidden_gem or False,
    )
    
    # Get mood context
    if request.mood_text:
        mood = await analyze_mood(request.mood_text)
    else:
        mood = await analyze_mood("I want to discover music")
    
    # Get user context
    taste_profile = None
    user_memory = {}
    
    if db is not None:
        user = await db.users.find_one({"user_id": request.user_id}, {"_id": 0})
        if user and user.get("taste_profile"):
            taste_profile = TasteProfile(**user["taste_profile"])
        
        user_memory = await get_user_memory(request.user_id)
    
    try:
        explanation = await explain_recommendation(
            track=track,
            mood=mood,
            taste_profile=taste_profile,
            user_memory=user_memory,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explanation failed: {str(e)}")
    
    return {
        "youtube_id": request.youtube_id,
        "title": request.title,
        "artist": request.artist,
        "explanation": explanation,
    }