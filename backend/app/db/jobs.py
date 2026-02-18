from __future__ import annotations

from typing import List, Optional

from psycopg.rows import dict_row

from app.core.settings import settings
from app.core.runtime_config import get_override
from app.db.cache import cache_get, cache_put, make_cache_key
from app.db.conn import get_conn
from app.services.azure_translator import translate_text as azure_translate
from app.services.openai_postedit import post_edit_text


def _ensure_target_table() -> None:
    target_table = get_override("target_table") or settings.target_table
    target_id_column = get_override("target_id_column") or settings.target_id_column
    target_text_column = get_override("target_text_column") or settings.target_text_column
    with get_conn() as conn:
        conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {target_table} (
              {target_id_column} TEXT PRIMARY KEY,
              {target_text_column} TEXT NOT NULL
            );
            """
        )
        conn.commit()


def run_db_job(
    *,
    limit: int,
    source_language: str,
    target_language: str,
    category: Optional[str],
    enable_post_edit: bool,
) -> dict:
    _ensure_target_table()

    processed = 0
    cached_hits = 0
    translated = 0
    failed = 0
    errors: List[str] = []

    azure_used = False
    openai_used = False

    with get_conn() as conn:
        source_table = get_override("source_table") or settings.source_table
        source_id_column = get_override("source_id_column") or settings.source_id_column
        source_text_column = get_override("source_text_column") or settings.source_text_column

        target_table = get_override("target_table") or settings.target_table
        target_id_column = get_override("target_id_column") or settings.target_id_column
        target_text_column = get_override("target_text_column") or settings.target_text_column

        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                f"""
                SELECT {source_id_column} AS id, {source_text_column} AS text
                FROM {source_table}
                LIMIT %s
                """,
                (limit,),
            )
            rows = cur.fetchall()

        for row in rows:
            processed += 1
            row_id = str(row["id"])
            text = row["text"]

            if not text:
                failed += 1
                errors.append(f"Row {row_id}: empty text")
                continue

            cache_key = make_cache_key(text, source_language, target_language, category)
            cached = cache_get(cache_key)

            if cached:
                cached_hits += 1
                final_text = cached.get("post_edited_text") or cached["translated_text"]
                _upsert_target(conn, row_id, final_text)
                continue

            try:
                azure_used = True
                base_translation = azure_translate(text, source_language, target_language, category)

                post_edited: Optional[str] = None
                if enable_post_edit:
                    openai_used = True
                    post_edited = post_edit_text(
                        source_text=text,
                        translated_text=base_translation,
                        source_language=source_language,
                        target_language=target_language,
                    )

                cache_put(cache_key, source_language, target_language, category, text, base_translation, post_edited)

                final_text = post_edited or base_translation
                _upsert_target(conn, row_id, final_text)
                translated += 1
            except Exception as e:
                failed += 1
                errors.append(f"Row {row_id}: {type(e).__name__}: {e}")

        conn.commit()

    return {
        "processed": processed,
        "cached_hits": cached_hits,
        "translated": translated,
        "failed": failed,
        "errors": errors,
        "azure_used": azure_used,
        "openai_used": openai_used,
    }


def _upsert_target(conn, row_id: str, translated_text: str) -> None:
    target_table = get_override("target_table") or settings.target_table
    target_id_column = get_override("target_id_column") or settings.target_id_column
    target_text_column = get_override("target_text_column") or settings.target_text_column
    conn.execute(
        f"""
        INSERT INTO {target_table} ({target_id_column}, {target_text_column})
        VALUES (%s, %s)
        ON CONFLICT ({target_id_column}) DO UPDATE SET
          {target_text_column} = EXCLUDED.{target_text_column}
        """,
        (row_id, translated_text),
    )
