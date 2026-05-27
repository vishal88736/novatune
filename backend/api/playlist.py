"""
Playlist API — POST /generate-playlist, POST /upload-playlist
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime

from agents.mood_agent import analyze_mood
from agents.recommendation_agent import generate_recommendations
from agents.sequencing_agent import sequence_playlist
from agents.discovery_agent import discover_tracks
from agents.explanation_agent import explain_playlist
from agents.playlist_analysis_agent import (
    analyze_youtube_playlist,
    analyze_csv_playlist,
    analyze_manual_playlist,
)
from agents.memory_agent import get_history_ids, get_user_memory
from database.connection import get_db
from models.schemas import MoodAnalysis, EnergyLevel, Intent

router = APIRouter()


class GeneratePlaylistRequest(BaseModel):
    user_id: str
    mood_text: str
    context: Optional[Dict[str, Any]] = None
    max_tracks: int = 20
    include_discovery: bool = True  # Include hidden gems
    include_latest: bool = True


class TrackOut(BaseModel):
    youtube_id: str
    title: str
    artist: str
    channel: str
    thumbnail: Optional[str] = None
    duration_seconds: Optional[int] = None
    mood_tags: List[str] = []
    is_hidden_gem: bool = False
    popularity_score: float = 0.5
    explanation: Optional[str] = None


class GeneratePlaylistResponse(BaseModel):
    playlist_id: str
    mood: Dict[str, Any]
    tracks: List[TrackOut]
    emotional_arc: List[str]
    playlist_overview: str
    track_count: int


@router.post("/generate-playlist", response_model=GeneratePlaylistResponse)
async def generate_playlist(request: GeneratePlaylistRequest):
    """
    Generate a full AI-curated playlist based on user's mood text.
    
    Flow:
    1. Analyze mood → 2. Fetch user memory → 3. Recommend tracks
    4. Discover hidden gems → 5. Sequence emotionally → 6. Explain
    """
    db = get_db()
    
    # Step 1: Analyze mood
    try:
        mood = await analyze_mood(request.mood_text, request.context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mood analysis failed: {str(e)}")
    
    # Step 2: Get user taste profile and history
    user_doc = None
    taste_profile = None
    if db is not None is not None:
        user_doc = await db.users.find_one({"user_id": request.user_id})
        if user_doc and user_doc.get("taste_profile"):
            from models.schemas import TasteProfile
            taste_profile = TasteProfile(**user_doc["taste_profile"])
    
    history_ids = await get_history_ids(request.user_id, limit=100) if db is not None is not None else []
    user_memory = await get_user_memory(request.user_id) if db is not None is not None else {}
    
    # Step 3: Generate recommendations
    main_tracks = await generate_recommendations(
        mood=mood,
        taste_profile=taste_profile,
        history_youtube_ids=history_ids,
        max_tracks=int(request.max_tracks * 0.75),
    )
    
    # Step 4: Add discovery tracks (hidden gems / latest)
    discovery = []
    if request.include_discovery:
        try:
            discovery = await discover_tracks(
                mood=mood,
                taste_profile=taste_profile,
                discovery_type="hidden_gems",
                count=int(request.max_tracks * 0.25),
                excluded_ids=history_ids + [t.youtube_id for t in main_tracks],
            )
        except Exception:
            pass  # Discovery is non-critical
    
    all_tracks = main_tracks + discovery
    
    if not all_tracks:
        raise HTTPException(status_code=404, detail="No tracks found for this mood. Try a different description.")
    
    # Step 5: Sequence emotionally
    ordered_tracks, emotional_arc = sequence_playlist(all_tracks, mood)
    
    # Step 6: Generate playlist overview
    try:
        overview = await explain_playlist(ordered_tracks, mood, emotional_arc)
    except Exception:
        overview = f"A {mood.music_style} playlist crafted for your {mood.mood} mood."
    
    # Step 7: Save to database
    playlist_id = str(uuid.uuid4())
    if db is not None:
        playlist_doc = {
            "playlist_id": playlist_id,
            "user_id": request.user_id,
            "mood_snapshot": mood.dict(),
            "tracks": [t.dict() for t in ordered_tracks],
            "emotional_arc": emotional_arc,
            "playlist_overview": overview,
            "created_at": datetime.utcnow(),
            "active": True,
        }
        await db.generated_playlists.insert_one(playlist_doc)
        
        # Update mood history to link playlist
        await db.mood_history.update_one(
            {"user_id": request.user_id, "playlist_generated": False},
            {"$set": {"playlist_generated": True, "generated_playlist_id": playlist_id}},
            
        )
    
    # Build response
    tracks_out = [
        TrackOut(
            youtube_id=t.youtube_id,
            title=t.title,
            artist=t.artist,
            channel=t.channel,
            thumbnail=t.thumbnail,
            duration_seconds=t.duration_seconds,
            mood_tags=t.mood_tags,
            is_hidden_gem=t.is_hidden_gem,
            popularity_score=t.popularity_score,
        )
        for t in ordered_tracks
    ]
    
    return GeneratePlaylistResponse(
        playlist_id=playlist_id,
        mood=mood.dict(),
        tracks=tracks_out,
        emotional_arc=emotional_arc,
        playlist_overview=overview,
        track_count=len(tracks_out),
    )


class UploadPlaylistRequest(BaseModel):
    user_id: str
    source: str          # "youtube_url" | "manual"
    playlist_url: Optional[str] = None
    songs: Optional[List[Dict[str, str]]] = None   # for "manual"


@router.post("/upload-playlist")
async def upload_playlist(request: UploadPlaylistRequest):
    """Upload a playlist URL or song list for taste profile analysis."""
    db = get_db()
    
    try:
        if request.source == "youtube_url" and request.playlist_url:
            taste_profile = await analyze_youtube_playlist(request.playlist_url)
        elif request.source == "manual" and request.songs:
            taste_profile = await analyze_manual_playlist(request.songs)
        else:
            raise HTTPException(status_code=400, detail="Provide either playlist_url or songs list")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Playlist analysis failed: {str(e)}")
    
    # Save/update taste profile in user document
    if db is not None:
        await db.users.update_one(
            {"user_id": request.user_id},
            {
                "$set": {
                    "taste_profile": taste_profile.dict(),
                    "last_active": datetime.utcnow(),
                },
                "$setOnInsert": {
                    "user_id": request.user_id,
                    "created_at": datetime.utcnow(),
                },
            },
            upsert=True,
        )
        
        # Archive the upload
        await db.uploaded_playlists.insert_one({
            "user_id": request.user_id,
            "source": request.source,
            "playlist_url": request.playlist_url,
            "analyzed_profile": taste_profile.dict(),
            "upload_timestamp": datetime.utcnow(),
        })
    
    return {
        "status": "success",
        "message": "Playlist analyzed and taste profile updated",
        "taste_profile": taste_profile.dict(),
    }


@router.post("/upload-playlist-csv")
async def upload_playlist_csv(
    user_id: str = Form(...),
    file: UploadFile = File(...),
):
    """Upload a CSV file for playlist analysis."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    content = await file.read()
    csv_text = content.decode("utf-8", errors="ignore")
    
    try:
        taste_profile = await analyze_csv_playlist(csv_text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CSV analysis failed: {str(e)}")
    
    db = get_db()
    if db is not None:
        await db.users.update_one(
            {"user_id": user_id},
            {"$set": {"taste_profile": taste_profile.dict(), "last_active": datetime.utcnow()}},
            upsert=True,
        )
    
    return {
        "status": "success",
        "message": f"CSV analyzed successfully",
        "taste_profile": taste_profile.dict(),
    }