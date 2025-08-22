import os
import sys
from loguru import logger
from pathlib import Path
from typing import Optional

from app.core.config import settings

def setup_logging():
    """Configure loguru logging."""
    log_level = settings.LOG_LEVEL
    log_format = settings.LOG_FORMAT
    log_path = Path("logs/app.log")
    
    # Create logs directory if it doesn't exist
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Remove default handler
    logger.remove()
    
    # Add file handler
    logger.add(
        log_path,
        rotation="100 MB",
        retention="30 days",
        level=log_level,
        format=log_format,
        enqueue=True,
        backtrace=True,
        diagnose=False  # Set to True in development, False in production
    )
    
    # Add console handler
    logger.add(
        sys.stderr,
        level=log_level,
        format=log_format,
        enqueue=True,
        backtrace=True,
        diagnose=False
    )
    
    # Configure loguru to use the logger in all modules
    logger.info("Logging is configured")
    
    return logger
