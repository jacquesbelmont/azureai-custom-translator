from contextlib import contextmanager

import psycopg

from app.core.settings import settings


@contextmanager
def get_conn():
    with psycopg.connect(settings.postgres_dsn) as conn:
        yield conn
