from __future__ import annotations

from openai import OpenAI

from app.core.settings import settings
from app.core.runtime_config import get_override


def is_configured() -> bool:
    return bool(get_override("openai_api_key") or settings.openai_api_key)


def _client_and_model() -> tuple[OpenAI, str]:
    api_key = get_override("openai_api_key") or settings.openai_api_key
    model = get_override("openai_model") or settings.openai_model
    if not api_key:
        raise ValueError("OpenAI is not configured.")
    return OpenAI(api_key=api_key), model


def post_edit_text(
    *,
    source_text: str,
    translated_text: str,
    source_language: str,
    target_language: str,
) -> str:
    client, model = _client_and_model()

    prompt = (
        "You are a translation post-editor. Improve fluency, fix awkward phrases, "
        "and keep meaning identical. Return only the final text. "
        f"Source language: {source_language}. Target language: {target_language}.\n\n"
        "SOURCE:\n"
        f"{source_text}\n\n"
        "TRANSLATION:\n"
        f"{translated_text}\n"
    )

    resp = client.responses.create(model=model, input=prompt)

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

    client, model = _client_and_model()

    prompt = (
        "You are a translation post-editor for Markdown. Improve readability and formatting "
        "while preserving structure (headings, lists, links). Return only valid Markdown. "
        f"Source language: {source_language}. Target language: {target_language}.\n\n"
        "SOURCE MARKDOWN:\n"
        f"{source_markdown}\n\n"
        "TRANSLATED MARKDOWN:\n"
        f"{translated_markdown}\n"
    )

    resp = client.responses.create(model=model, input=prompt)

    return (resp.output_text or "").strip()
