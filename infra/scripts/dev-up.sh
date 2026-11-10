#!/usr/bin/env bash
# Starts the whole VibeAI stack for local development.
#
# Infrastructure (Postgres, Redis, Qdrant) runs in Docker; the three
# application services run from your working tree so edits hot-reload.
#
#   ./infra/scripts/dev-up.sh
#
# Pass --build to rebuild the frontend's .next cache from scratch.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOG_DIR="${ROOT_DIR}/.dev-logs"

mkdir -p "$LOG_DIR"

# --- infrastructure -------------------------------------------------------
start_infra() {
  echo "==> infrastructure"
  if docker ps --format '{{.Names}}' | grep -qx 'vibeai-pg'; then
    echo "    postgres  already running"
  else
    docker run -d --name vibeai-pg \
      -e POSTGRES_USER=vibeai -e POSTGRES_PASSWORD=vibeai -e POSTGRES_DB=vibeai \
      -p 5432:5432 postgres:16-alpine > /dev/null
    echo "    postgres  started"
  fi

  if docker ps --format '{{.Names}}' | grep -qx 'vibeai-redis'; then
    echo "    redis     already running"
  else
    docker run -d --name vibeai-redis -p 6379:6379 redis:7-alpine > /dev/null
    echo "    redis     started"
  fi

  if docker ps --format '{{.Names}}' | grep -qx 'vibeai-qdrant'; then
    echo "    qdrant    already running"
  else
    docker run -d --name vibeai-qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant:v1.12.4 > /dev/null
    echo "    qdrant    started"
  fi
}

# --- environment files ----------------------------------------------------
ensure_env() {
  for svc in website/frontend website/backend ai-engine; do
    target="$ROOT_DIR/$svc/.env"
    [ "$svc" = "website/frontend" ] && target="$ROOT_DIR/$svc/.env.local"
    if [ ! -f "$target" ]; then
      cp "$ROOT_DIR/$svc/.env.example" "$target"
      echo "    created $svc/$(basename "$target") from example"
    fi
  done

  # Better Auth's session cookie has to be verifiable by website/backend, so
  # both sides need the same secret.
  local frontend_secret backend_secret
  frontend_secret="$(grep '^BETTER_AUTH_SECRET=' "$ROOT_DIR/website/frontend/.env.local" | cut -d= -f2-)"
  backend_secret="$(grep '^BETTER_AUTH_SECRET=' "$ROOT_DIR/website/backend/.env" | cut -d= -f2-)"
  if [ "$frontend_secret" != "$backend_secret" ]; then
    local shared
    shared="$(openssl rand -hex 32)"
    for f in "$ROOT_DIR/website/frontend/.env.local" "$ROOT_DIR/website/backend/.env"; do
      sed -i "s|^BETTER_AUTH_SECRET=.*|BETTER_AUTH_SECRET=$shared|" "$f"
    done
    echo "    synced BETTER_AUTH_SECRET across frontend and backend"
  fi
}

# --- database -------------------------------------------------------------
run_migrations() {
  echo "==> migrations"
  if [ ! -d "$ROOT_DIR/website/backend/.venv" ]; then
    echo "    skipped (no virtualenv yet — run: cd website/backend && uv venv --python 3.12 .venv && uv pip install --python .venv -e '.[dev]')"
    return
  fi
  (cd "$ROOT_DIR/website/backend" && \
    DATABASE_URL="postgresql+asyncpg://vibeai:vibeai@localhost:5432/vibeai" \
    .venv/bin/alembic upgrade head)
}

# --- application services -------------------------------------------------
start_service() {
  local name="$1" dir="$2" cmd="$3"
  if pgrep -f "$cmd" > /dev/null; then
    echo "    $name  already running"
    return
  fi
  (cd "$dir" && setsid nohup $cmd > "$LOG_DIR/$name.log" 2>&1 < /dev/null &)
  echo "    $name  started (log: .dev-logs/$name.log)"
}

start_infra
ensure_env
run_migrations

echo "==> application"
start_service ai-engine "$ROOT_DIR/ai-engine" \
  ".venv/bin/python -m uvicorn service.main:app --host 0.0.0.0 --port 8100"
start_service backend "$ROOT_DIR/website/backend" \
  ".venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

if [ "${1:-}" = "--build" ]; then
  rm -rf "$ROOT_DIR/website/frontend/.next"
fi
start_service frontend "$ROOT_DIR/website/frontend" "npm run dev"

echo
echo "==> waiting for services"
for _ in $(seq 1 30); do
  ok=0
  for port in 3000 8000 8100; do
    curl -sf -m 2 -o /dev/null "http://localhost:$port/" 2>/dev/null || \
      curl -sf -m 2 -o /dev/null "http://localhost:$port/health" 2>/dev/null || ok=1
  done
  [ "$ok" -eq 0 ] && break
  sleep 1
done

echo
echo "  frontend   http://localhost:3000"
echo "  api        http://localhost:8000/api/v1   (docs at /docs)"
echo "  ai-engine  http://localhost:8100"
echo
echo "  Chat needs GROQ_API_KEY in ai-engine/.env — set it to stream replies."
