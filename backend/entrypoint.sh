#!/usr/bin/env bash
export PYTHONPATH=/app
set -e
# aplica migrações
alembic upgrade head || true
# inicia a API
uvicorn app.main:app --host 0.0.0.0 --port 8000
