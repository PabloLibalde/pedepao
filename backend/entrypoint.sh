#!/usr/bin/env bash
set -e
export PYTHONPATH=/app
alembic upgrade head || true
uvicorn app.main:app --host 0.0.0.0 --port 8000