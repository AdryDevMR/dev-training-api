from pydantic import BaseModel, Field
from typing import Any, Generic, TypeVar, Optional
from enum import Enum

class ActionType(str, Enum):
    CREATE = "create"
    EDIT = "edit"
    VIEW = "view"

class BaseRequest(BaseModel):
    """Base request model that all API requests must follow."""
    action: ActionType = Field(..., description="Action to perform: create, edit, or view")
    
    class Config:
        json_schema_extra = {
            "example": {
                "action": "view"
            }
        }

class ErrorResponse(BaseModel):
    """Standard error response format."""
    reason: str = Field(..., description="User-friendly error message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "reason": "User not found"
            }
        }

class SuccessResponse(BaseModel):
    """Standard success response format."""
    success: bool = True
    data: Optional[Any] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {"id": 1, "name": "John Doe"}
            }
        }

# Generic type for paginated responses
T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response model."""
    items: list[T]
    total: int
    page: int
    size: int
    pages: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}],
                "total": 2,
                "page": 1,
                "size": 10,
                "pages": 1
            }
        }
