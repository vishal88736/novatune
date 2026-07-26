"""Qdrant collection schema definitions."""

from dataclasses import dataclass

EMBEDDING_DIM = 384  # all-MiniLM-L6-v2 output size


@dataclass(frozen=True)
class CollectionSpec:
    name: str
    dim: int
    distance: str = "Cosine"


TRACKS = CollectionSpec("tracks_embeddings", EMBEDDING_DIM)
USER_TASTE = CollectionSpec("user_taste_embeddings", EMBEDDING_DIM)
MEMORY = CollectionSpec("memory_embeddings", EMBEDDING_DIM)
MOOD_REFERENCE = CollectionSpec("mood_reference_embeddings", EMBEDDING_DIM)

ALL_COLLECTIONS = [TRACKS, USER_TASTE, MEMORY, MOOD_REFERENCE]

# Canonical mood labels seeded into MOOD_REFERENCE at bootstrap time, so a
# free-text mood description can be semantically matched even when it
# doesn't overlap lexically with a GoEmotions label.
CANONICAL_MOOD_LABELS = [
    "euphoric", "content", "calm", "melancholic", "anxious",
    "angry", "nostalgic", "motivated", "heartbroken", "hopeful",
]
