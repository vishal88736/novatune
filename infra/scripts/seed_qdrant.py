"""
Seeds the mood_reference_embeddings Qdrant collection with canonical mood
labels so free-text "search by vibe" queries have something to match
against even before any tracks have been ingested.

Run from ai-engine/: python ../infra/scripts/seed_qdrant.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "ai-engine"))

from providers.embeddings.sentence_transformer_provider import embedding_provider  # noqa: E402
from vector_store.collections import CANONICAL_MOOD_LABELS, MOOD_REFERENCE  # noqa: E402
from vector_store.qdrant_client import vector_store  # noqa: E402


def main() -> None:
    vector_store.bootstrap()
    for label in CANONICAL_MOOD_LABELS:
        vector = embedding_provider.embed(label)
        vector_store.upsert(MOOD_REFERENCE, label, vector, {"label": label})
    print(f"Seeded {len(CANONICAL_MOOD_LABELS)} canonical mood labels.")


if __name__ == "__main__":
    main()
