"""
MoodWave AI Music Companion — FastAPI Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database.connection import connect_db, disconnect_db
from api.mood import router as mood_router
from api.playlist import router as playlist_router
from api.tracks import router as tracks_router
from api.interaction import router as interaction_router
from api.user import router as user_router
from api.explain import router as explain_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await disconnect_db()


app = FastAPI(
    title="MoodWave AI Music Companion",
    description="Emotionally intelligent adaptive music recommendation system",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(mood_router, prefix="/api", tags=["Mood"])
app.include_router(playlist_router, prefix="/api", tags=["Playlist"])
app.include_router(tracks_router, prefix="/api", tags=["Tracks"])
app.include_router(interaction_router, prefix="/api", tags=["Interaction"])
app.include_router(user_router, prefix="/api", tags=["User"])
app.include_router(explain_router, prefix="/api", tags=["Explain"])


@app.get("/")
async def root():
    return {"message": "MoodWave AI Backend is running", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}