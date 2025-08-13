# PedePao

MVP de uma aplicação de pedidos de lanches para funcionários.

## Componentes
- **backend/**: API FastAPI + PostgreSQL (SQLAlchemy 2.x, Alembic).
- **client/**: Aplicativo desktop (Windows/macOS/Linux) com PySide6.
- **Docker**: `docker-compose.yml` para subir Postgres e API.

## Requisitos
- Python 3.13.6
- Docker / Docker Compose (para backend)
- Windows 10/11 (cliente; usa `pywin32` opcionalmente)

## Passos rápidos

### Backend
```bash
cd backend
docker compose up -d --build
# Criar tabelas
docker compose exec api bash -lc "alembic upgrade head"
```

### Cliente (Windows)
```bash
cd client/app
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt pyinstaller
# Ajuste o api_base no config.json
.venv\Scripts\pyinstaller --noconsole --name PedePao main.py
# Executável em dist\PedePao\PedePao.exe
```

## Notas
- Todos horários salvos em UTC; a lógica de corte (cutoff) usa TZ `America/Sao_Paulo`.
- Um pedido por usuário por dia. Admin gerencia ofertas e janelas (períodos) e define `cutoff` (padrão 13:00).
