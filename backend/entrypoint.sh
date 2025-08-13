#!/usr/bin/env bash
set -e

# aplica migrações antes de iniciar a API
alembic upgrade head

# inicia a API
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
