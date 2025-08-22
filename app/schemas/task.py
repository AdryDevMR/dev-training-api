from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, computed_field
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
    URGENT = "urgent"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Current task status")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Task priority level")
    due_date: Optional[datetime] = Field(None, description="Task due date")
    is_completed: bool = Field(default=False, description="Whether the task is completed")


class TaskCreate(TaskBase):
    user_id: int = Field(..., description="ID of the user who owns this task")


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    status: Optional[TaskStatus] = Field(None, description="Current task status")
    priority: Optional[TaskPriority] = Field(None, description="Task priority level")
    due_date: Optional[datetime] = Field(None, description="Task due date")
    is_completed: Optional[bool] = Field(None, description="Whether the task is completed")


class TaskResponse(TaskBase):
    id: int = Field(..., description="Unique task ID")
    user_id: int = Field(..., description="ID of the user who owns this task")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Task last update timestamp")
    
    @computed_field
    @property
    def created_at_iso(self) -> str:
        return self.created_at.isoformat()
    
    @computed_field
    @property
    def updated_at_iso(self) -> str:
        return self.updated_at.isoformat()
    
    @computed_field
    @property
    def due_date_iso(self) -> Optional[str]:
        return self.due_date.isoformat() if self.due_date else None
    
    class Config:
        from_attributes = True


class TaskInDB(TaskResponse):
    pass


class TaskActionRequest(BaseModel):
    action: str = Field(..., description="Action to perform: create, edit, or view")
    data: Optional[dict] = Field(None, description="Data for the action")
