from __future__ import annotations

from app.core.settings import settings
from app.db.cache import cache_get, cache_put, make_cache_key
from app.db.jobs import run_db_job
from app.models.requests import DbTranslateRequest, TextTranslateRequest, UrlTranslateRequest
from app.models.responses import (
    DbTranslateResponse,
    ProviderMeta,
    TextTranslateResponse,
    UrlTranslateResponse,
)
from app.services.azure_translator import translate_text as azure_translate
from app.services.openai_postedit import is_configured as openai_is_configured
from app.services.openai_postedit import post_edit_markdown, post_edit_text
from app.services.url_extract import extract_main_text, fetch_html, to_markdown


def _resolve_lang(req_source: str | None, req_target: str | None) -> tuple[str, str]:
    return (req_source or settings.translation_from, req_target or settings.translation_to)


def _resolve_category(req_category: str | None) -> str | None:
    return req_category or (settings.azure_translator_category or None)


def translate_text_pipeline(req: TextTranslateRequest) -> TextTranslateResponse:
    source_lang, target_lang = _resolve_lang(req.source_language, req.target_language)
    category = _resolve_category(req.category)

    cache_key = make_cache_key(req.text, source_lang, target_lang, category)
    cached = cache_get(cache_key)
    if cached:
        return TextTranslateResponse(
            source_text=req.text,
            translated_text=cached["translated_text"],
            post_edited_text=cached.get("post_edited_text"),
            provider_meta=ProviderMeta(
                azure_used=False,
                openai_used=bool(cached.get("post_edited_text")),
                category_used=category,
            ),
        )

    translated = azure_translate(req.text, source_lang, target_lang, category)

    post_edited: str | None = None
    if req.enable_post_edit and openai_is_configured():
        post_edited = post_edit_text(
            source_text=req.text,
            translated_text=translated,
            source_language=source_lang,
            target_language=target_lang,
        )

    cache_put(cache_key, source_lang, target_lang, category, req.text, translated, post_edited)

    return TextTranslateResponse(
        source_text=req.text,
        translated_text=translated,
        post_edited_text=post_edited,
        provider_meta=ProviderMeta(azure_used=True, openai_used=bool(post_edited), category_used=category),
    )


def translate_url_pipeline(req: UrlTranslateRequest) -> UrlTranslateResponse:
    source_lang, target_lang = _resolve_lang(req.source_language, req.target_language)
    category = _resolve_category(req.category)

    html = fetch_html(req.url)
    title, text = extract_main_text(html)
    source_md = to_markdown(text)

    cache_key = make_cache_key(source_md, source_lang, target_lang, category)
    cached = cache_get(cache_key)
    if cached:
        return UrlTranslateResponse(
            url=req.url,
            title=title,
            source_markdown=source_md,
            translated_markdown=cached["translated_text"],
            post_edited_markdown=cached.get("post_edited_text"),
            provider_meta=ProviderMeta(
                azure_used=False,
                openai_used=bool(cached.get("post_edited_text")),
                category_used=category,
            ),
        )

    translated_md = azure_translate(source_md, source_lang, target_lang, category)

    post_edited_md: str | None = None
    if req.enable_post_edit and openai_is_configured():
        post_edited_md = post_edit_markdown(
            source_markdown=source_md,
            translated_markdown=translated_md,
            source_language=source_lang,
            target_language=target_lang,
        )

    cache_put(cache_key, source_lang, target_lang, category, source_md, translated_md, post_edited_md)

    return UrlTranslateResponse(
        url=req.url,
        title=title,
        source_markdown=source_md,
        translated_markdown=translated_md,
        post_edited_markdown=post_edited_md,
        provider_meta=ProviderMeta(azure_used=True, openai_used=bool(post_edited_md), category_used=category),
    )


def translate_db_pipeline(req: DbTranslateRequest) -> DbTranslateResponse:
    source_lang, target_lang = _resolve_lang(req.source_language, req.target_language)
    category = _resolve_category(req.category)

    result = run_db_job(
        limit=req.limit,
        source_language=source_lang,
        target_language=target_lang,
        category=category,
        enable_post_edit=req.enable_post_edit and openai_is_configured(),
    )

    return DbTranslateResponse(
        processed=result["processed"],
        cached_hits=result["cached_hits"],
        translated=result["translated"],
        failed=result["failed"],
        errors=result["errors"],
        provider_meta=ProviderMeta(
            azure_used=result["azure_used"],
            openai_used=result["openai_used"],
            category_used=category,
        ),
    )
