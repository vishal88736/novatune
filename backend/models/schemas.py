"""
Pydantic models (schemas) for MoodWave MongoDB collections.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ─────────────────────────────────────────────
# Enums
# ─────────────────────────────────────────────

class EnergyLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Intent(str, Enum):
    focus = "focus"
    relax = "relax"
    workout = "workout"
    sleep = "sleep"
    party = "party"
    explore = "explore"
    heal = "heal"


# ─────────────────────────────────────────────
# User Schema
# ─────────────────────────────────────────────

class TasteProfile(BaseModel):
    top_genres: List[str] = []
    top_artists: List[str] = []
    bpm_preference: Optional[str] = None          # e.g. "60-90", "120-140"
    mainstream_score: float = 0.5                 # 0=underground, 1=mainstream
    energy_distribution: Dict[str, float] = {}   # {"low": 0.3, "medium": 0.5, "high": 0.2}
    emotional_tendencies: List[str] = []
    skipped_genres: List[str] = []
    preferred_languages: List[str] = ["English"]
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserSchema(BaseModel):
    user_id: str
    name: Optional[str] = None
    email: Optional[str] = None
    taste_profile: TasteProfile = Field(default_factory=TasteProfile)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_active: datetime = Field(default_factory=datetime.utcnow)


# ─────────────────────────────────────────────
# Mood Schema
# ─────────────────────────────────────────────

class MoodAnalysis(BaseModel):
    mood: str                           # e.g. "tired", "anxious", "happy"
    energy: EnergyLevel
    intent: Intent
    music_style: str                    # e.g. "ambient instrumental"
    productivity_need: float = 0.5     # 0-1
    relaxation_level: float = 0.5      # 0-1
    raw_input: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MoodHistoryEntry(BaseModel):
    user_id: str
    analysis: MoodAnalysis
    playlist_generated: bool = False
    generated_playlist_id: Optional[str] = None


# ─────────────────────────────────────────────
# Track Schema
# ─────────────────────────────────────────────

class Track(BaseModel):
    youtube_id: str
    title: str
    artist: str
    channel: str
    thumbnail: Optional[str] = None
    duration_seconds: Optional[int] = None
    genre_tags: List[str] = []
    mood_tags: List[str] = []
    energy_level: Optional[EnergyLevel] = None
    bpm_estimate: Optional[int] = None
    is_hidden_gem: bool = False
    popularity_score: float = 0.5       # 0=obscure, 1=mainstream


# ─────────────────────────────────────────────
# Playlist Schemas
# ─────────────────────────────────────────────

class UploadedPlaylist(BaseModel):
    user_id: str
    source: str                          # "youtube_url", "csv", "manual"
    raw_tracks: List[Dict[str, Any]] = []
    analyzed_profile: Optional[TasteProfile] = None
    upload_timestamp: datetime = Field(default_factory=datetime.utcnow)


class GeneratedPlaylist(BaseModel):
    playlist_id: str
    user_id: str
    mood_snapshot: MoodAnalysis
    tracks: List[Track]
    emotional_arc: List[str] = []       # e.g. ["fatigue","stabilization","focus"]
    generation_reason: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    active: bool = True


# ─────────────────────────────────────────────
# Interaction Schema
# ─────────────────────────────────────────────

class InteractionType(str, Enum):
    play = "play"
    skip = "skip"
    replay = "replay"
    like = "like"
    dislike = "dislike"
    complete = "complete"


class InteractionEvent(BaseModel):
    user_id: str
    playlist_id: str
    track_youtube_id: str
    interaction: InteractionType
    listen_duration_seconds: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ─────────────────────────────────────────────
# Listening History Schema
# ─────────────────────────────────────────────

class ListeningHistoryEntry(BaseModel):
    user_id: str
    track: Track
    listened_at: datetime = Field(default_factory=datetime.utcnow)
    context_mood: Optional[str] = None
    context_intent: Optional[str] = None
    listen_percentage: float = 0.0     # 0.0 - 1.0