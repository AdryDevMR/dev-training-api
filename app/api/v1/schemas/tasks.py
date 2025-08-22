from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskBase(BaseModel):
    """Base task model containing common fields."""
    title: str = Field(..., min_length=3, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=2000, description="Detailed task description")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Current status of the task")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Task priority level")
    due_date: Optional[datetime] = Field(None, description="Due date for the task")
    
    @validator('title')
    def validate_title(cls, v):
        v = v.strip()
        if not v:
            raise ValueError('Title cannot be empty')
        return v

class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    assignee_id: Optional[int] = Field(None, description="ID of the user this task is assigned to")

class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    title: Optional[str] = Field(None, min_length=3, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=2000, description="Detailed task description")
    status: Optional[TaskStatus] = Field(None, description="Current status of the task")
    priority: Optional[TaskPriority] = Field(None, description="Task priority level")
    due_date: Optional[datetime] = Field(None, description="Due date for the task")
    assignee_id: Optional[int] = Field(None, description="ID of the user this task is assigned to")

class TaskInDB(TaskBase):
    """Task model for database operations."""
    id: int
    created_by_id: int
    assignee_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TaskResponse(TaskBase):
    """Task model for API responses."""
    id: int
    created_by_id: int
    assignee: Optional['UserResponse'] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TaskListResponse(BaseModel):
    """Response model for listing tasks."""
    tasks: List[TaskResponse]
    total: int

# Update forward refs for TaskResponse
from app.api.v1.schemas.users import UserResponse
TaskResponse.update_forward_refs()
