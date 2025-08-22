from typing import Any, Dict, Optional
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.utils.logging import get_logger

logger = get_logger(__name__)


class APIResponse:
    """Custom response handler that ensures only 200/500 status codes."""
    
    @staticmethod
    def success(data: Any = None, message: str = "Success") -> JSONResponse:
        """Return a successful response with 200 status."""
        response_data = {
            "success": True,
            "message": message,
            "data": data
        }
        logger.info(f"Success response: {message}")
        return JSONResponse(content=response_data, status_code=200)
    
    @staticmethod
    def error(reason: str, status_code: int = 200) -> JSONResponse:
        """
        Return an error response.
        Note: Even for errors, we return 200 status with error details in 'reason' field.
        Only server errors (500) are allowed to return different status.
        """
        if status_code != 500:
            status_code = 200
            
        response_data = {
            "success": False,
            "reason": reason
        }
        
        if status_code == 500:
            logger.error(f"Server error: {reason}")
        else:
            logger.warning(f"Client error: {reason}")
            
        return JSONResponse(content=response_data, status_code=status_code)
    
    @staticmethod
    def server_error(reason: str = "Internal server error") -> JSONResponse:
        """Return a server error response with 500 status."""
        return APIResponse.error(reason, status_code=500)


def handle_exception(exc: Exception) -> JSONResponse:
    """Handle exceptions and return appropriate responses."""
    logger.error(f"Exception occurred: {str(exc)}", exc_info=True)
    
    # For known exceptions, return 200 with reason
    if isinstance(exc, ValueError) or isinstance(exc, KeyError):
        return APIResponse.error(str(exc))
    
    # For unknown exceptions, return 500
    return APIResponse.server_error("An unexpected error occurred")
