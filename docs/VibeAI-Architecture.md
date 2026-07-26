# VibeAI — Software Architecture & Project Structure
### "The AI that understands your vibe."

**Document type:** Architecture Specification (Phase 0)
**Status:** Awaiting approval before code generation begins
**Version:** 1.0

---

## 0. Product Framing

VibeAI is not a music player. It is an **AI-first emotional operating system for music**, composed of a multi-agent AI backend that listens, understands, remembers, and orchestrates — with a music player as one of its output surfaces (via YouTube).

The product's core loop:

```
User signal (text / voice / mood tap / uploaded playlist)
        ↓
Conversation + Mood Agents interpret emotional state
        ↓
Memory + Taste Profiling Agents contextualize against history
        ↓
Recommendation + Sequencing + Discovery Agents build an experience
        ↓
Explainability Agent narrates *why*
        ↓
Playback Orchestrator (YouTube IFrame) executes it
        ↓
Analytics + Trend Agents learn from the outcome
```

Every screen in the product should visibly trace back to this loop — the UI is a window into an agentic system, not a catalog browser.

---

## 1. Tech Stack (Confirmed)

### Frontend
| Layer | Choice |
|---|---|
| Framework | Next.js 15 (App Router, RSC, Server Actions) |
| Language | TypeScript (strict mode) |
| Styling | Tailwind CSS v4 |
| Components | shadcn/ui (base) + Magic UI (motion/marketing primitives) |
| Motion | Framer Motion |
| Server state | TanStack Query v5 |
| Client state | Zustand (player state, agent-stream state, UI state) |
| Forms | React Hook Form + Zod resolvers |
| Icons | Lucide React |
| Realtime | Server-Sent Events (agent thinking/streaming) + WebSocket (playback sync) |

### Backend
| Layer | Choice |
|---|---|
| API framework | FastAPI (Python 3.12, async) |
| ORM | SQLAlchemy 2.0 (async engine) |
| Validation | Pydantic v2 |
| Background jobs | Celery + Redis broker |
| Migrations | Alembic |
| Task areas | playlist ingestion, embedding generation, trend crawling, nightly taste recompute |

### Data Layer
| Store | Purpose |
|---|---|
| PostgreSQL (Neon) | Source of truth: users, tracks, playlists, sessions, memory, analytics |
| Redis | Cache, Celery broker, rate limiting, agent short-term memory, pub/sub for streaming |
| Qdrant | Vector search: track embeddings, taste embeddings, semantic query search, "vibe" similarity |

### Auth
- **Better Auth** — email/password + OAuth (Google, GitHub), session cookies, CSRF handling, integrated with FastAPI via a shared JWT/session-verification middleware (see §6).

### AI (updated per your instruction)
| Purpose | Model / Library |
|---|---|
| Primary LLM (conversation, reasoning, explanation, sequencing rationale) | **Groq** — `llama-3.3-70b-versatile` (reasoning/orchestration), `llama-3.1-8b-instant` (low-latency mood parsing, tagging) |
| Voice transcription | **Groq Whisper** (`whisper-large-v3-turbo`) |
| Text embeddings | Sentence Transformers (`all-MiniLM-L6-v2` for speed, `bge-large-en-v1.5` for quality) |
| Emotion classification | GoEmotions (fine-tuned HuggingFace model, 27-class emotion taxonomy) served via local inference microservice |
| Model hub / hosting fallback | HuggingFace Inference Endpoints (for GoEmotions + any custom fine-tunes) |

> Gemini/OpenAI are removed from the default path per your request. The AI client layer is provider-abstracted (`LLMProvider` interface) so a provider can be swapped later without touching agent logic.

### Music
- YouTube Data API v3 — search, metadata, channel/artist enrichment
- YouTube IFrame Player API — playback surface (web), driven by the Sequencing Agent

### Deployment
| Component | Platform |
|---|---|
| Frontend | Vercel |
| Backend (FastAPI + Celery workers) | Railway |
| Database | Neon PostgreSQL (serverless, branching for staging) |
| Redis | Railway managed Redis |
| Qdrant | Qdrant Cloud (or Railway Docker service for staging) |
| Containerization | Docker + docker-compose (local/staging parity) |

---

## 2. Top-Level Repository Structure

Per your requirement, the repo is split into **exactly two top-level product domains**, plus shared/infra folders that both depend on:

