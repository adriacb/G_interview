"""Configuration module for the RAG application."""
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Settings for the RAG application."""
    
    # OpenAI settings
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    
    # Vector store settings
    VECTOR_STORE_PATH: str = Field("vector_store", env="VECTOR_STORE_PATH")
    
    # API settings
    API_HOST: str = Field("0.0.0.0", env="API_HOST")
    API_PORT: int = Field(8000, env="API_PORT")
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings() 