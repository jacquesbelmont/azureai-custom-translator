from pydantic import BaseModel


class ProviderMeta(BaseModel):
    azure_used: bool
    openai_used: bool
    category_used: str | None = None


class TextTranslateResponse(BaseModel):
    source_text: str
    translated_text: str
    post_edited_text: str | None = None
    provider_meta: ProviderMeta


class UrlTranslateResponse(BaseModel):
    url: str
    source_markdown: str
    translated_markdown: str
    post_edited_markdown: str | None = None
    title: str | None = None
    provider_meta: ProviderMeta


class DbTranslateResponse(BaseModel):
    processed: int
    cached_hits: int
    translated: int
    failed: int
    errors: list[str]
    provider_meta: ProviderMeta