```
vibeai/
├── website/                     # Everything user-facing: Next.js app + FastAPI app + DB
│   ├── frontend/                # Next.js 15 application
│   └── backend/                 # FastAPI application (business logic, auth, persistence)
│
├── ai-engine/                   # Everything model/agent related — the "brain"
│   ├── agents/                  # 11 agents, each a self-contained module
│   ├── orchestrator/            # Multi-agent router, planner, shared context bus
│   ├── providers/                # Groq / Sentence-Transformers / GoEmotions / HF clients
│   ├── pipelines/               # embedding, recommendation, mood, discovery pipelines
│   ├── vector_store/             # Qdrant client + collection schemas
│   ├── prompts/                  # versioned prompt templates per agent
│   └── service/                  # FastAPI micro-service exposing ai-engine to website/backend
│
├── infra/                       # Cross-cutting infrastructure
│   ├── docker/                   # Dockerfiles, docker-compose.yml, compose.prod.yml
│   ├── ci/                       # GitHub Actions workflows
│   ├── scripts/                  # db seed, migration runner, dev bootstrap
│   └── env/                      # .env.example files per service
│
├── packages/                    # Shared code used by BOTH website and ai-engine
│   ├── shared-types/              # OpenAPI-generated TS types + Pydantic schemas mirror
│   └── contracts/                 # JSON schema / protobuf-style contracts for agent I/O
│
├── docs/                         # Architecture docs (this file lives here), ADRs, API docs
├── .github/
├── docker-compose.yml
├── turbo.json / pnpm-workspace.yaml   (if using a JS monorepo tool for website/frontend)
└── README.md
```

### Why this split works architecturally
- `website/` is a **product shell**: it owns users, sessions, playback state, UI, and persistence of business data (playlists, likes, uploads).
- `ai-engine/` is a **model service**: it owns intelligence — agents, embeddings, prompts, vector search — and is deliberately stateless per-request (reads/writes context via well-defined contracts, not by touching Postgres directly except through its own memory tables).
- `website/backend` talks to `ai-engine/service` over an internal HTTP/gRPC-style contract (`packages/contracts`), the same way it would talk to a third-party AI vendor — this means `ai-engine` could be extracted into its own deployable service (which it is, on Railway) without refactoring.

---

## 3. `website/frontend` — Next.js Architecture

```
website/frontend/
├── src/
│   ├── app/
│   │   ├── (marketing)/                 # public landing, no auth
│   │   │   ├── page.tsx                 # Homepage — aurora mesh hero, "this is not Spotify"
│   │   │   ├── layout.tsx
│   │   │   └── how-it-works/page.tsx
│   │   │
│   │   ├── (auth)/
│   │   │   ├── sign-in/page.tsx
│   │   │   ├── sign-up/page.tsx
│   │   │   └── layout.tsx               # centered glass card auth layout
│   │   │
│   │   ├── (app)/                       # authenticated shell
│   │   │   ├── layout.tsx               # persistent player dock + sidebar + top bar
│   │   │   ├── dashboard/page.tsx       # "Today's Vibe" — mood check-in + live recs
│   │   │   ├── chat/page.tsx            # Conversation Agent full interface
│   │   │   ├── discover/page.tsx        # Discovery + Trend Agent surfaces
│   │   │   ├── library/page.tsx         # uploaded playlists, taste profile
│   │   │   ├── library/upload/page.tsx  # Playlist Upload Analysis flow
│   │   │   ├── journey/page.tsx         # Emotional journey timeline (Memory Agent viz)
│   │   │   ├── analytics/page.tsx       # Analytics Agent dashboard
│   │   │   ├── explain/[trackId]/page.tsx # Explainability drill-down
│   │   │   └── settings/page.tsx
│   │   │
│   │   ├── api/                         # Next.js route handlers (BFF layer only)
│   │   │   ├── auth/[...all]/route.ts   # Better Auth handler
│   │   │   └── stream/route.ts          # SSE proxy to backend agent stream
│   │   │
│   │   └── layout.tsx                   # root layout, fonts, providers
│   │
│   ├── components/
│   │   ├── ui/                          # shadcn/ui primitives (generated, not hand-edited)
│   │   ├── magic/                       # Magic UI wrappers (aurora bg, marquee, orb)
│   │   ├── player/                      # PlayerDock, NowPlayingCard, Waveform, Queue
│   │   ├── chat/                        # ChatBubble, AgentThinkingIndicator, VoiceOrb
│   │   ├── mood/                        # MoodWheel, MoodCheckinCard, EmotionBadge
│   │   ├── recommendation/              # TrackCard, PlaylistRow, DiscoveryGrid
│   │   ├── explainability/              # ReasonChip, ExplanationPanel
│   │   ├── analytics/                   # ListeningHeatmap, GenreRadar, MoodTimeline
│   │   └── shared/                      # GlassCard, AuroraBackground, PageTransition
│   │
│   ├── lib/
│   │   ├── api-client.ts                # typed fetch wrapper (uses shared-types)
│   │   ├── auth-client.ts               # Better Auth client instance
│   │   ├── query-client.ts              # TanStack Query provider config
│   │   └── utils.ts
│   │
│   ├── stores/                          # Zustand
│   │   ├── player-store.ts
│   │   ├── chat-store.ts                # streaming agent messages
│   │   ├── mood-store.ts
│   │   └── ui-store.ts                  # theme, command palette, modals
│   │
│   ├── hooks/
│   │   ├── use-agent-stream.ts          # SSE hook for live agent responses
│   │   ├── use-youtube-player.ts        # wraps IFrame API
│   │   └── use-mood-detection.ts
│   │
│   ├── schemas/                         # Zod schemas (forms + API response validation)
│   ├── styles/
│   │   └── globals.css                  # Tailwind v4 config, aurora gradient tokens
│   └── config/
│       └── site.ts
│
├── public/
├── next.config.ts
├── tailwind.config.ts
├── components.json                      # shadcn config
├── package.json
└── tsconfig.json
```

