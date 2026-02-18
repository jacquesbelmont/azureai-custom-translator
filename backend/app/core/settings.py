from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    azure_translator_endpoint: str = "https://api.cognitive.microsofttranslator.com"
    azure_translator_key: str = ""
    azure_translator_region: str = ""
    azure_translator_category: str = ""

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    translation_from: str = "en"
    translation_to: str = "pt-br"

    postgres_dsn: str = "postgresql://postgres:postgres@localhost:5432/postgres"

    source_table: str = "source_texts"
    source_id_column: str = "id"
    source_text_column: str = "source_text"

    target_table: str = "translated_texts"
    target_id_column: str = "id"
    target_text_column: str = "translated_text"

    cache_table: str = "translation_cache"

    cors_allow_origins: str = "http://localhost:4321,http://127.0.0.1:4321"

    @property
    def cors_allow_origins_list(self) -> List[str]:
        return [o.strip() for o in self.cors_allow_origins.split(",") if o.strip()]


settings = Settings()
