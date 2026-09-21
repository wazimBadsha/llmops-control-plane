from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "local"
    log_level: str = "INFO"
    api_key: str | None = None
    llm_provider: str = "mock"
    llm_base_url: str = "http://127.0.0.1:11434/v1"
    llm_api_key: str | None = None
    llm_model: str = "local-model"
    llm_timeout_seconds: float = 20.0
    retrieval_top_k: int = 4
    max_context_chars: int = 6000
    eval_min_score: float = 0.75
    mlflow_tracking_uri: str | None = None
    otel_exporter_otlp_endpoint: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