**Design system notes (for Phase 2 build):**
- Aurora mesh gradients as CSS `@property` animated gradients (GPU-cheap, no canvas needed for background).
- Glassmorphism via a single `--glass` Tailwind utility layer (`backdrop-blur-xl`, `bg-white/5`, `border-white/10`) applied consistently — never ad hoc per component.
- Motion: page transitions via Framer Motion `AnimatePresence` at the `(app)` layout boundary; micro-interactions (button press, card hover) use `whileTap`/`whileHover` variants defined once in `lib/motion-variants.ts`.
- Typography: a geometric sans (e.g. Geist or Inter) for UI, a variable-weight display face for hero/marketing headlines.

---

## 4. `website/backend` — FastAPI Architecture

```
website/backend/
├── app/
│   ├── main.py                          # FastAPI app factory, middleware, routers
│   ├── core/
│   │   ├── config.py                    # Pydantic Settings (env-driven)
│   │   ├── security.py                  # Better Auth session verification, CSRF
│   │   ├── logging.py
│   │   └── exceptions.py                # domain exception → HTTP error mapping
│   │
│   ├── db/
│   │   ├── session.py                   # async SQLAlchemy engine/session
│   │   ├── base.py
│   │   └── models/                      # SQLAlchemy ORM models (see §7 schema)
│   │       ├── user.py
│   │       ├── track.py
│   │       ├── playlist.py
│   │       ├── mood_log.py
│   │       ├── memory.py
│   │       ├── session.py               # listening session
│   │       └── analytics.py
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── router.py                # aggregates all v1 routers
│   │       ├── endpoints/
│   │       │   ├── auth.py              # session bridge, profile
│   │       │   ├── chat.py              # → proxies to ai-engine Conversation Agent
│   │       │   ├── mood.py              # → Mood Agent
│   │       │   ├── playlists.py         # upload, list, delete
│   │       │   ├── recommendations.py   # → Recommendation/Sequencing Agents
│   │       │   ├── discovery.py         # → Discovery/Trend Agents
│   │       │   ├── memory.py            # → Memory Agent (journey timeline)
│   │       │   ├── explain.py           # → Explainability Agent
│   │       │   ├── analytics.py         # → Analytics Agent
│   │       │   ├── playback.py          # play/pause/skip state sync, queue
│   │       │   └── voice.py             # audio upload → Groq Whisper → Conversation Agent
│   │       └── deps.py                  # shared FastAPI dependencies (current_user, db)
│   │
│   ├── schemas/                         # Pydantic v2 request/response DTOs
│   ├── services/                        # business logic orchestration layer
│   │   ├── ai_engine_client.py          # typed HTTP client → ai-engine/service
│   │   ├── youtube_service.py           # YouTube Data API wrapper + quota mgmt
│   │   ├── playlist_ingestion_service.py
│   │   └── playback_orchestrator.py
│   │
│   ├── workers/                         # Celery tasks
│   │   ├── celery_app.py
│   │   ├── tasks_playlist.py            # async playlist parsing + embedding trigger
│   │   ├── tasks_trend.py               # nightly trend crawl
│   │   ├── tasks_taste_recompute.py     # nightly taste profile refresh
│   │   └── tasks_analytics.py           # rollups
│   │
│   └── tests/
│       ├── unit/
│       ├── integration/
│       └── conftest.py
│
├── alembic/
│   ├── versions/
│   └── env.py
├── pyproject.toml                       # (uv or poetry)
├── Dockerfile
└── .env.example
```

**Key architectural rule:** `website/backend` never calls Groq, Sentence Transformers, or Qdrant directly. All model reasoning goes through `ai_engine_client.py` → `ai-engine/service`. This keeps the "product brain" swappable and independently scalable/deployable.

---

## 5. `ai-engine` — Multi-Agent AI Architecture

