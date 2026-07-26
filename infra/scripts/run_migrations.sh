#!/usr/bin/env bash
# Runs Alembic migrations against the configured DATABASE_URL.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../../website/backend"
alembic upgrade head
