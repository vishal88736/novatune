#!/usr/bin/env bash
# One-shot local dev setup: copies env templates and brings up the full stack.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

for svc in website/frontend website/backend ai-engine; do
  if [ ! -f "$ROOT_DIR/$svc/.env" ] && [ ! -f "$ROOT_DIR/$svc/.env.local" ]; then
    target=".env"
    [ "$svc" = "website/frontend" ] && target=".env.local"
    cp "$ROOT_DIR/$svc/.env.example" "$ROOT_DIR/$svc/$target"
    echo "Created $svc/$target from example — fill in secrets before continuing."
  fi
done

docker compose -f "$ROOT_DIR/infra/docker/docker-compose.yml" up --build
