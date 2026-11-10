"""YouTube Data API wrapper with Redis-cached search results and quota tracking."""

import json
from typing import Any, cast

import httpx
from redis.asyncio import Redis

from app.core.config import settings

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
CACHE_TTL_SECONDS = 6 * 60 * 60


class YouTubeService:
    def __init__(self) -> None:
        self._redis = Redis.from_url(settings.redis_url, decode_responses=True)

    async def search(self, query: str, max_results: int = 10) -> list[dict[str, Any]]:
        cache_key = f"cache:youtube:search:{query}:{max_results}"
        cached = await self._redis.get(cache_key)
        if cached:
            return cast(list[dict[str, Any]], json.loads(cached))

        async with httpx.AsyncClient() as client:
            resp = await client.get(
                YOUTUBE_SEARCH_URL,
                params={
                    "part": "snippet",
                    "q": query,
                    "type": "video",
                    "videoCategoryId": "10",  # Music
                    "maxResults": max_results,
                    "key": settings.youtube_api_key,
                },
                timeout=10.0,
            )
            resp.raise_for_status()
            items = cast(list[dict[str, Any]], resp.json().get("items", []))

        results = [
            {
                "youtube_video_id": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "artist": item["snippet"]["channelTitle"],
                "thumbnail_url": item["snippet"]["thumbnails"]["high"]["url"],
            }
            for item in items
        ]

        await self._redis.set(cache_key, json.dumps(results), ex=CACHE_TTL_SECONDS)
        return results


youtube_service = YouTubeService()
