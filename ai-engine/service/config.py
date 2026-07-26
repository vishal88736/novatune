from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"

    groq_api_key: str = ""
    groq_conversation_model: str = "llama-3.3-70b-versatile"
    groq_fast_model: str = "llama-3.1-8b-instant"
    groq_whisper_model: str = "whisper-large-v3-turbo"

    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""

    huggingface_token: str = ""
    sentence_transformer_model: str = "all-MiniLM-L6-v2"
    goemotions_model_name: str = "SamLowe/roberta-base-go_emotions"

    redis_url: str = "redis://localhost:6379/0"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
