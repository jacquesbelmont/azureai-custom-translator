from typing import Optional

from pydantic import BaseModel


class RuntimeConfigRequest(BaseModel):
    # Backend behavior
    translation_from: Optional[str] = None
    translation_to: Optional[str] = None
    azure_translator_category: Optional[str] = None

    # Azure Translator
    azure_translator_endpoint: Optional[str] = None
    azure_translator_key: Optional[str] = None
    azure_translator_region: Optional[str] = None

    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: Optional[str] = None

    # Postgres + DB job tables
    postgres_dsn: Optional[str] = None

    source_table: Optional[str] = None
    source_id_column: Optional[str] = None
    source_text_column: Optional[str] = None

    target_table: Optional[str] = None
    target_id_column: Optional[str] = None
    target_text_column: Optional[str] = None

    cache_table: Optional[str] = None


class RuntimeConfigResponse(BaseModel):
    applied: bool
    overrides: dict
