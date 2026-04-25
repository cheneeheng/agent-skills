#!/usr/bin/env bash
# setup-test-db.sh
# Starts an ephemeral Postgres for integration tests and writes DATABASE_URL to
# .env.test.local. Idempotent — reuses the container if it's already up.
# Tears down with `down`. Designed as a fallback when a project has no existing
# DB harness; prefer the project's existing setup if one is present.
#
# Usage:
#   bash setup-test-db.sh up     # start + emit DATABASE_URL
#   bash setup-test-db.sh down   # stop + remove
#   bash setup-test-db.sh url    # print current DATABASE_URL
#
# Run from the project root.
set -euo pipefail

CMD="${1:-up}"
NAME="claude-test-pg"
PORT="${TEST_DB_PORT:-55432}"
USER="test"
PASS="test"
DB="testdb"
ENV_FILE=".env.test.local"

url() { echo "postgres://$USER:$PASS@127.0.0.1:$PORT/$DB"; }

case "$CMD" in
  up)
    if ! command -v docker >/dev/null; then
      echo "ERROR: docker is required for setup-test-db.sh" >&2
      exit 2
    fi

    if docker ps --format '{{.Names}}' | grep -qx "$NAME"; then
      echo ">> $NAME already running on port $PORT"
    else
      # Remove any stopped container with the same name.
      docker rm -f "$NAME" >/dev/null 2>&1 || true
      echo ">> starting $NAME on port $PORT"
      docker run -d --rm \
        --name "$NAME" \
        -e "POSTGRES_USER=$USER" \
        -e "POSTGRES_PASSWORD=$PASS" \
        -e "POSTGRES_DB=$DB" \
        -p "$PORT:5432" \
        postgres:16-alpine >/dev/null
    fi

    # Wait for readiness (max ~30s).
    for i in $(seq 1 30); do
      if docker exec "$NAME" pg_isready -U "$USER" -d "$DB" >/dev/null 2>&1; then
        echo ">> postgres ready"
        break
      fi
      sleep 1
      if [[ $i -eq 30 ]]; then
        echo "ERROR: postgres did not become ready in 30s" >&2
        exit 1
      fi
    done

    # Write/refresh env file. Keep any existing unrelated vars.
    tmp=$(mktemp)
    if [[ -f "$ENV_FILE" ]]; then
      grep -v '^DATABASE_URL=' "$ENV_FILE" > "$tmp" || true
    fi
    echo "DATABASE_URL=$(url)" >> "$tmp"
    mv "$tmp" "$ENV_FILE"
    echo ">> DATABASE_URL written to $ENV_FILE"
    echo "$(url)"
    ;;

  down)
    docker rm -f "$NAME" >/dev/null 2>&1 || true
    echo ">> $NAME stopped"
    ;;

  url)
    url
    ;;

  *)
    echo "Usage: $0 {up|down|url}" >&2
    exit 2
    ;;
esac
