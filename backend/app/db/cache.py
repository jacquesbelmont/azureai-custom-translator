import hashlib
from datetime import datetime

from psycopg.rows import dict_row

from app.core.settings import settings
from app.db.conn import get_conn


def make_cache_key(text: str, source_language: str, target_language: str, category: str | None) -> str:
    payload = f"{source_language}|{target_language}|{category or ''}|{text}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def ensure_cache_table() -> None:
    table = settings.cache_table
    with get_conn() as conn:
        conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table} (
              cache_key TEXT PRIMARY KEY,
              source_language TEXT NOT NULL,
              target_language TEXT NOT NULL,
              category TEXT,
              source_text TEXT NOT NULL,
              translated_text TEXT NOT NULL,
              post_edited_text TEXT,
              created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
            """
        )
        conn.commit()


def cache_get(cache_key: str) -> dict | None:
    table = settings.cache_table
    with get_conn() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                f"SELECT translated_text, post_edited_text FROM {table} WHERE cache_key = %s",
                (cache_key,),
            )
            row = cur.fetchone()
            return dict(row) if row else None


def cache_put(
    cache_key: str,
    source_language: str,
    target_language: str,
    category: str | None,
    source_text: str,
    translated_text: str,
    post_edited_text: str | None,
) -> None:
    table = settings.cache_table
    with get_conn() as conn:
        conn.execute(
            f"""
            INSERT INTO {table} (
              cache_key, source_language, target_language, category, source_text,
              translated_text, post_edited_text, created_at
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (cache_key) DO UPDATE SET
              translated_text = EXCLUDED.translated_text,
              post_edited_text = EXCLUDED.post_edited_text
            """,
            (
                cache_key,
                source_language,
                target_language,
                category,
                source_text,
                translated_text,
                post_edited_text,
                datetime.utcnow(),
            ),
        )
        conn.commit()
