"""
Tracks API — GET /latest-tracks
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from agents.discovery_agent import get_trending_tracks, discover_tracks
from agents.mood_agent import analyze_mood

router = APIRouter()


@router.get("/latest-tracks")
async def get_latest_tracks(
    genre: Optional[str] = Query(None, description="Genre filter"),
    mood_text: Optional[str] = Query(None, description="Mood context for personalization"),
    discovery_type: str = Query("latest", description="latest|hidden_gems|niche|global"),
    count: int = Query(15, ge=1, le=50),
):
    """
    Fetch latest trending or discovery tracks.
    Optionally personalized by mood text.
    """
    if mood_text:
        mood = await analyze_mood(mood_text)
        tracks = await discover_tracks(
            mood=mood,
            taste_profile=None,
            discovery_type=discovery_type,
            count=count,
        )
    else:
        tracks = await get_trending_tracks(genre=genre, max_results=count)
    
    return {
        "tracks": [t.dict() for t in tracks],
        "count": len(tracks),
        "discovery_type": discovery_type,
    }