```
ai-engine/
├── service/
│   ├── main.py                          # FastAPI micro-service entrypoint
│   ├── router.py                        # /agents/{agent_name}/invoke, /pipeline/*
│   └── deps.py
│
├── orchestrator/
│   ├── planner.py                       # decides which agent(s) to invoke per request
│   ├── context_bus.py                   # shared short-term context (Redis-backed) across agents in one turn
│   ├── agent_registry.py                # registers all 11 agents, exposes uniform .run(ctx) interface
│   └── streaming.py                     # token/event streaming back to website/backend via SSE
│
├── agents/
│   ├── base.py                          # BaseAgent abstract class (input schema, run(), output schema)
│   ├── conversation_agent/
│   ├── mood_agent/
│   ├── taste_profiling_agent/
│   ├── playlist_upload_analysis_agent/
│   ├── recommendation_agent/
│   ├── sequencing_agent/
│   ├── memory_agent/
│   ├── discovery_agent/
│   ├── trend_analysis_agent/
│   ├── explainability_agent/
│   └── analytics_agent/
│       # each agent folder contains:
│       #   agent.py        - orchestration logic
│       #   prompts.py       - imports from /prompts, agent-specific formatting
│       #   schema.py        - Pydantic input/output contracts
│       #   tools.py         - agent-specific tool functions (if any)
│
├── providers/
│   ├── llm/
│   │   ├── base_provider.py             # LLMProvider interface (provider-agnostic)
│   │   ├── groq_provider.py             # Groq chat completions + Whisper client
│   │   └── provider_factory.py          # env-driven provider selection (future-proofing)
│   ├── embeddings/
│   │   └── sentence_transformer_provider.py
│   └── emotion/
│       └── goemotions_provider.py       # HF pipeline, 27-class emotion output
│
├── pipelines/
│   ├── embedding_pipeline.py            # track/text → vector, batch + streaming modes
│   ├── mood_detection_pipeline.py       # text/voice → GoEmotions → normalized mood vector
│   ├── recommendation_pipeline.py       # candidate generation → ranking → filtering
│   ├── sequencing_pipeline.py           # ordered "emotional arc" construction
│   └── discovery_pipeline.py            # long-tail / hidden-artist surfacing logic
│
├── vector_store/
│   ├── qdrant_client.py
│   └── collections.py                   # schema defs: tracks, taste_profiles, mood_embeddings
│
├── prompts/
│   ├── conversation/
│   ├── mood/
│   ├── recommendation/
│   ├── explainability/
│   └── versioning.py                    # prompt version registry (for A/B + rollback)
│
├── evaluation/
│   ├── offline_eval/                    # recommendation quality, mood classification accuracy
│   └── golden_sets/                     # labeled test cases per agent
│
├── tests/
├── pyproject.toml
├── Dockerfile
└── .env.example
```

### 5.1 The 11 Agents — Responsibility Contracts

| # | Agent | Input | Output | Notes |
|---|---|---|---|---|
| 1 | **Conversation Agent** | user message / voice transcript, session context | reply text, detected intent, routed sub-agent calls | Groq `llama-3.3-70b`; the "face" of VibeAI, orchestration entry point |
| 2 | **Mood Agent** | text, emoji/mood-wheel tap, listening behavior signals | normalized emotion vector (27-dim GoEmotions + valence/arousal) | GoEmotions model; feeds almost every other agent |
| 3 | **Taste Profiling Agent** | listening history, likes, uploaded playlists | taste embedding + genre/artist affinity graph | recomputed nightly via Celery, updated incrementally on strong signals |
| 4 | **Playlist Upload Analysis Agent** | uploaded playlist file/URL | parsed tracks, genre/mood breakdown, taste delta | triggers embedding pipeline per track |
| 5 | **Recommendation Agent** | mood vector + taste embedding + context | ranked candidate track list | hybrid: Qdrant ANN + collaborative signals + Groq re-ranking rationale |
| 6 | **Sequencing Agent** | candidate list + target emotional arc | ordered playback queue | e.g. "ease down" vs "build energy" arcs |
| 7 | **Memory Agent** | session events, mood logs, feedback | persisted long-term memory entries, "emotional journey" summaries | writes to `memory` table, Redis for short-term |
| 8 | **Discovery Agent** | taste embedding, diversity target | hidden/underexposed artist surfacing | penalizes popularity bias intentionally |
| 9 | **Trend Analysis Agent** | YouTube trending data, crawl cache | trending-by-mood clusters | scheduled Celery crawl, cached in Redis |
| 10 | **Explainability Agent** | a recommendation + its generating context | human-readable "why this track, why now" | Groq `llama-3.1-8b-instant` for low-latency short explanations |
| 11 | **Analytics Agent** | aggregated listening/mood data | dashboards: mood trends, genre radar, listening heatmap | mostly deterministic aggregation + light LLM narrative summary |

### 5.2 Orchestration Pattern

