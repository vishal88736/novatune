"""
Interaction API — POST /track-interaction
Real-time behavior tracking to adapt playlists.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from agents.memory_agent import record_interaction, record_listening
from agents.sequencing_agent import adapt_sequence_from_behavior
from database.connection import get_db
from models.schemas import InteractionEvent, InteractionType, ListeningHistoryEntry, Track

router = APIRouter()


class TrackInteractionRequest(BaseModel):
    user_id: str
    playlist_id: str
    track_youtube_id: str
    interaction: str   # play|skip|replay|like|dislike|complete
    listen_duration_seconds: Optional[int] = None
    current_index: Optional[int] = None    # position in playlist
    consecutive_skips: Optional[int] = 0
    skip_pattern: Optional[str] = None    # slow|fast|emotional


@router.post("/track-interaction")
async def track_interaction(request: TrackInteractionRequest):
    """
    Record a user interaction with a track.
    Triggers real-time playlist adaptation if needed.
    """
    try:
        interaction_type = InteractionType(request.interaction)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid interaction type: {request.interaction}")
    
    event = InteractionEvent(
        user_id=request.user_id,
        playlist_id=request.playlist_id,
        track_youtube_id=request.track_youtube_id,
        interaction=interaction_type,
        listen_duration_seconds=request.listen_duration_seconds,
    )
    
    await record_interaction(event)
    
    # Handle real-time playlist adaptation
    adapted_playlist = None
    db = get_db()
    
    if (
        interaction_type == InteractionType.skip
        and request.consecutive_skips >= 2
        and request.skip_pattern
        and db
    ):
        # Fetch current playlist and reorder
        playlist_doc = await db.generated_playlists.find_one({"playlist_id": request.playlist_id})
        if playlist_doc:
            tracks = [Track(**t) for t in playlist_doc.get("tracks", [])]
            new_order = adapt_sequence_from_behavior(
                current_playlist=tracks,
                skip_count=request.consecutive_skips,
                current_index=request.current_index or 0,
                skip_pattern=request.skip_pattern,
            )
            # Save adapted order
            await db.generated_playlists.update_one(
                {"playlist_id": request.playlist_id},
                {"$set": {"tracks": [t.dict() for t in new_order], "adapted": True}},
            )
            adapted_playlist = [
                {"youtube_id": t.youtube_id, "title": t.title, "artist": t.artist}
                for t in new_order[request.current_index or 0:]
            ]
    
    # Record to listening history
    if interaction_type in (InteractionType.complete, InteractionType.play) and db:
        track_doc = await db.generated_playlists.find_one(
            {"playlist_id": request.playlist_id},
            {"tracks": 1, "mood_snapshot": 1},
        )
        if track_doc:
            track_data = next(
                (t for t in track_doc.get("tracks", []) if t.get("youtube_id") == request.track_youtube_id),
                None
            )
            if track_data:
                mood = track_doc.get("mood_snapshot", {})
                entry = ListeningHistoryEntry(
                    user_id=request.user_id,
                    track=Track(**track_data),
                    context_mood=mood.get("mood"),
                    context_intent=mood.get("intent"),
                    listen_percentage=min(1.0, (request.listen_duration_seconds or 0) / max(track_data.get("duration_seconds", 180), 1)),
                )
                await record_listening(entry)
    
    response = {
        "status": "recorded",
        "interaction": request.interaction,
        "track_youtube_id": request.track_youtube_id,
    }
    
    if adapted_playlist:
        response["playlist_adapted"] = True
        response["new_queue"] = adapted_playlist
    
    return response