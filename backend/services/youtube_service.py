"""
YouTube Data API v3 Service.
Handles video search, playlist fetching, and video details.
Uses YouTube IFrame Player API for frontend embedding — no audio download.
"""

import os
import httpx
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"


async def search_youtube(
    query: str,
    max_results: int = 5,
    order: str = "relevance",  # relevance | date | viewCount | rating
) -> List[Dict[str, Any]]:
    """
    Search YouTube for videos matching the query.
    
    Args:
        query: Search string
        max_results: Maximum number of results (1-50)
        order: Sort order
    
    Returns:
        List of video metadata dicts
    """
    if not YOUTUBE_API_KEY:
        raise ValueError("YOUTUBE_API_KEY not configured")
    
    async with httpx.AsyncClient(timeout=15.0) as client:
        # Step 1: Search for video IDs
        search_resp = await client.get(
            f"{YOUTUBE_API_BASE}/search",
            params={
                "part": "snippet",
                "q": query,
                "type": "video",
                "videoCategoryId": "10",  # Music category
                "maxResults": max_results,
                "order": order,
                "key": YOUTUBE_API_KEY,
            },
        )
        search_resp.raise_for_status()
        search_data = search_resp.json()
        
        items = search_data.get("items", [])
        if not items:
            return []
        
        video_ids = [item["id"]["videoId"] for item in items if item.get("id", {}).get("videoId")]
        
        if not video_ids:
            return []
        
        # Step 2: Fetch detailed stats for these videos
        details = await _get_video_details_batch(client, video_ids)
        detail_map = {d["youtube_id"]: d for d in details}
        
        # Step 3: Merge search snippets with detail stats
        results = []
        for item in items:
            vid_id = item.get("id", {}).get("videoId")
            if not vid_id:
                continue
            
            snippet = item.get("snippet", {})
            detail = detail_map.get(vid_id, {})
            
            results.append({
                "youtube_id": vid_id,
                "title": snippet.get("title", ""),
                "artist": _extract_artist(snippet.get("title", ""), snippet.get("channelTitle", "")),
                "channel": snippet.get("channelTitle", ""),
                "thumbnail": _best_thumbnail(snippet.get("thumbnails", {})),
                "published_at": snippet.get("publishedAt"),
                "duration_seconds": detail.get("duration_seconds"),
                "view_count": detail.get("view_count", 0),
                "like_count": detail.get("like_count", 0),
                "genre_tags": [],  # enriched by recommendation agent
            })
        
        return results


async def get_video_details(youtube_id: str) -> Optional[Dict[str, Any]]:
    """Fetch details for a single YouTube video."""
    async with httpx.AsyncClient(timeout=15.0) as client:
        details = await _get_video_details_batch(client, [youtube_id])
        return details[0] if details else None


async def get_playlist_items(
    playlist_id: str,
    max_results: int = 50,
) -> List[Dict[str, Any]]:
    """
    Fetch all items from a YouTube playlist.
    
    Args:
        playlist_id: YouTube playlist ID
        max_results: Max items to fetch (up to 50 per page)
    
    Returns:
        List of video info dicts
    """
    if not YOUTUBE_API_KEY:
        raise ValueError("YOUTUBE_API_KEY not configured")
    
    all_items = []
    page_token = None
    
    async with httpx.AsyncClient(timeout=15.0) as client:
        while len(all_items) < max_results:
            params = {
                "part": "snippet",
                "playlistId": playlist_id,
                "maxResults": min(50, max_results - len(all_items)),
                "key": YOUTUBE_API_KEY,
            }
            if page_token:
                params["pageToken"] = page_token
            
            resp = await client.get(f"{YOUTUBE_API_BASE}/playlistItems", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            for item in data.get("items", []):
                snippet = item.get("snippet", {})
                vid_id = snippet.get("resourceId", {}).get("videoId")
                if vid_id:
                    all_items.append({
                        "youtube_id": vid_id,
                        "title": snippet.get("title", ""),
                        "channel": snippet.get("videoOwnerChannelTitle", ""),
                        "thumbnail": _best_thumbnail(snippet.get("thumbnails", {})),
                    })
            
            page_token = data.get("nextPageToken")
            if not page_token:
                break
    
    return all_items[:max_results]


async def _get_video_details_batch(
    client: httpx.AsyncClient,
    video_ids: List[str],
) -> List[Dict[str, Any]]:
    """Fetch duration and stats for a batch of video IDs."""
    if not video_ids:
        return []
    
    resp = await client.get(
        f"{YOUTUBE_API_BASE}/videos",
        params={
            "part": "contentDetails,statistics",
            "id": ",".join(video_ids),
            "key": YOUTUBE_API_KEY,
        },
    )
    resp.raise_for_status()
    data = resp.json()
    
    results = []
    for item in data.get("items", []):
        vid_id = item.get("id")
        content = item.get("contentDetails", {})
        stats = item.get("statistics", {})
        
        results.append({
            "youtube_id": vid_id,
            "duration_seconds": _parse_iso8601_duration(content.get("duration", "")),
            "view_count": int(stats.get("viewCount", 0)),
            "like_count": int(stats.get("likeCount", 0)),
        })
    
    return results


def _extract_artist(title: str, channel: str) -> str:
    """Attempt to extract artist name from video title."""
    # Common patterns: "Artist - Song Title", "Artist: Song"
    if " - " in title:
        return title.split(" - ")[0].strip()
    if " | " in title:
        return title.split(" | ")[0].strip()
    # Fall back to channel name
    return channel


def _best_thumbnail(thumbnails: Dict) -> Optional[str]:
    """Pick the highest quality available thumbnail."""
    for quality in ("maxres", "high", "medium", "standard", "default"):
        if quality in thumbnails:
            return thumbnails[quality].get("url")
    return None


def _parse_iso8601_duration(duration: str) -> Optional[int]:
    """Convert ISO 8601 duration (PT4M32S) to seconds."""
    import re
    if not duration:
        return None
    
    match = re.match(
        r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?",
        duration
    )
    if not match:
        return None
    
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds