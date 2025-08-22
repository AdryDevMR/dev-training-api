from sqlalchemy import Boolean, Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from .base import Base, BaseModel
import enum

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base, BaseModel):
    """User model for storing user related details."""
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean(), default=True, nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    created_tasks = "Task"
    assigned_tasks = "Task"
    
    @property
    def is_superuser(self) -> bool:
        """Check if user is an admin."""
        return self.role == UserRole.ADMIN
    
    def __repr__(self) -> str:
        return f"<User {self.email}>"
    
    def to_dict(self):
        """Convert user to dictionary."""
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "role": self.role.value,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