- **Planner-based routing**, not a rigid pipeline: the `orchestrator/planner.py` uses the Conversation Agent's intent classification to decide which subset of agents to invoke per turn (e.g., a mood check-in triggers Mood → Recommendation → Sequencing → Explainability; a playlist upload triggers Upload Analysis → Taste Profiling → Discovery).
- **Context bus**: all agents in a single turn share a Redis-backed `ctx` object (user id, session id, current mood vector, recent memory excerpt) so agents don't redundantly re-fetch state.
- **Streaming**: Conversation and Explainability agents stream tokens back through `orchestrator/streaming.py` → SSE → `website/frontend` chat UI, so the "thinking" feels alive rather than a spinner.

---

## 6. Authentication Flow (Better Auth)

```
1. User signs up/in on website/frontend via Better Auth client
2. Better Auth (Next.js route handler: app/api/auth/[...all]) issues
   a secure, httpOnly session cookie, backed by Postgres (Better Auth's own tables)
3. Every request to website/backend includes the session cookie
4. website/backend's core/security.py verifies the session by calling
   Better Auth's session-verification endpoint (or validating the shared
   secret/JWT if configured in JWT mode) — populates `current_user` dependency
5. website/backend is the ONLY service that ever sees `current_user`.
   ai-engine/service receives only an opaque `user_id` + relevant context —
   never credentials, never the raw session.
6. OAuth providers (Google/GitHub) handled entirely by Better Auth's
   provider config; no custom OAuth code needed.
```

**Database ownership:** Better Auth manages its own `user`, `session`, `account`, `verification` tables inside the same Postgres instance (Neon) as the rest of the app — kept in a dedicated schema (`auth`) to avoid collision with domain tables.

---

## 7. Database Schema (PostgreSQL — domain tables, `public` schema)

```
users                     (mirrors Better Auth's user id; app-specific profile fields)
  id (uuid, PK, = auth.user.id)
  display_name
  avatar_url
  onboarding_completed_at
  created_at

tracks
  id (uuid, PK)
  youtube_video_id (unique)
  title, artist, duration_seconds
  thumbnail_url
  genre_tags (text[])
  mood_tags (text[])
  popularity_score (float)
  is_hidden_gem (bool)             -- flagged by Discovery Agent
  qdrant_point_id (uuid)           -- FK reference into vector_store
  created_at

playlists
  id (uuid, PK)
  user_id (FK → users.id)
  source (enum: upload_csv, upload_url, spotify_export, manual)
  raw_file_ref (text, nullable)
  status (enum: pending, processing, analyzed, failed)
  created_at

playlist_tracks
  playlist_id (FK)
  track_id (FK)
  position (int)

mood_logs
  id (uuid, PK)
  user_id (FK)
  source (enum: manual_checkin, chat_inferred, behavior_inferred)
  emotion_vector (jsonb)            -- 27-dim GoEmotions scores
  valence (float), arousal (float)
  raw_text (text, nullable)
  created_at

listening_sessions
  id (uuid, PK)
  user_id (FK)
  started_at, ended_at
  target_mood, resulting_mood (nullable)
  queue (jsonb)                     -- ordered track_id list from Sequencing Agent

listening_events
  id (uuid, PK)
  session_id (FK)
  track_id (FK)
  event_type (enum: play, skip, like, dislike, replay, complete)
  timestamp_in_track (int, nullable)
  created_at

memory_entries
  id (uuid, PK)
  user_id (FK)
  entry_type (enum: fact, preference, emotional_milestone, journey_summary)
  content (text)
  embedding_ref (uuid, nullable)     -- points into Qdrant
  importance_score (float)
  created_at

taste_profiles
  user_id (FK, PK)
  genre_affinity (jsonb)
  artist_affinity (jsonb)
  embedding_ref (uuid)                -- Qdrant point
  last_computed_at

recommendation_logs
  id (uuid, PK)
  user_id (FK)
  track_id (FK)
  reason_summary (text)               -- from Explainability Agent
  agent_trace (jsonb)                 -- which agents fired, scores
  accepted (bool, nullable)           -- did user play it
  created_at

trend_snapshots
  id (uuid, PK)
  mood_cluster (text)
  tracks (jsonb)
  captured_at

analytics_daily_rollups
  user_id (FK)
  date
  total_listen_minutes
  top_genres (jsonb)
  mood_distribution (jsonb)
```

### Qdrant Collections

```
tracks_embeddings         vector: 384/1024-dim (Sentence Transformer output), payload: track_id, genre, mood_tags
user_taste_embeddings     vector: same dim, payload: user_id, computed_at
memory_embeddings         vector: same dim, payload: user_id, memory_entry_id, entry_type
mood_reference_embeddings vector: same dim, payload: canonical mood label (for semantic mood matching)
```

