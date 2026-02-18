from __future__ import annotations

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

from app.core.settings import settings


class AzureTranslatorAuthError(RuntimeError):
    pass


class AzureTranslatorQuotaError(RuntimeError):
    pass


class AzureTranslatorTransientError(RuntimeError):
    pass


def _headers() -> dict:
    if not settings.azure_translator_key or not settings.azure_translator_region:
        raise ValueError("Azure Translator is not configured. Set AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION.")
    return {
        "Ocp-Apim-Subscription-Key": settings.azure_translator_key,
        "Ocp-Apim-Subscription-Region": settings.azure_translator_region,
        "Content-Type": "application/json",
    }


@retry(
    retry=retry_if_exception_type((AzureTranslatorQuotaError, AzureTranslatorTransientError, httpx.TimeoutException)),
    stop=stop_after_attempt(6),
    wait=wait_exponential_jitter(initial=1, max=20),
)
def translate_text(
    text: str,
    source_language: str,
    target_language: str,
    category: str | None,
) -> str:
    url = f"{settings.azure_translator_endpoint.rstrip('/')}/translate"

    params: dict[str, str] = {
        "api-version": "3.0",
        "from": source_language,
        "to": target_language,
    }
    if category:
        params["category"] = category

    body = [{"text": text}]

    try:
        resp = httpx.post(url, params=params, headers=_headers(), json=body, timeout=20)
    except httpx.TimeoutException:
        raise

    if resp.status_code in (401, 403):
        raise AzureTranslatorAuthError(f"Azure Translator auth failed (status={resp.status_code}).")
    if resp.status_code == 429:
        raise AzureTranslatorQuotaError("Azure Translator quota/rate limit reached (429).")
    if resp.status_code >= 500:
        raise AzureTranslatorTransientError(f"Azure Translator transient error (status={resp.status_code}).")

    resp.raise_for_status()
    data = resp.json()
    return data[0]["translations"][0]["text"]
