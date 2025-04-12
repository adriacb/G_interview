"""Main application package."""
from .utils.logging import configure_logging
from .config import load_env

# Load environment variables
load_env()

# Configure logging
configure_logging()

__version__ = "0.1.0" 