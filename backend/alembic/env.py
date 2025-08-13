from __future__ import annotations

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.db.base import Base  # noqa: F401
# IMPORTANTE: importe os módulos de modelos para que Base.metadata tenha todas as tabelas
from app.db.models import product, order, offer  # noqa: F401

# puxa URL do banco das envs ou do settings do projeto
try:
    from app.core.config import settings
except Exception:  # fallback se settings não puder ser importado
    settings = None

config = context.config

# logging do alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- DEFINIR URL DO BANCO AQUI ---
database_url = (
    os.getenv("DATABASE_URL")
    or (getattr(settings, "database_url", None) if settings else None)
)

if not database_url:
    raise RuntimeError(
        "DATABASE_URL não definido. Configure-o no .env/compose ou em app.core.config.Settings."
    )

config.set_main_option("sqlalchemy.url", database_url)
# ---------------------------------

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