### Redis Key Namespaces

```
session:ctx:{session_id}         -- orchestrator context bus, TTL 1h
cache:youtube:search:{hash}      -- YouTube API response cache, TTL 6h
cache:trend:{mood_cluster}       -- trend snapshots, TTL 12h
ratelimit:{user_id}:{route}      -- sliding window rate limiting
stream:chat:{session_id}         -- pub/sub channel for SSE token streaming
celery (broker + result backend)
```

---

## 8. API Documentation (v1 — surface overview)

All routes below are on `website/backend`, prefixed `/api/v1`. Full OpenAPI spec will be generated by FastAPI automatically (`/docs`, `/openapi.json`) and mirrored into `packages/shared-types`.

```
POST   /auth/session/sync             bridge Better Auth session → backend user context

POST   /chat/message                  send message → SSE stream (Conversation Agent)
GET    /chat/history                  paginated session history

POST   /mood/checkin                  manual mood submission (mood wheel)
GET    /mood/current                  latest resolved mood vector
GET    /mood/history                  timeseries for journey view

POST   /playlists/upload              multipart upload → Celery ingestion job
GET    /playlists                     list user playlists
GET    /playlists/{id}                status + analysis result
DELETE /playlists/{id}

GET    /recommendations               current recommendation batch (mood/taste-aware)
POST   /recommendations/feedback      like/dislike/skip → feeds Recommendation + Taste agents

GET    /discovery/hidden-gems         Discovery Agent surface
GET    /discovery/trending            Trend Agent surface, filterable by mood

GET    /memory/journey                Memory Agent emotional-journey timeline
GET    /memory/entries                raw memory entries (debug/settings view)

GET    /explain/{track_id}            Explainability Agent narrative for a given rec

GET    /analytics/overview            dashboard aggregate
GET    /analytics/mood-timeline
GET    /analytics/genre-radar

POST   /playback/state                sync play/pause/seek/queue position
GET    /playback/queue

POST   /voice/transcribe              audio upload → Groq Whisper → Conversation Agent
```

Internal-only contract (`ai-engine/service`, not exposed publicly):
```
POST   /agents/{agent_name}/invoke
POST   /pipeline/recommendation/run
POST   /pipeline/embedding/run
GET    /health
```

---

## 9. AI Pipeline (end-to-end)

```
Input (text / voice / mood-tap / playlist upload)
   │
   ├─ voice → Groq Whisper → transcript
   │
   ▼
Conversation Agent (Groq llama-3.3-70b)
   → intent classification: {mood_checkin, recommendation_request,
                              chit_chat, playlist_question, discovery_request}
   │
   ▼
Mood Agent
   → GoEmotions inference → 27-dim emotion vector → valence/arousal projection
   → stored to mood_logs, pushed to context bus
   │
   ▼
Taste Profiling Agent (reads cached taste embedding, or triggers recompute)
   │
   ▼
Recommendation Agent
   → Qdrant ANN search (tracks_embeddings) filtered/boosted by mood + taste
   → candidate re-ranking (Groq llama-3.1-8b-instant, structured JSON output)
   │
   ▼
Sequencing Agent
   → orders candidates into an emotional arc (e.g. plateau, build, wind-down)
   │
   ▼
Explainability Agent
   → generates short natural-language rationale per track (streamed)
   │
   ▼
Memory Agent
   → writes session summary + significant emotional milestones
   │
   ▼
Response → website/backend → website/frontend (SSE stream + final structured payload)
```

Analytics + Trend Agents run largely out-of-band (Celery scheduled), feeding cached read models that other agents and the dashboard consume.

---

## 10. Recommendation Pipeline (detail)

1. **Candidate generation** — Qdrant ANN search over `tracks_embeddings`, query vector = weighted blend of `mood_vector_embedding` + `user_taste_embedding` (weights tunable, default 60/40 favoring current mood).
2. **Filtering** — remove recently played (last N sessions), apply explicit taste exclusions, respect content filters.
3. **Diversity injection** — Discovery Agent reserves a configurable slot quota (e.g. 20%) for low-popularity_score tracks matching the mood cluster.
4. **Re-ranking** — Groq structured-output call scores top-K candidates against a rubric (mood fit, novelty, recency of similar recs, arc position) and returns ranked JSON.
5. **Sequencing** — Sequencing Agent arranges final order into an emotional arc rather than pure rank order.
6. **Logging** — every recommendation batch logged to `recommendation_logs` with full agent trace for offline evaluation and the Explainability Agent's future reference.

---

## 11. Vector Search Pipeline (Qdrant)

