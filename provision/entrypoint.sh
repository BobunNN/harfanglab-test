#!/bin/sh
set -e
# sh /app/provision/init_db.sh
uv run alembic upgrade head
uv run uvicorn src.app.main:app --reload --port 8080 --host 0.0.0.0
