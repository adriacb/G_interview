"""Settings module for the RAG application."""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Settings for the RAG application."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow"
    )
    
    # OpenAI settings
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    
    # Vector store settings
    VECTOR_STORE_PATH: str = Field("vector_store", env="VECTOR_STORE_PATH")
    
    # API settings
    API_HOST: str = Field("0.0.0.0", env="API_HOST")
    API_PORT: int = Field(8000, env="API_PORT")
    
    # Logging settings
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    
    # Optional settings with defaults
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.0

    # Langfuse settings
    LANGFUSE_PUBLIC_KEY: str = Field("", env="LANGFUSE_PUBLIC_KEY")
    LANGFUSE_SECRET_KEY: str = Field("", env="LANGFUSE_SECRET_KEY")
    LANGFUSE_HOST: str = Field("https://cloud.langfuse.com", env="LANGFUSE_HOST")
    LANGFUSE_TAGS: str = Field("", env="LANGFUSE_TAGS")  # Comma-separated list of tags
    LANGFUSE_TIMEOUT: int = Field(30, env="LANGFUSE_TIMEOUT")
    LANGFUSE_VERSION: str = Field("1.0.0", env="LANGFUSE_VERSION")
    LANGFUSE_RELEASE: str = Field("development", env="LANGFUSE_RELEASE")
    LANGFUSE_ENVIRONMENT: str = Field("development", env="LANGFUSE_ENVIRONMENT")


# Create settings instance
settings = Settings() 