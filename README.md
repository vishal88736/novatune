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

## Quick start

```bash
./infra/scripts/dev-up.sh
```

This starts the whole stack: Postgres, Redis and Qdrant in Docker, and the
three application services from your working tree (so edits hot-reload). It
creates the env files from their examples, syncs the shared `BETTER_AUTH_SECRET`
between the frontend and backend, and runs the database migrations.

| Service | Port | Description |
|---|---|---|
| frontend | 3000 | Next.js 15 App Router UI |
| backend | 8000 | FastAPI product API (auth, persistence, orchestration entrypoint) |
| ai-engine | 8100 | FastAPI multi-agent AI microservice (Groq, Qdrant, GoEmotions) |
| postgres | 5432 | Primary datastore |
| redis | 6379 | Cache, Celery broker, context bus, SSE pub/sub |
| qdrant | 6333 | Vector database |

Visit http://localhost:3000 — sign up at `/sign-up` and the app shell opens.

To run the services in containers instead:

```bash
cp website/frontend/.env.example website/frontend/.env.local
cp website/backend/.env.example website/backend/.env
cp ai-engine/.env.example ai-engine/.env
# fill in GROQ_API_KEY, YOUTUBE_API_KEY, BETTER_AUTH_SECRET, etc.

docker compose -f infra/docker/docker-compose.yml up --build
```

## Configuration

- **`GROQ_API_KEY`** (ai-engine) is required for the Conversation Agent to
  stream replies. Everything else works without it — the Mood Agent runs
  GoEmotions locally, so mood check-ins, the mood wheel and recommendations
  all function.
- **`BETTER_AUTH_SECRET`** must be identical in `website/frontend/.env.local`
  and `website/backend/.env`: the frontend issues the session cookie and the
  backend verifies it. `dev-up.sh` keeps them in step.
- **`YOUTUBE_API_KEY`** (backend) is needed for track search and the trend
  crawl.

## Database

Two schemas in one Postgres database:

- `public` — the product's domain tables (users, tracks, playlists, mood
  logs, listening sessions, …), owned by `website/backend`.
- `auth` — Better Auth's own tables (user, session, account, verification).

Both are created by `alembic upgrade head`. The domain `users` row is
provisioned on the caller's first authenticated request; `POST
/api/v1/auth/session/sync` does the same thing explicitly and is safe to call
on every sign-in.

## Checks

```bash
# backend
cd website/backend && .venv/bin/ruff check . && .venv/bin/mypy app && .venv/bin/python -m pytest -q

# ai-engine
cd ai-engine && .venv/bin/ruff check . && .venv/bin/mypy . && .venv/bin/python -m pytest -q
# golden-set regression gate — exits non-zero below the accuracy threshold
.venv/bin/python -m evaluation.offline_eval.eval_mood_agent

# frontend
cd website/frontend && npm run lint && npm run typecheck && npm run test && npm run build
```

All of these run in CI on every push to `main`.

## Design system

Light, printed-paper look: cream canvas, a violet primary, a sunflower accent
and dark navy type, with dashed hand-drawn doodles and a gradient disc as
signature elements. Tokens live in `website/frontend/src/styles/globals.css`;
the signature pieces are `VibeDisc`, `Doodle` and `PlayerPreview` under
`website/frontend/src/components/magic/`.

See `docs/VibeAI-Architecture.md` for the full architecture spec.
