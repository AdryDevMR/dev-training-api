#!/usr/bin/env python3
"""
Startup script for the User Account and Tasks API
"""

import uvicorn
from app.config import settings
from app.utils.logging import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("Starting User Account and Tasks API...")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.log_level.lower(),
        access_log=True
    )
