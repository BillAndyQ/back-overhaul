import os
from sqlalchemy.engine import make_url

_DEFAULT_URL = "postgresql://root:password@localhost:5432/postgres"


def _base_url():
    url = make_url(os.getenv("DATABASE_URL", _DEFAULT_URL))
    # "schema" es un parámetro de Prisma; ni psycopg2 ni asyncpg lo aceptan
    query = {k: v for k, v in url.query.items() if k != "schema"}
    return url.set(query=query)


def get_sync_database_url() -> str:
    """URL para el engine síncrono (psycopg2), aunque DATABASE_URL traiga +asyncpg."""
    return _base_url().set(drivername="postgresql").render_as_string(hide_password=False)


def get_async_database_url() -> str:
    """URL para el engine asíncrono (asyncpg), aunque DATABASE_URL no traiga +asyncpg."""
    return _base_url().set(drivername="postgresql+asyncpg").render_as_string(hide_password=False)
