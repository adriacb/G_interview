"""Configuration module for the RAG application."""
from pathlib import Path
import os
from typing import Optional
from dotenv import load_dotenv
from .config.settings import settings

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path, override=True)  # Override existing env vars with .env values

# Export settings for backward compatibility
VECTOR_STORE_PATH = settings.VECTOR_STORE_PATH
API_HOST = settings.API_HOST
API_PORT = settings.API_PORT
LOG_LEVEL = settings.LOG_LEVEL
LANGFUSE_ENABLED = bool(settings.LANGFUSE_PUBLIC_KEY and settings.LANGFUSE_SECRET_KEY)
LANGFUSE_PUBLIC_KEY = settings.LANGFUSE_PUBLIC_KEY
LANGFUSE_SECRET_KEY = settings.LANGFUSE_SECRET_KEY

# Vector store settings
VECTOR_STORE_PATH: str = os.getenv("VECTOR_STORE_PATH", "data/vector_store")

# API settings
API_HOST: str = os.getenv("API_HOST") or "0.0.0.0"
API_PORT: int = int(os.getenv("API_PORT") or "8000")

# Logging settings
LOG_LEVEL: str = os.getenv("LOG_LEVEL") or "INFO"

# Langfuse settings (for future use)
LANGFUSE_ENABLED: bool = (os.getenv("LANGFUSE_ENABLED") or "false").lower() == "true"
LANGFUSE_PUBLIC_KEY: Optional[str] = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY: Optional[str] = os.getenv("LANGFUSE_SECRET_KEY") 