- **Embedding generation**: track metadata (title + artist + genre/mood tags + optional lyrics snippet) → Sentence Transformer → stored in `tracks_embeddings` at ingestion time (Celery task triggered on playlist upload / catalog sync).
- **Mood-to-vector bridging**: `mood_reference_embeddings` holds canonical embeddings for mood labels (e.g. "melancholic," "euphoric") so a free-text mood description can be semantically matched even without exact GoEmotions label overlap.
- **User taste vector**: computed as a weighted centroid of liked/completed tracks' embeddings, recomputed nightly (Celery) and incrementally nudged on strong real-time signals (explicit like).
- **Semantic search feature** (user-facing "search by vibe, not by name"): free text → embed → Qdrant ANN → same ranking pipeline as §10 steps 2–5.

---

## 12. Prompt Engineering Strategy

- **Versioned prompts**: every agent's prompt lives in `ai-engine/prompts/{agent}/v{n}.py`; `prompts/versioning.py` resolves the active version per environment, enabling safe rollback and A/B testing.
- **Structured outputs**: all agent-to-agent handoffs (Recommendation, Sequencing, Explainability) request strict JSON via Groq's JSON mode / tool-calling, validated against Pydantic schemas in `agents/*/schema.py` before being trusted downstream — malformed output triggers a single retry with a repair prompt, then a deterministic fallback.
- **Latency tiering**: `llama-3.1-8b-instant` for anything user-latency-sensitive and short (mood tagging, explanations, re-ranking scores); `llama-3.3-70b-versatile` reserved for the Conversation Agent's actual dialogue turns where reasoning quality matters most.
- **System prompt composition**: each agent's system prompt is assembled from (a) a stable role definition, (b) injected context-bus state, (c) a small set of few-shot exemplars stored alongside the prompt file — never hand-typed inline in agent logic.
- **Safety/guardrails**: Conversation Agent system prompt explicitly scopes the assistant to music/emotional-wellness support and defers to crisis-resource language patterns for any self-harm signal detected by the Mood Agent (cross-agent guardrail, not just prompt-level).
- **Evaluation loop**: `ai-engine/evaluation/golden_sets` holds labeled cases per agent (e.g. known text → expected mood cluster) run in CI to catch prompt-version regressions before deploy.

---

## 13. Deployment Architecture

```
                    ┌──────────────────────────┐
                    │        Vercel            │
                    │  website/frontend (Next) │
                    └────────────┬─────────────┘
                                 │ HTTPS
                    ┌────────────▼─────────────┐
                    │        Railway            │
                    │  website/backend (FastAPI)│
                    │  + Celery workers          │
                    │  + Celery beat (scheduler) │
                    └────┬──────────┬───────────┘
                         │          │
             ┌───────────▼──┐   ┌───▼─────────────┐
             │ Neon Postgres│   │ Railway Redis     │
             └──────────────┘   └───────────────────┘
                         │
                    ┌────▼─────────────────┐
                    │       Railway         │
                    │  ai-engine/service    │
                    │  (FastAPI, separate   │
                    │   deploy + autoscale) │
                    └────┬──────────┬───────┘
                         │          │
                 ┌───────▼───┐  ┌───▼─────────┐
                 │  Qdrant   │  │  Groq API    │
                 │  Cloud    │  │  (external)  │
                 └───────────┘  └──────────────┘
```

- `website/backend` and `ai-engine/service` are **independently deployed Railway services**, each with their own Dockerfile, scaling policy, and env vars — this lets the AI layer scale on inference load independently of API traffic.
- Neon's branching is used to give each PR/staging environment an isolated Postgres branch.
- Qdrant Cloud free/starter tier for staging, dedicated cluster for production.

---

## 14. Docker Setup (overview — full files generated in Phase 2)

```
infra/docker/
├── docker-compose.yml            # local dev: postgres, redis, qdrant, backend, ai-engine, frontend
├── docker-compose.prod.yml       # production overrides (no local db/redis, uses managed services)
├── frontend.Dockerfile
├── backend.Dockerfile
└── ai-engine.Dockerfile
```

Local dev spins up all 6 services (`frontend`, `backend`, `ai-engine`, `postgres`, `redis`, `qdrant`) with hot-reload volumes; production compose is used only for Railway's Docker-based deploys where applicable (frontend instead deploys natively to Vercel).

---

## 15. Environment Variables (by service)

**`website/frontend/.env.example`**
```
NEXT_PUBLIC_APP_URL=
NEXT_PUBLIC_API_URL=
BETTER_AUTH_SECRET=
BETTER_AUTH_URL=
GOOGLE_CLIENT_ID= / GOOGLE_CLIENT_SECRET=
GITHUB_CLIENT_ID= / GITHUB_CLIENT_SECRET=
```

**`website/backend/.env.example`**
```
DATABASE_URL=
REDIS_URL=
BETTER_AUTH_SECRET=              # shared w/ frontend for session verification
AI_ENGINE_BASE_URL=
YOUTUBE_API_KEY=
CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=
ENVIRONMENT=development|staging|production
```

