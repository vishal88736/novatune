"""
Playlist Upload Analysis Agent — Analyzes uploaded playlists to build
or refine user taste profiles. Supports YouTube playlist URLs and CSV.
"""

import csv
import io
import json
import re
from typing import List, Dict, Any, Optional
from services.youtube_service import get_playlist_items, search_youtube
from services.llm_service import call_llm
from models.schemas import TasteProfile


ANALYSIS_SYSTEM_PROMPT = """You are a music intelligence analyst.
Given a list of songs and artists, analyze the musical taste profile.

Return ONLY valid JSON with this exact structure:
{
  "top_genres": ["genre1", "genre2", ...],
  "top_artists": ["artist1", "artist2", ...],
  "bpm_preference": "60-90" or "90-120" or "120-150" or "mixed",
  "mainstream_score": <float 0.0-1.0>,
  "emotional_tendencies": ["melancholic", "energetic", ...],
  "music_era_preference": "classic" or "modern" or "mixed",
  "instrumental_preference": <float 0.0-1.0>,
  "listening_style": "background" or "active" or "mixed",
  "summary": "<2 sentence description of this listener>"
}
"""


async def analyze_youtube_playlist(playlist_url: str) -> TasteProfile:
    """
    Fetch and analyze a YouTube playlist URL.
    
    Args:
        playlist_url: Full YouTube playlist URL or ID
    
    Returns:
        TasteProfile derived from playlist analysis
    """
    # Extract playlist ID
    playlist_id = _extract_playlist_id(playlist_url)
    if not playlist_id:
        raise ValueError(f"Cannot extract playlist ID from: {playlist_url}")
    
    # Fetch playlist items from YouTube API
    items = await get_playlist_items(playlist_id, max_results=50)
    
    if not items:
        raise ValueError("Playlist is empty or inaccessible")
    
    # Build analysis input
    track_list = [
        f"{item.get('title', 'Unknown')} — {item.get('channel', 'Unknown')}"
        for item in items
    ]
    
    return await _analyze_track_list(track_list)


async def analyze_csv_playlist(csv_content: str) -> TasteProfile:
    """
    Analyze a CSV file containing song/artist data.
    
    Supported CSV formats:
    - "title, artist" columns
    - "song, artist, genre" columns
    - Single column with "Artist - Song" format
    
    Args:
        csv_content: Raw CSV string content
    
    Returns:
        TasteProfile derived from analysis
    """
    reader = csv.DictReader(io.StringIO(csv_content))
    track_list = []
    
    for row in reader:
        # Try common column name variations
        title = (
            row.get("title") or row.get("song") or row.get("track") or
            row.get("Title") or row.get("Song") or ""
        ).strip()
        
        artist = (
            row.get("artist") or row.get("Artist") or
            row.get("band") or row.get("Band") or ""
        ).strip()
        
        if title and artist:
            track_list.append(f"{title} — {artist}")
        elif title:
            track_list.append(title)
    
    if not track_list:
        raise ValueError("No valid tracks found in CSV")
    
    return await _analyze_track_list(track_list)


async def analyze_manual_playlist(songs: List[Dict[str, str]]) -> TasteProfile:
    """
    Analyze a manually provided list of songs.
    
    Args:
        songs: List of dicts with 'title' and 'artist' keys
    
    Returns:
        TasteProfile
    """
    track_list = [
        f"{s.get('title', '')} — {s.get('artist', '')}"
        for s in songs
        if s.get("title") or s.get("artist")
    ]
    
    if not track_list:
        raise ValueError("No songs provided")
    
    return await _analyze_track_list(track_list)


async def _analyze_track_list(track_list: List[str]) -> TasteProfile:
    """Core analysis logic using LLM."""
    # Sample if too many tracks
    sample = track_list[:50]
    track_text = "\n".join(f"- {t}" for t in sample)
    
    prompt = f"Analyze this playlist of {len(track_list)} tracks (showing {len(sample)}):\n\n{track_text}\n\nReturn the taste profile JSON."
    
    raw = await call_llm(
        system_prompt=ANALYSIS_SYSTEM_PROMPT,
        user_prompt=prompt,
        max_tokens=500,
    )
    
    # Parse response
    clean = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
    try:
        data = json.loads(clean)
    except Exception:
        match = re.search(r"\{.*\}", clean, re.DOTALL)
        data = json.loads(match.group()) if match else {}
    
    # Build TasteProfile
    return TasteProfile(
        top_genres=data.get("top_genres", [])[:10],
        top_artists=data.get("top_artists", [])[:15],
        bpm_preference=data.get("bpm_preference", "mixed"),
        mainstream_score=float(data.get("mainstream_score", 0.5)),
        emotional_tendencies=data.get("emotional_tendencies", []),
    )


def _extract_playlist_id(url: str) -> Optional[str]:
    """Extract YouTube playlist ID from URL."""
    # Handle direct ID input
    if len(url) < 50 and "http" not in url:
        return url
    
    # Regex patterns for playlist ID
    patterns = [
        r"list=([a-zA-Z0-9_-]+)",
        r"playlist\?list=([a-zA-Z0-9_-]+)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None