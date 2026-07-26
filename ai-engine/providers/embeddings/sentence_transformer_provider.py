"""
Sentence Transformer embedding provider. Used for: track metadata vectors,
user taste centroid vectors, memory entry vectors, and free-text "search by
vibe" queries. Model choice is env-driven (default all-MiniLM-L6-v2 for
speed; bge-large-en-v1.5 available for higher-quality offline batch jobs).
"""

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from service.config import settings


@lru_cache(maxsize=1)
def _model() -> SentenceTransformer:
    return SentenceTransformer(settings.sentence_transformer_model)


class EmbeddingProvider:
    def embed(self, text: str) -> list[float]:
        return _model().encode(text, normalize_embeddings=True).tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return _model().encode(texts, normalize_embeddings=True).tolist()


embedding_provider = EmbeddingProvider()