**`ai-engine/.env.example`**
```
GROQ_API_KEY=
QDRANT_URL=
QDRANT_API_KEY=
HUGGINGFACE_TOKEN=
SENTENCE_TRANSFORMER_MODEL=all-MiniLM-L6-v2
GOEMOTIONS_MODEL_PATH=
REDIS_URL=                       # shared context bus
ENVIRONMENT=development|staging|production
```

---

## 16. Testing Strategy

| Layer | Approach |
|---|---|
| Frontend unit | Vitest + React Testing Library for components/hooks |
| Frontend E2E | Playwright — critical flows: sign-up, mood check-in → recommendation, playlist upload, playback |
| Backend unit | Pytest, isolated per service (mocked DB via `pytest-asyncio` + test containers) |
| Backend integration | Pytest against a real Postgres/Redis test instance (Docker) |
| ai-engine unit | Pytest per agent with mocked `LLMProvider` (deterministic fixtures) |
| ai-engine eval | Golden-set regression suite (§12) — run on every prompt/model change |
| Contract testing | `packages/contracts` schemas validated on both sides (backend request shape, ai-engine response shape) to prevent drift |
| Load/perf | k6 scripts for `/chat/message` and `/recommendations` under concurrent load (pre-launch gate) |

---

## 17. CI/CD Pipeline (GitHub Actions)

```
.github/workflows/
├── frontend-ci.yml     lint → typecheck → unit tests → build → Vercel preview deploy (on PR)
├── backend-ci.yml      lint (ruff) → typecheck (mypy) → pytest → Docker build → Railway deploy (on merge to main)
├── ai-engine-ci.yml    lint → pytest → golden-set eval → Docker build → Railway deploy (on merge to main)
├── db-migrations.yml   alembic upgrade check against Neon staging branch on PR
└── e2e.yml             Playwright suite against preview deployment, nightly + pre-release
```

Branching model: `main` (production, protected), `develop` (staging auto-deploy), feature branches → PR → preview deploy + required checks before merge.

---

## 18. Coding Standards

- **TypeScript**: strict mode, no implicit `any`, ESLint (typescript-eslint) + Prettier, absolute imports via `@/`, components colocated with tests.
- **Python**: `ruff` (lint + format), `mypy` strict on `app/` and `ai-engine/`, Pydantic v2 everywhere at boundaries (no raw dicts crossing service lines), async-first (no blocking I/O in request path).
- **Commits**: Conventional Commits (`feat:`, `fix:`, `refactor:`...), enforced via commit-lint hook.
- **API contracts**: any change to a Pydantic schema shared across services must update `packages/contracts` in the same PR (checked in CI).
- **Agent contracts**: every agent must implement `BaseAgent.run(ctx: AgentContext) -> AgentResult` — no agent may reach into another agent's internals; all cross-agent communication goes through the context bus or explicit return values.
- **No secrets in code**: all keys via env, `.env.example` kept in sync, secrets scanning in CI.

---

## 19. Development Roadmap

**Phase 1 — Foundation**
Monorepo scaffold, Docker compose, Postgres schema + Alembic, Better Auth wired end-to-end, base Next.js shell with design system tokens (aurora/glass primitives), health-check deploys to Vercel/Railway.

**Phase 2 — Core Agent Loop**
Conversation + Mood Agents live (Groq integration), mood check-in UI, basic Recommendation Agent (Qdrant + static catalog), playback via YouTube IFrame, SSE streaming chat.

**Phase 3 — Personalization**
Taste Profiling Agent, Playlist Upload Analysis Agent, Sequencing Agent, Memory Agent + journey timeline UI, Explainability Agent.

**Phase 4 — Discovery & Trends**
Discovery Agent (hidden gems), Trend Analysis Agent + Celery crawl jobs, semantic "search by vibe."

**Phase 5 — Analytics & Voice**
Analytics Agent + dashboards, Groq Whisper voice input, notification/re-engagement loop.

**Phase 6 — Hardening**
Load testing, golden-set eval gates in CI, accessibility pass, premium micro-interaction polish, launch readiness review.

---

## Next Step

This document is the full architecture. Per your instruction, no code will be generated yet.

To proceed, confirm which module to build first — recommended order:
1. Monorepo scaffold + Docker compose + env setup
2. Database schema + Alembic migrations
3. Better Auth integration (frontend + backend bridge)
4. Design system primitives (aurora/glass components) + homepage
5. `ai-engine` skeleton (BaseAgent, Groq provider, orchestrator) + Conversation Agent
6. Mood Agent + mood check-in flow
7. Recommendation + Sequencing pipeline
8. Remaining agents, one at a time

Let me know which to start with, or say "start from module 1" to build in order.
