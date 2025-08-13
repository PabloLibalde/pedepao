from __future__ import annotations

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# === Carrega o Base e os modelos do projeto ===
from app.db.base import Base  # noqa: F401
# IMPORTANTE: importe os módulos de modelos para que as tabelas entrem no Base.metadata
from app.db.models import product, order, offer  # noqa: F401

# Config do Alembic
config = context.config

# Configura logging se existir seção [loggers] no alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Define o metadata alvo (usado no autogenerate)
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
