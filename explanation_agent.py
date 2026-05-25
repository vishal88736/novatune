"""
Explanation Agent — Generates natural language explanations for
why a specific track was recommended to a user.
"""

from typing import Optional, Dict, Any
from models.schemas import Track, MoodAnalysis, TasteProfile
from services.llm_service import call_llm


EXPLAIN_SYSTEM_PROMPT = """You are a thoughtful AI music curator who explains recommendations with warmth and insight.
Write a single, natural sentence (max 30 words) explaining why this specific song was chosen for this user.
Mention the mood, their taste, or the emotional journey.
Be specific, human, and avoid clichés.
Return ONLY the explanation sentence — no quotes, no prefix."""


async def explain_recommendation(
    track: Track,
    mood: MoodAnalysis,
    taste_profile: Optional[TasteProfile],
    user_memory: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Generate a short, personalized explanation for why a track was recommended.
    
    Args:
        track: The recommended track
        mood: Current mood analysis
        taste_profile: User's taste profile
        user_memory: Aggregated behavioral memory
    
    Returns:
        A natural language explanation string
    """
    context_parts = []
    
    if taste_profile and taste_profile.top_genres:
        context_parts.append(f"User loves: {', '.join(taste_profile.top_genres[:3])}")
    
    if taste_profile and taste_profile.top_artists:
        context_parts.append(f"Favorite artists: {', '.join(taste_profile.top_artists[:3])}")
    
    if user_memory:
        peak_time = user_memory.get("time_patterns", {}).get("peak_time")
        if peak_time:
            context_parts.append(f"Typically listens at: {peak_time}")
        
        replays = user_memory.get("replay_tracks", [])
        if replays:
            context_parts.append(f"Has replayed {len(replays)} tracks recently")
    
    context = "\n".join(context_parts) if context_parts else "No additional context"
    
    prompt = f"""Track: "{track.title}" by {track.artist}
Track tags: {', '.join(track.mood_tags + track.genre_tags)}
Hidden gem: {track.is_hidden_gem}

Current mood: {mood.mood} | Energy: {mood.energy} | Intent: {mood.intent}
Music style sought: {mood.music_style}

{context}

Write one sentence explaining why this track was chosen."""
    
    explanation = await call_llm(
        system_prompt=EXPLAIN_SYSTEM_PROMPT,
        user_prompt=prompt,
        max_tokens=80,
    )
    
    return explanation.strip().strip('"').strip("'")


async def explain_playlist(
    tracks: list,
    mood: MoodAnalysis,
    emotional_arc: list,
) -> str:
    """
    Generate a brief explanation for the entire playlist.
    
    Args:
        tracks: List of tracks in the playlist
        mood: Mood that triggered the playlist
        emotional_arc: List of arc stage labels
    
    Returns:
        A multi-sentence playlist overview
    """
    arc_str = " → ".join(emotional_arc) if emotional_arc else "steady flow"
    track_count = len(tracks)
    hidden_count = sum(1 for t in tracks if t.is_hidden_gem)
    
    prompt = f"""Playlist overview:
- {track_count} tracks total, {hidden_count} hidden gems
- Emotional arc: {arc_str}
- User mood: {mood.mood}, seeking {mood.intent}
- Music style: {mood.music_style}

Write 2-3 sentences introducing this playlist to the user. Be warm, insightful, specific about the journey."""
    
    overview = await call_llm(
        system_prompt="You are a warm, poetic AI music curator. Write engaging playlist introductions.",
        user_prompt=prompt,
        max_tokens=150,
    )
    
    return overview.strip()