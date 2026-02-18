from __future__ import annotations

from typing import Optional, Tuple

import httpx
import trafilatura
from bs4 import BeautifulSoup
from markdownify import markdownify as md


def fetch_html(url: str) -> str:
    resp = httpx.get(url, timeout=20, follow_redirects=True)
    resp.raise_for_status()
    return resp.text


def extract_main_text(html: str) -> Tuple[Optional[str], str]:
    downloaded = trafilatura.extract(html, include_comments=False, include_tables=True, output_format="xml")

    title: Optional[str] = None
    text: Optional[str] = None

    if downloaded:
        try:
            title = trafilatura.metadata.extract_metadata(html).title
        except Exception:
            title = None

        text = trafilatura.extract(html, include_comments=False, include_tables=True)

    if not text:
        soup = BeautifulSoup(html, "html.parser")
        title = title or (soup.title.string.strip() if soup.title and soup.title.string else None)
        text = soup.get_text("\n")

    return title, text or ""


def to_markdown(text: str) -> str:
    html = "<pre>" + (text or "") + "</pre>"
    return md(html).strip()
