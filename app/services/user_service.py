from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from passlib.context import CryptContext
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.utils.logging import get_logger

logger = get_logger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """Service class for user-related operations."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user."""
        try:
            # Check if username or email already exists
            existing_user = db.query(User).filter(
                (User.username == user_data.username) | 
                (User.email == user_data.email)
            ).first()
            
            if existing_user:
                if existing_user.username == user_data.username:
                    raise ValueError("Username already exists")
                else:
                    raise ValueError("Email already exists")
            
            # Hash the password
            hashed_password = UserService.hash_password(user_data.password)
            
            # Create user object
            db_user = User(
                username=user_data.username,
                email=user_data.email,
                full_name=user_data.full_name,
                hashed_password=hashed_password,
                is_active=user_data.is_active,
                is_admin=user_data.is_admin
            )
            
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            
            logger.info(f"User created successfully: {user_data.username}")
            return db_user
            
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Database integrity error creating user: {e}")
            raise ValueError("User creation failed due to database constraint")
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating user: {e}")
            raise
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                logger.warning(f"User not found with ID: {user_id}")
            return user
        except Exception as e:
            logger.error(f"Error getting user by ID {user_id}: {e}")
            raise
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get a user by username."""
        try:
            user = db.query(User).filter(User.username == username).first()
            return user
        except Exception as e:
            logger.error(f"Error getting user by username {username}: {e}")
            raise
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get a user by email."""
        try:
            user = db.query(User).filter(User.email == email).first()
            return user
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            raise
    
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get a list of users with pagination."""
        try:
            users = db.query(User).offset(skip).limit(limit).all()
            return users
        except Exception as e:
            logger.error(f"Error getting users: {e}")
            raise
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update a user."""
        try:
            user = UserService.get_user_by_id(db, user_id)
            if not user:
                raise ValueError("User not found")
            
            # Check for unique constraints if updating username or email
            if user_data.username and user_data.username != user.username:
                existing_user = UserService.get_user_by_username(db, user_data.username)
                if existing_user:
                    raise ValueError("Username already exists")
            
            if user_data.email and user_data.email != user.email:
                existing_user = UserService.get_user_by_email(db, user_data.email)
                if existing_user:
                    raise ValueError("Email already exists")
            
            # Update fields
            update_data = user_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(user, field, value)
            
            db.commit()
            db.refresh(user)
            
            logger.info(f"User updated successfully: {user.username}")
            return user
            
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Database integrity error updating user: {e}")
            raise ValueError("User update failed due to database constraint")
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating user {user_id}: {e}")
            raise
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete a user."""
        try:
            user = UserService.get_user_by_id(db, user_id)
            if not user:
                raise ValueError("User not found")
            
            db.delete(user)
            db.commit()
            
            logger.info(f"User deleted successfully: {user.username}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting user {user_id}: {e}")
            raise
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """Authenticate a user with username and password."""
        try:
            user = UserService.get_user_by_username(db, username)
            if not user:
                return None
            
            if not UserService.verify_password(password, user.hashed_password):
                return None
            
            if not user.is_active:
                return None
            
            logger.info(f"User authenticated successfully: {username}")
            return user
            
        except Exception as e:
            logger.error(f"Error authenticating user {username}: {e}")
            raise
