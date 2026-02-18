from typing import Optional
from pydantic import BaseModel, Field


class TextTranslateRequest(BaseModel):
    text: str = Field(min_length=1)
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    category: Optional[str] = None
    enable_post_edit: bool = True


class UrlTranslateRequest(BaseModel):
    url: str = Field(min_length=5)
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    category: Optional[str] = None
    enable_post_edit: bool = True


class DbTranslateRequest(BaseModel):
    limit: int = Field(default=100, ge=1, le=5000)
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    category: Optional[str] = None
    enable_post_edit: bool = True
