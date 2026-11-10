"""Batch and streaming embedding generation for tracks, memory entries, and
free-text search queries — the shared entry point every other pipeline uses
before touching Qdrant."""

from typing import Any

from providers.embeddings.sentence_transformer_provider import embedding_provider
from vector_store.collections import MEMORY, TRACKS
from vector_store.qdrant_client import vector_store


def embed_track(track_id: str, title: str, artist: str, genre_tags: list[str], mood_tags: list[str]) -> None:
    text = f"{title} by {artist}. Genres: {', '.join(genre_tags)}. Moods: {', '.join(mood_tags)}."
    vector = embedding_provider.embed(text)
    vector_store.upsert(TRACKS, track_id, vector, {"title": title, "artist": artist, "genre_tags": genre_tags, "mood_tags": mood_tags})


def embed_tracks_batch(tracks: list[dict[str, Any]]) -> None:
    texts = [f"{t['title']} by {t['artist']}" for t in tracks]
    vectors = embedding_provider.embed_batch(texts)
    for track, vector in zip(tracks, vectors, strict=True):
        vector_store.upsert(TRACKS, track["id"], vector, track)


def embed_memory_entry(entry_id: str, user_id: str, content: str, entry_type: str) -> None:
    vector = embedding_provider.embed(content)
    vector_store.upsert(MEMORY, entry_id, vector, {"user_id": user_id, "entry_type": entry_type})
