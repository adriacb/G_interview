"""Langfuse service for monitoring and tracing."""
from typing import Optional
from langfuse import Langfuse
from langfuse.callback import CallbackHandler

from ..utils.logging import get_logger

logger = get_logger(__name__)


def create_langfuse_callback(settings) -> Optional[CallbackHandler]:
    """Create a Langfuse callback handler with the given settings.
    Returns None if credentials are not provided."""
    if not settings.LANGFUSE_PUBLIC_KEY or not settings.LANGFUSE_SECRET_KEY:
        logger.warning("Langfuse client is disabled - missing credentials")
        return None

    try:
        return CallbackHandler(
            public_key=settings.LANGFUSE_PUBLIC_KEY,
            secret_key=settings.LANGFUSE_SECRET_KEY,
            host=settings.LANGFUSE_HOST,
            timeout=settings.LANGFUSE_TIMEOUT,
            tags=settings.LANGFUSE_TAGS.split(",") if settings.LANGFUSE_TAGS else [],
            version=settings.LANGFUSE_VERSION,
            release=settings.LANGFUSE_RELEASE,
            environment=settings.LANGFUSE_ENVIRONMENT
        )
    except Exception as e:
        logger.error(f"Failed to create Langfuse client: {e}")
        return None


def get_langfuse_callback(settings) -> Optional[CallbackHandler]:
    """Get a Langfuse callback handler with the given settings.
    Returns None if credentials are not provided."""
    return create_langfuse_callback(settings)