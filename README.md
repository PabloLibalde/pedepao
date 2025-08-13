# PedePao (versão refatorada)

Projeto exemplo com melhorias:
- Backend FastAPI + SQLAlchemy 2.x + Alembic
- Regras: **1 pedido por usuário/dia**; cutoff configurável (padrão 13:00 America/Sao_Paulo)
- Cliente desktop **PySide6** com bloqueio pós-cutoff
- Docker/Compose (PostgreSQL + API)
- CI (GitHub Actions), lint (ruff), type-check (mypy) e pre-commit

## Python
Validado com **Python 3.13.6**.

## Como subir
```bash
cp .env.example .env
docker compose up -d --build
# A API sobe em http://localhost:8000
# Swagger: http://localhost:8000/docs
```

## Cliente (PySide6)
Com Python 3.13.6:
```bash
python -m venv .venv && . .venv/bin/activate  # (Linux/Mac)
# Windows: .venv\Scripts\activate
pip install -r client/requirements.txt
python client/app.py
```

**Terminologia:** Produtos = itens do catálogo; Ofertas = o que está liberado para seleção pelos usuários.
