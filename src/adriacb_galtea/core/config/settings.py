"""Settings module for the RAG application."""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # Vector store settings
    VECTOR_STORE_PATH: str = Field(env="VECTOR_STORE_PATH")
    
    # API settings
    API_HOST: str = Field("0.0.0.0", env="API_HOST")
    API_PORT: int = Field(8000, env="API_PORT")
    API_WORKERS: int = Field(1, env="API_WORKERS")
    
    # Logging settings
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field("%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT")
    
    # Langfuse settings
    LANGFUSE_PUBLIC_KEY: str = Field("", env="LANGFUSE_PUBLIC_KEY")
    LANGFUSE_SECRET_KEY: str = Field("", env="LANGFUSE_SECRET_KEY")
    LANGFUSE_HOST: str = Field("https://cloud.langfuse.com", env="LANGFUSE_HOST")
    LANGFUSE_ENVIRONMENT: str = Field("development", env="LANGFUSE_ENVIRONMENT")
    
    # Document processor settings
    DOCUMENT_PROCESSOR_HOST: str = Field("0.0.0.0", env="DOCUMENT_PROCESSOR_HOST")
    DOCUMENT_PROCESSOR_PORT: int = Field(8002, env="DOCUMENT_PROCESSOR_PORT")
    
    # Embedding settings
    EMBEDDING_MODEL: str = Field("sentence-transformers/all-MiniLM-L6-v2", env="EMBEDDING_MODEL")
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Create settings instance
settings = Settings() 