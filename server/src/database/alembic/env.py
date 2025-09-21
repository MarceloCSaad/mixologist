import os
import pkgutil
import importlib
import sys

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from src.database.constants import POSTGRESQL__PSYCOPG2__DB_URI
from src.models.base_model import BaseModel


def import_all_models():
    """
    Dynamically import all modules in the src.models package and its subpackages.
    Ensures all SQLAlchemy models are registered with the Base metadata for Alembic.
    """
    # Get the project root (assumes this file is in server/src/database/alembic/)
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../..")
    )
    models_path = os.path.join(project_root, "src", "models")
    package_name = "src.models"

    if project_root not in sys.path:
        sys.path.append(project_root)

    for _importer, modname, _ispkg in pkgutil.walk_packages(
        [models_path], prefix=package_name + "."
    ):
        importlib.import_module(modname)


# Dynamically import all models for Alembic autogenerate
import_all_models()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Override the sqlalchemy.url .ini with .env.development created setting variable
config.set_main_option("sqlalchemy.url", POSTGRESQL__PSYCOPG2__DB_URI)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None
target_metadata = BaseModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
