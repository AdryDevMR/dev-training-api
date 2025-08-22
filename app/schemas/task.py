from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.task import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    owner_id: int


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class TaskResponse(TaskBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TaskWithOwner(TaskResponse):
    owner: dict  # Will contain user info
