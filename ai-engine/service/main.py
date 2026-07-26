from contextlib import asynccontextmanager

from fastapi import FastAPI

from service.router import router
from vector_store.qdrant_client import vector_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    vector_store.bootstrap()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="VibeAI AI Engine",
        description="Multi-agent AI microservice: Groq orchestration, embeddings, GoEmotions, Qdrant.",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.include_router(router)

    @app.get("/health", tags=["system"])
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": "vibeai-ai-engine"}

    return app


app = create_app()
