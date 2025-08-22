from pydantic import BaseModel, Field
from typing import Any, Optional, Literal
from enum import Enum


class ActionType(str, Enum):
    CREATE = "create"
    EDIT = "edit"
    VIEW = "view"


class BaseActionRequest(BaseModel):
    """Base request schema for all endpoints."""
    action: ActionType = Field(..., description="Action to perform: create, edit, or view")
    data: Optional[dict] = Field(None, description="Data for the action")


class UserActionRequest(BaseActionRequest):
    """Request schema for user endpoints."""
    data: Optional[dict] = Field(None, description="User data for the action")


class TaskActionRequest(BaseActionRequest):
    """Request schema for task endpoints."""
    data: Optional[dict] = Field(None, description="Task data for the action")


class PaginationParams(BaseModel):
    """Pagination parameters for list operations."""
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(10, ge=1, le=100, description="Page size")
    sort_by: Optional[str] = Field(None, description="Field to sort by")
    sort_order: Literal["asc", "desc"] = Field("asc", description="Sort order")


class FilterParams(BaseModel):
    """Filter parameters for search operations."""
    search: Optional[str] = Field(None, description="Search term")
    status: Optional[str] = Field(None, description="Filter by status")
    priority: Optional[str] = Field(None, description="Filter by priority")
    owner_id: Optional[int] = Field(None, description="Filter by owner ID")
