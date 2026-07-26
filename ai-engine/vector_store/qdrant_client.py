"""Thin wrapper around the Qdrant client — collection bootstrap, upsert, and
search helpers shared by all pipelines."""

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

from service.config import settings
from vector_store.collections import ALL_COLLECTIONS, CollectionSpec


class VectorStore:
    def __init__(self) -> None:
        self._client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key or None)

    def bootstrap(self) -> None:
        """Idempotently ensures all required collections exist. Safe to call on startup."""
        existing = {c.name for c in self._client.get_collections().collections}
        for spec in ALL_COLLECTIONS:
            if spec.name not in existing:
                self._client.create_collection(
                    collection_name=spec.name,
                    vectors_config=qmodels.VectorParams(
                        size=spec.dim, distance=qmodels.Distance[spec.distance.upper()]
                    ),
                )

    def upsert(self, spec: CollectionSpec, point_id: str, vector: list[float], payload: dict) -> None:
        self._client.upsert(
            collection_name=spec.name,
            points=[qmodels.PointStruct(id=point_id, vector=vector, payload=payload)],
        )

    def search(
        self,
        spec: CollectionSpec,
        query_vector: list[float],
        limit: int = 20,
        query_filter: dict | None = None,
    ) -> list[dict]:
        qfilter = qmodels.Filter(**query_filter) if query_filter else None
        results = self._client.search(
            collection_name=spec.name, query_vector=query_vector, limit=limit, query_filter=qfilter
        )
        return [{"id": r.id, "score": r.score, "payload": r.payload} for r in results]


vector_store = VectorStore()
