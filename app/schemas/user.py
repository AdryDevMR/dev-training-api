from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, computed_field


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr = Field(..., description="Valid email address")
    full_name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    is_active: bool = Field(default=True, description="Whether the user account is active")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Unique username")
    email: Optional[EmailStr] = Field(None, description="Valid email address")
    full_name: Optional[str] = Field(None, min_length=1, max_length=100, description="User's full name")
    password: Optional[str] = Field(None, min_length=8, description="User password (min 8 characters)")
    is_active: Optional[bool] = Field(None, description="Whether the user account is active")


class UserResponse(UserBase):
    id: int = Field(..., description="Unique user ID")
    created_at: datetime = Field(..., description="User creation timestamp")
    updated_at: datetime = Field(..., description="User last update timestamp")
    
    class Config:
        from_attributes = True


class UserResponseSerialized(BaseModel):
    """Serialized user response with ISO format dates."""
    id: int = Field(..., description="Unique user ID")
    username: str = Field(..., description="Unique username")
    email: str = Field(..., description="Valid email address")
    full_name: str = Field(..., description="User's full name")
    is_active: bool = Field(..., description="Whether the user account is active")
    created_at: str = Field(..., description="User creation timestamp in ISO format")
    updated_at: Optional[str] = Field(None, description="User last update timestamp in ISO format")
    
    @classmethod
    def from_user(cls, user: UserResponse):
        """Create a serialized response from a user model."""
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at.isoformat() if user.created_at else None,
            updated_at=user.updated_at.isoformat() if user.updated_at else None
        )


class UserInDB(UserResponse):
    hashed_password: str = Field(..., description="Hashed password")


class UserActionRequest(BaseModel):
    action: str = Field(..., description="Action to perform: create, edit, or view")
    data: Optional[dict] = Field(None, description="Data for the action")
