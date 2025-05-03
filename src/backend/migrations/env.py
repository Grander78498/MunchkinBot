# pylint: skip-file
"""Настройка миграций."""
import asyncio
import os
from pathlib import Path
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import pool, MetaData
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context
import alembic_postgresql_enum

from backend.database.enums import *
from backend.database.link_models import *
from backend.database.users import *
from backend.database.game import *
from backend.database.cards import *
from backend.database.actions import *
from backend.database.conditions import *
from backend.database import CustomSQLModel

current_dir = Path().absolute()
load_dotenv(current_dir.parent.parent.joinpath(".env"))

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = CustomSQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    db_url = os.getenv("DB_URL")
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run async migrations.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = create_async_engine(os.getenv("DB_URL"))

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
