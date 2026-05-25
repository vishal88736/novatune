"""
Discovery Agent — Finds fresh, trending, and hidden gem tracks.
Avoids repetitive mainstream recommendations.
"""

import asyncio
from typing import List, Dict, Any, Optional
from models.schemas import Track, MoodAnalysis, TasteProfile, EnergyLevel
from services.youtube_service import search_youtube


# Discovery query templates for different discovery types
DISCOVERY_TEMPLATES = {
    "hidden_gems": [
        "{genre} hidden gems 2024",
        "underrated {genre} artists",
        "{mood} underground {genre}",
        "lesser known {genre} music",
        "indie {genre} {mood}",
    ],
    "latest": [
        "{genre} new releases 2025",
        "trending {genre} 2024",
        "new {mood} music this month",
        "{genre} latest songs 2024",
    ],
    "niche": [
        "deep {genre} cuts",
        "experimental {genre} {mood}",
        "{genre} rarities",
        "obscure {genre} tracks",
    ],
    "global": [
        "world music {mood}",
        "global {genre} fusion",
        "non-english {mood} {genre}",
    ],
}


async def discover_tracks(
    mood: MoodAnalysis,
    taste_profile: Optional[TasteProfile],
    discovery_type: str = "hidden_gems",
    count: int = 10,
    excluded_ids: List[str] = [],
) -> List[Track]:
    """
    Discover fresh tracks based on mood and taste profile.
    
    Args:
        mood: Current mood analysis
        taste_profile: User taste profile for personalization
        discovery_type: One of "hidden_gems", "latest", "niche", "global"
        count: How many discovery tracks to return
        excluded_ids: YouTube IDs to exclude
    
    Returns:
        List of discovered Track objects
    """
    genre = _pick_genre(taste_profile, mood)
    queries = _build_discovery_queries(mood, genre, discovery_type)
    
    # Search in parallel
    tasks = [search_youtube(q, max_results=4) for q in queries[:5]]
    batches = await asyncio.gather(*tasks, return_exceptions=True)
    
    seen = set(excluded_ids)
    discovered: List[Track] = []
    
    for batch in batches:
        if not isinstance(batch, list):
            continue
        for item in batch:
            vid_id = item.get("youtube_id")
            if not vid_id or vid_id in seen:
                continue
            seen.add(vid_id)
            
            # Mark as hidden gem based on view count
            view_count = item.get("view_count", 0)
            is_gem = view_count < 300_000 if view_count else True
            
            track = Track(
                youtube_id=vid_id,
                title=item.get("title", ""),
                artist=item.get("artist", "Unknown"),
                channel=item.get("channel", ""),
                thumbnail=item.get("thumbnail"),
                duration_seconds=item.get("duration_seconds"),
                mood_tags=[mood.mood, mood.intent.value],
                energy_level=mood.energy,
                is_hidden_gem=is_gem,
                popularity_score=min(1.0, (view_count or 100_000) / 5_000_000),
            )
            discovered.append(track)
            
            if len(discovered) >= count:
                break
        
        if len(discovered) >= count:
            break
    
    return discovered[:count]


async def get_trending_tracks(
    genre: Optional[str] = None,
    region: str = "US",
    max_results: int = 15,
) -> List[Track]:
    """
    Fetch currently trending music from YouTube.
    
    Args:
        genre: Optional genre filter
        region: Country code for trending
        max_results: Maximum results to return
    
    Returns:
        List of trending Track objects
    """
    queries = []
    if genre:
        queries = [
            f"trending {genre} music 2024",
            f"viral {genre} songs this week",
            f"top {genre} hits 2024",
        ]
    else:
        queries = [
            "trending music 2024",
            "viral songs this week",
            "top hits 2025",
            "music trending right now",
        ]
    
    tasks = [search_youtube(q, max_results=6) for q in queries[:3]]
    batches = await asyncio.gather(*tasks, return_exceptions=True)
    
    seen_ids = set()
    trending: List[Track] = []
    
    for batch in batches:
        if not isinstance(batch, list):
            continue
        for item in batch:
            vid_id = item.get("youtube_id")
            if not vid_id or vid_id in seen_ids:
                continue
            seen_ids.add(vid_id)
            
            track = Track(
                youtube_id=vid_id,
                title=item.get("title", ""),
                artist=item.get("artist", "Unknown"),
                channel=item.get("channel", ""),
                thumbnail=item.get("thumbnail"),
                duration_seconds=item.get("duration_seconds"),
                is_hidden_gem=False,
                popularity_score=0.8,
            )
            trending.append(track)
    
    return trending[:max_results]


def _build_discovery_queries(
    mood: MoodAnalysis,
    genre: str,
    discovery_type: str,
) -> List[str]:
    """Build discovery queries from templates."""
    templates = DISCOVERY_TEMPLATES.get(discovery_type, DISCOVERY_TEMPLATES["hidden_gems"])
    queries = []
    for template in templates:
        query = template.format(
            genre=genre,
            mood=mood.mood,
            intent=mood.intent.value,
        )
        queries.append(query)
    return queries


def _pick_genre(
    taste_profile: Optional[TasteProfile],
    mood: MoodAnalysis,
) -> str:
    """Pick a genre from taste profile or derive from mood."""
    if taste_profile and taste_profile.top_genres:
        return taste_profile.top_genres[0]
    
    # Derive from mood intent
    mood_genre_map = {
        "focus": "lo-fi",
        "relax": "ambient",
        "workout": "electronic",
        "sleep": "piano",
        "party": "pop",
        "explore": "indie",
        "heal": "acoustic",
    }
    return mood_genre_map.get(mood.intent.value, "instrumental")