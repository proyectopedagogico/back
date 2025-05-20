import logging
from logging.config import fileConfig

from flask import current_app

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None: # Check if config_file_name is set
    fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')


def get_engine():
    try:
        # this works with Flask-SQLAlchemy<3 and Alchemical
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # this works with Flask-SQLAlchemy>=3
        return current_app.extensions['migrate'].db.engine


def get_engine_url():
    try:
        return get_engine().url.render_as_string(hide_password=False).replace(
            '%', '%%')
    except AttributeError:
        return str(get_engine().url).replace('%', '%%')


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

# Set the sqlalchemy.url in the Alembic config based on the Flask app's config
db_url_for_alembic_setup = get_engine_url()
logger.info(f"Setting Alembic's sqlalchemy.url to: {db_url_for_alembic_setup}")
config.set_main_option('sqlalchemy.url', db_url_for_alembic_setup)

# Get the SQLAlchemy db instance from the Flask-Migrate extension
target_db = current_app.extensions['migrate'].db

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_metadata():
    """
    Returns the metadata from the Flask-SQLAlchemy db instance.
    Handles different ways metadata might be stored (e.g., for multiple databases).
    """
    if hasattr(target_db, 'metadatas'): # For Flask-SQLAlchemy with multiple binds
        return target_db.metadatas[None] # Use the default bind's metadata
    return target_db.metadata # For a single database setup


def run_migrations_offline():
    """Run migrations in 'offline' mode.

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
        target_metadata=get_metadata(), # Use the get_metadata() function
        literal_binds=True,
        dialect_opts={"paramstyle": "named"} # Often useful for offline mode
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = get_engine() # Use the get_engine() helper

    # Debug print for the database URL being used by Alembic
    # This was added for debugging, can be kept or removed
    db_url_for_alembic_runtime = str(connectable.url)
    logger.info(f"DEBUG EN env.py (Alembic - online): SQLALCHEMY_DATABASE_URI para Alembic = {db_url_for_alembic_runtime}")


    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(), # Use the get_metadata() function
            compare_type=True, # Useful for detecting column type changes
            # You might want to include schema if you use schemas other than public
            # include_schemas=True, 
            # version_table_schema=target_db.metadata.schema, # If version table is in a specific schema
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    logger.info("Running migrations in offline mode...")
    run_migrations_offline()
else:
    logger.info("Running migrations in online mode...")
    run_migrations_online()