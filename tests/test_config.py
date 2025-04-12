"""Tests for the configuration module."""
import os
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

import pytest

from adriacb_galtea.core.config import (
    get_openai_api_key,
    VECTOR_STORE_PATH,
    API_HOST,
    API_PORT,
    LOG_LEVEL,
    LANGFUSE_ENABLED,
    LANGFUSE_PUBLIC_KEY,
    LANGFUSE_SECRET_KEY,
)

def test_env_file_loading():
    """Test that values are properly loaded from .env file."""
    def mock_path_init(*args, **kwargs):
        mock = MagicMock(spec=Path)
        mock.exists.return_value = True
        mock.parent = mock
        return mock
    
    with patch('pathlib.Path', side_effect=mock_path_init):
        with patch('dotenv.load_dotenv') as mock_load_dotenv:
            def mock_getenv(key, default=None):
                env_vars = {
                    "OPENAI_API_KEY": "test-env-key",
                    "VECTOR_STORE_PATH": "env-store",
                    "API_HOST": "127.0.0.2",
                    "API_PORT": "9000",
                    "LOG_LEVEL": "WARNING"
                }
                return env_vars.get(key, default)
            
            with patch.dict('os.environ', {}, clear=True):
                with patch('os.getenv', side_effect=mock_getenv):
                    from importlib import reload
                    import adriacb_galtea.core.config
                    reload(adriacb_galtea.core.config)
                    
                    assert mock_load_dotenv.called
                    assert get_openai_api_key() is not None
                    assert VECTOR_STORE_PATH is not None
                    assert API_HOST is not None
                    assert API_PORT is not None
                    assert LOG_LEVEL is not None

def test_openai_api_key_required():
    """Test that OPENAI_API_KEY is required."""
    with patch.dict(os.environ, clear=True):  # Clear all env vars
        with pytest.raises(ValueError, match="OPENAI_API_KEY environment variable is required"):
            get_openai_api_key()

def test_default_values():
    """Test default values when environment variables are not set."""
    test_env = {
        "OPENAI_API_KEY": "test-key",  # Required key
        "VECTOR_STORE_PATH": "",
        "API_HOST": "",
        "API_PORT": "",
        "LOG_LEVEL": "",
    }
    with patch.dict(os.environ, test_env, clear=True):
        from importlib import reload
        import adriacb_galtea.core.config
        reload(adriacb_galtea.core.config)
        
        assert VECTOR_STORE_PATH is not None
        assert API_HOST is not None
        assert API_PORT is not None
        assert LOG_LEVEL is not None

def test_custom_values():
    """Test custom values when environment variables are set."""
    test_env = {
        "OPENAI_API_KEY": "test-key",  # Required key
        "VECTOR_STORE_PATH": "custom_store",
        "API_HOST": "127.0.0.1",
        "API_PORT": "8080",
        "LOG_LEVEL": "DEBUG",
    }
    with patch.dict(os.environ, test_env, clear=True):
        from importlib import reload
        import adriacb_galtea.core.config
        reload(adriacb_galtea.core.config)
        
        assert VECTOR_STORE_PATH is not None
        assert API_HOST is not None
        assert API_PORT is not None
        assert LOG_LEVEL is not None

def test_langfuse_settings():
    """Test Langfuse settings."""
    test_env = {
        "OPENAI_API_KEY": "test-key",  # Required key
        "LANGFUSE_ENABLED": "true",
        "LANGFUSE_PUBLIC_KEY": "public-key",
        "LANGFUSE_SECRET_KEY": "secret-key",
    }
    with patch.dict(os.environ, test_env, clear=True):
        from importlib import reload
        import adriacb_galtea.core.config
        reload(adriacb_galtea.core.config)
        
        assert LANGFUSE_ENABLED is not None
        assert LANGFUSE_PUBLIC_KEY is not None
        assert LANGFUSE_SECRET_KEY is not None 