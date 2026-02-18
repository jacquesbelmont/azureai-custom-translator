from __future__ import annotations

from typing import Optional

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

from app.core.settings import settings
from app.core.runtime_config import get_override


class AzureTranslatorAuthError(RuntimeError):
    pass


class AzureTranslatorQuotaError(RuntimeError):
    pass


class AzureTranslatorTransientError(RuntimeError):
    pass


def _headers() -> dict:
    key = get_override("azure_translator_key") or settings.azure_translator_key
    region = get_override("azure_translator_region") or settings.azure_translator_region
    if not key or not region:
        raise ValueError("Azure Translator is not configured. Set AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION.")
    return {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
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
    category: Optional[str],
) -> str:
    endpoint = get_override("azure_translator_endpoint") or settings.azure_translator_endpoint
    url = f"{endpoint.rstrip('/')}/translate"

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
