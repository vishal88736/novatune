"""
Memory Agent — Manages persistent user behavior memory.
Tracks skips, replays, favorites, listening patterns, and emotional habits.
Updates the user's taste profile dynamically.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from database.connection import get_db
from models.schemas import (
    InteractionEvent, InteractionType, TasteProfile,
    ListeningHistoryEntry, Track
)


async def record_interaction(event: InteractionEvent) -> None:
    """Store a single interaction event in MongoDB."""
    db = get_db()
    await db.interactions.insert_one(event.dict())
    
    # Trigger profile update on significant events
    if event.interaction in (InteractionType.skip, InteractionType.like, InteractionType.complete):
        await _update_taste_profile_from_interaction(event)


async def get_user_memory(user_id: str) -> Dict[str, Any]:
    """
    Retrieve aggregated behavioral memory for a user.
    Returns insights useful for recommendation agents.
    """
    db = get_db()
    
    # Fetch recent interactions (last 30 days)
    cutoff = datetime.utcnow() - timedelta(days=30)
    interactions = await db.interactions.find(
        {"user_id": user_id, "timestamp": {"$gte": cutoff}}
    ).to_list(length=500)
    
    # Compute behavioral stats
    memory = {
        "user_id": user_id,
        "skip_patterns": _analyze_skips(interactions),
        "replay_tracks": _find_replayed_tracks(interactions),
        "time_patterns": _analyze_time_patterns(interactions),
        "liked_tracks": _get_liked_tracks(interactions),
        "total_interactions": len(interactions),
    }
    
    return memory


async def get_history_ids(user_id: str, limit: int = 100) -> List[str]:
    """Get YouTube IDs of recently heard tracks to avoid repetition."""
    db = get_db()
    cutoff = datetime.utcnow() - timedelta(days=7)
    
    history = await db.listening_history.find(
        {"user_id": user_id, "listened_at": {"$gte": cutoff}},
        {"track.youtube_id": 1, "_id": 0}
    ).limit(limit).to_list(length=limit)
    
    return [h["track"]["youtube_id"] for h in history if h.get("track")]


async def record_listening(entry: ListeningHistoryEntry) -> None:
    """Add a track to the user's listening history."""
    db = get_db()
    await db.listening_history.insert_one(entry.dict())


async def _update_taste_profile_from_interaction(event: InteractionEvent) -> None:
    """Incrementally update user taste profile based on a single interaction."""
    db = get_db()
    
    # Retrieve the track details from generated playlists
    playlist = await db.generated_playlists.find_one({"playlist_id": event.playlist_id})
    if not playlist:
        return
    
    track_data = next(
        (t for t in playlist.get("tracks", []) if t.get("youtube_id") == event.track_youtube_id),
        None
    )
    if not track_data:
        return
    
    user = await db.users.find_one({"user_id": event.user_id})
    if not user:
        return
    
    profile = user.get("taste_profile", {})
    updates: Dict[str, Any] = {}
    
    if event.interaction == InteractionType.like:
        # Boost artist and genres
        artist = track_data.get("artist", "")
        if artist:
            top_artists = profile.get("top_artists", [])
            if artist not in top_artists:
                top_artists.insert(0, artist)
            updates["taste_profile.top_artists"] = top_artists[:20]
        
        for genre in track_data.get("genre_tags", []):
            top_genres = profile.get("top_genres", [])
            if genre not in top_genres:
                top_genres.insert(0, genre)
            updates["taste_profile.top_genres"] = top_genres[:15]
    
    elif event.interaction == InteractionType.skip:
        # Note skipped genres
        for genre in track_data.get("genre_tags", []):
            skipped = profile.get("skipped_genres", [])
            if genre not in skipped:
                skipped.append(genre)
            updates["taste_profile.skipped_genres"] = skipped[:10]
    
    if updates:
        updates["taste_profile.updated_at"] = datetime.utcnow()
        await db.users.update_one(
            {"user_id": event.user_id},
            {"$set": updates}
        )


def _analyze_skips(interactions: List[Dict]) -> Dict[str, int]:
    """Count skips by hour of day to detect skip patterns."""
    hourly_skips: Dict[str, int] = {}
    for i in interactions:
        if i.get("interaction") == InteractionType.skip:
            hour = i.get("timestamp", datetime.utcnow()).hour
            key = f"{hour:02d}:00"
            hourly_skips[key] = hourly_skips.get(key, 0) + 1
    return hourly_skips


def _find_replayed_tracks(interactions: List[Dict]) -> List[str]:
    """Find tracks that were replayed (strong positive signal)."""
    replayed = []
    for i in interactions:
        if i.get("interaction") == InteractionType.replay:
            tid = i.get("track_youtube_id")
            if tid and tid not in replayed:
                replayed.append(tid)
    return replayed


def _analyze_time_patterns(interactions: List[Dict]) -> Dict[str, str]:
    """Detect time-of-day listening preferences."""
    hour_counts: Dict[str, int] = {}
    for i in interactions:
        ts = i.get("timestamp", datetime.utcnow())
        hour = ts.hour if isinstance(ts, datetime) else 12
        if 5 <= hour < 12:
            period = "morning"
        elif 12 <= hour < 17:
            period = "afternoon"
        elif 17 <= hour < 21:
            period = "evening"
        else:
            period = "night"
        hour_counts[period] = hour_counts.get(period, 0) + 1
    
    if not hour_counts:
        return {"peak_time": "evening"}
    
    peak = max(hour_counts, key=hour_counts.get)
    return {"peak_time": peak, "distribution": hour_counts}


def _get_liked_tracks(interactions: List[Dict]) -> List[str]:
    """Return list of explicitly liked track IDs."""
    return [
        i["track_youtube_id"] for i in interactions
        if i.get("interaction") == InteractionType.like and i.get("track_youtube_id")
    ]