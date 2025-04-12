"""Logging configuration for the application."""
import logging
import sys
import structlog

def configure_logging(level: str = "INFO") -> None:
    """Configure structlog for the application.
    
    Args:
        level: Logging level (default: INFO)
    """
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=level
    )
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.dev.ConsoleRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelName(level)),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True
    )

def get_logger(name: str) -> structlog.BoundLogger:
    """Get a configured logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name) 