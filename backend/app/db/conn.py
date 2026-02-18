from contextlib import contextmanager

import psycopg

from app.core.settings import settings
from app.core.runtime_config import get_override


@contextmanager
def get_conn():
    dsn = get_override("postgres_dsn") or settings.postgres_dsn
    with psycopg.connect(dsn) as conn:
        yield conn
