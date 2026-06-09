#!/bin/sh
uv run uvicorn src.app.main:app --reload --port 8080 --host 0.0.0.0