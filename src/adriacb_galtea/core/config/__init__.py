"""Configuration package for the RAG application."""
from .settings import Settings, settings

def load_env() -> None:
    """Load environment variables from .env file."""
    # The settings instance will automatically load from .env
    _ = settings

__all__ = ["Settings", "settings"] 