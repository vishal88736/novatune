from fastapi import APIRouter

from app.api.v1.endpoints import (
    analytics,
    chat,
    discovery,
    explain,
    memory,
    mood,
    playback,
    playlists,
    recommendations,
    voice,
)

api_router = APIRouter()

api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(mood.router, prefix="/mood", tags=["mood"])
api_router.include_router(playlists.router, prefix="/playlists", tags=["playlists"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(discovery.router, prefix="/discovery", tags=["discovery"])
api_router.include_router(memory.router, prefix="/memory", tags=["memory"])
api_router.include_router(explain.router, prefix="/explain", tags=["explainability"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(playback.router, prefix="/playback", tags=["playback"])
api_router.include_router(voice.router, prefix="/voice", tags=["voice"])
