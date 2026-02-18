from __future__ import annotations

from openai import OpenAI

from app.core.settings import settings


def is_configured() -> bool:
    return bool(settings.openai_api_key)


def post_edit_text(
    *,
    source_text: str,
    translated_text: str,
    source_language: str,
    target_language: str,
) -> str:
    if not is_configured():
        raise ValueError("OpenAI is not configured.")

    client = OpenAI(api_key=settings.openai_api_key)

    prompt = (
        "You are a translation post-editor. Improve fluency, fix awkward phrases, "
        "and keep meaning identical. Return only the final text. "
        f"Source language: {source_language}. Target language: {target_language}.\n\n"
        "SOURCE:\n"
        f"{source_text}\n\n"
        "TRANSLATION:\n"
        f"{translated_text}\n"
    )

    resp = client.responses.create(
        model=settings.openai_model,
        input=prompt,
    )

    return (resp.output_text or "").strip()


def post_edit_markdown(
    *,
    source_markdown: str,
    translated_markdown: str,
    source_language: str,
    target_language: str,
) -> str:
    if not is_configured():
        raise ValueError("OpenAI is not configured.")

    client = OpenAI(api_key=settings.openai_api_key)

    prompt = (
        "You are a translation post-editor for Markdown. Improve readability and formatting "
        "while preserving structure (headings, lists, links). Return only valid Markdown. "
        f"Source language: {source_language}. Target language: {target_language}.\n\n"
        "SOURCE MARKDOWN:\n"
        f"{source_markdown}\n\n"
        "TRANSLATED MARKDOWN:\n"
        f"{translated_markdown}\n"
    )

    resp = client.responses.create(
        model=settings.openai_model,
        input=prompt,
    )

    return (resp.output_text or "").strip()
