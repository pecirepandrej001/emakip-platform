from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "EMAKIP"
    app_env: str = "development"
    app_debug: bool = False
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    ui_port: int = 8501
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 60

    database_url: str = "sqlite+aiosqlite:///./emakip.db"
    redis_url: str = "redis://localhost:6379/0"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "emakip_documents"

    mlflow_tracking_uri: str = "http://localhost:5000"
    langsmith_tracing: bool = False
    langsmith_api_key: str = ""
    langsmith_project: str = "emakip"

    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    top_k: int = 8
    rerank_top_k: int = 4
    chunk_size: int = 700
    chunk_overlap: int = 100

    api_base_url: str = "http://localhost:8000"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()
