"""
Recommendation Agent — Combines mood analysis, taste profile, and
listening history to generate YouTube search queries and rank tracks.
"""

import os
import asyncio
from typing import List, Dict, Any, Optional
from models.schemas import MoodAnalysis, Track, TasteProfile, EnergyLevel
from services.youtube_service import search_youtube, get_video_details
from services.llm_service import call_llm
import json
import re


QUERY_BUILDER_PROMPT = """You are a music curation expert.
Given a mood analysis and user taste profile, generate 5-8 YouTube search queries
to find the best matching music tracks.

Return ONLY a JSON array of search query strings.
Example: ["lo-fi hip hop study beats", "ambient piano focus music 2024"]

Rules:
- Mix popular and obscure/hidden gem queries
- Include genre + mood descriptors
- Add year hints for latest tracks (2023, 2024, 2025)
- Include instrumental-only queries when intent is focus/study
- Vary query styles to get diverse results
"""


async def generate_recommendations(
    mood: MoodAnalysis,
    taste_profile: Optional[TasteProfile],
    history_youtube_ids: List[str] = [],
    max_tracks: int = 20,
    include_hidden_gems: bool = True,
) -> List[Track]:
    """
    Generate a list of recommended Track objects.
    
    Args:
        mood: Analyzed mood from MoodAgent
        taste_profile: User's stored taste profile
        history_youtube_ids: IDs to exclude (already heard)
        max_tracks: Maximum number of tracks to return
        include_hidden_gems: Whether to include underrated artists
    
    Returns:
        List of Track objects sorted by relevance
    """
    # Step 1: Build smart search queries using LLM
    queries = await _build_search_queries(mood, taste_profile)
    
    # Step 2: Search YouTube in parallel
    all_results: List[Dict] = []
    search_tasks = [search_youtube(q, max_results=5) for q in queries]
    search_batches = await asyncio.gather(*search_tasks, return_exceptions=True)
    
    for batch in search_batches:
        if isinstance(batch, list):
            all_results.extend(batch)
    
    # Step 3: Deduplicate by video ID
    seen_ids = set(history_youtube_ids)
    unique_results = []
    for result in all_results:
        vid_id = result.get("youtube_id")
        if vid_id and vid_id not in seen_ids:
            seen_ids.add(vid_id)
            unique_results.append(result)
    
    # Step 4: Score and rank results
    scored_tracks = _score_tracks(unique_results, mood, taste_profile)
    
    # Step 5: Convert to Track models
    tracks = []
    for item in scored_tracks[:max_tracks]:
        track = Track(
            youtube_id=item["youtube_id"],
            title=item.get("title", "Unknown"),
            artist=item.get("artist", "Unknown"),
            channel=item.get("channel", ""),
            thumbnail=item.get("thumbnail"),
            duration_seconds=item.get("duration_seconds"),
            genre_tags=item.get("genre_tags", []),
            mood_tags=_derive_mood_tags(mood),
            energy_level=mood.energy,
            is_hidden_gem=item.get("is_hidden_gem", False),
            popularity_score=item.get("popularity_score", 0.5),
        )
        tracks.append(track)
    
    return tracks


async def _build_search_queries(
    mood: MoodAnalysis,
    taste_profile: Optional[TasteProfile],
) -> List[str]:
    """Use LLM to generate diverse, smart YouTube search queries."""
    
    profile_summary = ""
    if taste_profile:
        profile_summary = f"""
User taste profile:
- Top genres: {', '.join(taste_profile.top_genres[:5])}
- Top artists: {', '.join(taste_profile.top_artists[:5])}
- BPM preference: {taste_profile.bpm_preference}
- Mainstream score: {taste_profile.mainstream_score} (0=underground, 1=mainstream)
- Avoid genres: {', '.join(taste_profile.skipped_genres[:3])}
"""
    
    prompt = f"""
Mood analysis:
- Mood: {mood.mood}
- Energy: {mood.energy}
- Intent: {mood.intent}
- Music style: {mood.music_style}
- Productivity need: {mood.productivity_need}
- Relaxation level: {mood.relaxation_level}

{profile_summary}

Generate search queries to find perfect music for this user right now.
Return ONLY a JSON array of strings.
"""
    
    raw = await call_llm(
        system_prompt=QUERY_BUILDER_PROMPT,
        user_prompt=prompt,
        max_tokens=300,
    )
    
    # Parse query list
    clean = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
    try:
        queries = json.loads(clean)
        if isinstance(queries, list):
            return [str(q) for q in queries[:8]]
    except Exception:
        pass
    
    # Fallback queries based on mood
    return [
        f"{mood.music_style} music",
        f"{mood.mood} {mood.intent} music 2024",
        f"{mood.energy} energy {mood.intent} playlist",
    ]


def _score_tracks(
    results: List[Dict],
    mood: MoodAnalysis,
    taste_profile: Optional[TasteProfile],
) -> List[Dict]:
    """Score and sort tracks by relevance to mood and taste."""
    
    for item in results:
        score = 0.5  # base score
        title_lower = (item.get("title", "") + " " + item.get("channel", "")).lower()
        
        # Boost if matches user's top artists
        if taste_profile:
            for artist in taste_profile.top_artists:
                if artist.lower() in title_lower:
                    score += 0.3
            
            # Penalize skipped genres
            for genre in taste_profile.skipped_genres:
                if genre.lower() in title_lower:
                    score -= 0.2
        
        # Hidden gem detection (low view count = underrated)
        view_count = item.get("view_count", 0)
        if view_count and view_count < 500_000:
            item["is_hidden_gem"] = True
            item["popularity_score"] = 0.2
            score += 0.1  # slight boost for discovery
        else:
            item["is_hidden_gem"] = False
            item["popularity_score"] = min(1.0, (view_count or 1_000_000) / 10_000_000)
        
        item["_score"] = score
    
    return sorted(results, key=lambda x: x.get("_score", 0), reverse=True)


def _derive_mood_tags(mood: MoodAnalysis) -> List[str]:
    """Generate mood tags from mood analysis."""
    tags = [mood.mood, mood.intent.value]
    if mood.energy == EnergyLevel.low:
        tags.append("calm")
    elif mood.energy == EnergyLevel.high:
        tags.append("energetic")
    return tags