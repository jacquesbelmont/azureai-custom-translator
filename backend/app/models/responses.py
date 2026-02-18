from typing import List, Optional
from pydantic import BaseModel


class ProviderMeta(BaseModel):
    azure_used: bool
    openai_used: bool
    category_used: Optional[str] = None


class TextTranslateResponse(BaseModel):
    source_text: str
    translated_text: str
    post_edited_text: Optional[str] = None
    provider_meta: ProviderMeta


class UrlTranslateResponse(BaseModel):
    url: str
    source_markdown: str
    translated_markdown: str
    post_edited_markdown: Optional[str] = None
    title: Optional[str] = None
    provider_meta: ProviderMeta


class DbTranslateResponse(BaseModel):
    processed: int
    cached_hits: int
    translated: int
    failed: int
    errors: List[str]
    provider_meta: ProviderMeta
