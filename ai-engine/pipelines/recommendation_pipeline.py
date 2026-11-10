"""
End-to-end candidate generation → filtering → diversity injection →
re-ranking, orchestrated as a pure function so it can be called from the
recommendation_agent, tested in isolation, and reused by the Celery
pre-computation jobs.
"""

from typing import Any

from providers.embeddings.sentence_transformer_provider import embedding_provider
from vector_store.collections import TRACKS
from vector_store.qdrant_client import vector_store

MOOD_WEIGHT = 0.6
TASTE_WEIGHT = 0.4
DIVERSITY_QUOTA = 0.2


def blend_vectors(mood_vector: list[float], taste_vector: list[float]) -> list[float]:
    return [MOOD_WEIGHT * m + TASTE_WEIGHT * t for m, t in zip(mood_vector, taste_vector, strict=True)]


def generate_candidates(mood_label: str, taste_embedding: list[float] | None, limit: int = 30) -> list[dict[str, Any]]:
    mood_vector = embedding_provider.embed(mood_label)
    query_vector = blend_vectors(mood_vector, taste_embedding) if taste_embedding else mood_vector
    results = vector_store.search(TRACKS, query_vector, limit=limit)
    return [r["payload"] | {"id": r["id"], "score": r["score"]} for r in results]


def apply_diversity_quota(candidates: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    reserved = int(limit * DIVERSITY_QUOTA)
    mainstream = [c for c in candidates if c.get("popularity_score", 0) > 0.35][: limit - reserved]
    niche = [c for c in candidates if c.get("popularity_score", 0) <= 0.35][:reserved]
    return mainstream + niche
