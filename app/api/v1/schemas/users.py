from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserBase(BaseModel):
    """Base user model containing common fields."""
    email: EmailStr = Field(..., description="User's email address")
    full_name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    role: UserRole = Field(default=UserRole.USER, description="User's role")
    is_active: bool = Field(default=True, description="Whether the user is active")

class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, max_length=100, description="User's password (min 8 characters)")
    
    @validator('password')
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        return v

class UserUpdate(BaseModel):
    """Schema for updating an existing user."""
    email: Optional[EmailStr] = Field(None, description="User's email address")
    full_name: Optional[str] = Field(None, min_length=2, max_length=100, description="User's full name")
    password: Optional[str] = Field(None, min_length=8, max_length=100, description="New password (min 8 characters)")
    role: Optional[UserRole] = Field(None, description="User's role")
    is_active: Optional[bool] = Field(None, description="Whether the user is active")

class UserInDB(UserBase):
    """User model for database operations."""
    id: int
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserResponse(UserBase):
    """User model for API responses."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    """Response model for listing users."""
    users: list[UserResponse]
    total: int
