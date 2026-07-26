# VibeAI — "The AI that understands your vibe."

VibeAI is an AI-first emotional operating system for music. It is not a music
player and not a Spotify clone — it is a multi-agent AI companion (personal DJ +
emotional companion + music therapist + recommendation engine) that happens to
play music through YouTube as one of its output surfaces.

## Monorepo layout

```
website/     User-facing product: Next.js 15 frontend + FastAPI backend + Postgres
ai-engine/   The "brain": 11-agent multi-agent system, Groq LLM orchestration,
             embeddings, GoEmotions, Qdrant vector search
infra/       Docker, CI/CD, scripts
packages/    Shared types/contracts used by both website and ai-engine
docs/        Architecture docs
```

## Quick start (local dev)

```bash
cp website/frontend/.env.example website/frontend/.env.local
cp website/backend/.env.example website/backend/.env
cp ai-engine/.env.example ai-engine/.env
# fill in GROQ_API_KEY, YOUTUBE_API_KEY, BETTER_AUTH_SECRET, etc.

docker compose -f infra/docker/docker-compose.yml up --build
```

This brings up: `postgres`, `redis`, `qdrant`, `backend` (FastAPI, :8000),
`ai-engine` (FastAPI, :8100), `celery-worker`, `celery-beat`, `frontend` (Next.js, :3000).

Visit http://localhost:3000

## Services

| Service | Port | Description |
|---|---|---|
| frontend | 3000 | Next.js 15 App Router UI |
| backend | 8000 | FastAPI product API (auth, persistence, orchestration entrypoint) |
| ai-engine | 8100 | FastAPI multi-agent AI microservice (Groq, Qdrant, GoEmotions) |
| postgres | 5432 | Primary datastore |
| redis | 6379 | Cache, Celery broker, context bus, SSE pub/sub |
| qdrant | 6333 | Vector database |

See `docs/VibeAI-Architecture.md` for the full architecture spec.
