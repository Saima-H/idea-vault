from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine # <-- Added create_engine
from alembic import context
from database import Base
import models
from dotenv import load_dotenv
import os

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # Load the database URL from .env
    load_dotenv()
    url = os.getenv("DATABASE_URL")
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # 1. Load the database URL from .env
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")

    # 2. Create the engine using the URL
    connectable = create_engine(db_url, poolclass=pool.NullPool)

    # 3. Connect and run the migrations
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()