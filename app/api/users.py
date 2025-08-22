from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.database import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserResponseSerialized
from app.schemas.common import UserActionRequest
from app.utils.responses import APIResponse
from app.utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/")
async def handle_user_action(request: UserActionRequest, db: Session = Depends(get_db)):
    """
    Handle user actions: create, edit, view
    All responses return either 200 (success/error) or 500 (server error)
    """
    try:
        action = request.action
        data = request.data or {}
        
        logger.info(f"Processing user action: {action}")
        
        if action == "create":
            return await create_user(data, db)
        elif action == "edit":
            return await edit_user(data, db)
        elif action == "view":
            return await view_user(data, db)
        else:
            return APIResponse.error(f"Invalid action: {action}")
            
    except Exception as e:
        logger.error(f"Error processing user action: {e}")
        return APIResponse.server_error("Failed to process user action")


async def create_user(data: Dict[str, Any], db: Session) -> APIResponse:
    """Create a new user."""
    try:
        # Validate required fields
        required_fields = ["username", "email", "full_name", "password"]
        for field in required_fields:
            if field not in data:
                return APIResponse.error(f"Missing required field: {field}")
        
        # Create user data object
        user_data = UserCreate(
            username=data["username"],
            email=data["email"],
            full_name=data["full_name"],
            password=data["password"],
            is_active=data.get("is_active", True)
        )
        
        # Create user
        user = UserService.create_user(db, user_data)
        
        # Return success response without datetime fields
        return APIResponse.success(
            data={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "is_active": user.is_active
            },
            message="User created successfully"
        )
        
    except ValueError as e:
        return APIResponse.error(str(e))
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return APIResponse.server_error("Failed to create user")


async def edit_user(data: Dict[str, Any], db: Session) -> APIResponse:
    """Edit an existing user."""
    try:
        # Validate required fields
        if "id" not in data:
            return APIResponse.error("Missing required field: id")
        
        user_id = data["id"]
        
        # Get existing user
        existing_user = UserService.get_user_by_id(db, user_id)
        if not existing_user:
            return APIResponse.error("User not found")
        
        # Prepare update data
        update_data = {}
        allowed_fields = ["username", "email", "full_name", "is_active"]
        
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
        
        if not update_data:
            return APIResponse.error("No valid fields to update")
        
        # Update user
        user_update = UserUpdate(**update_data)
        updated_user = UserService.update_user(db, user_id, user_update)
        
        # Return success response without datetime fields
        return APIResponse.success(
            data={
                "id": updated_user.id,
                "username": updated_user.username,
                "email": updated_user.email,
                "full_name": updated_user.full_name,
                "is_active": updated_user.is_active
            },
            message="User updated successfully"
        )
        
    except ValueError as e:
        return APIResponse.error(str(e))
    except Exception as e:
        logger.error(f"Error updating user: {e}")
        return APIResponse.server_error("Failed to update user")


async def view_user(data: Dict[str, Any], db: Session) -> APIResponse:
    """View user(s) based on criteria."""
    try:
        # Handle different view scenarios
        if "id" in data:
            # View specific user by ID
            user_id = data["id"]
            user = UserService.get_user_by_id(db, user_id)
            
            if not user:
                return APIResponse.error("User not found")
            
            return APIResponse.success(
                data={
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "full_name": user.full_name,
                    "is_active": user.is_active
                },
                message="User retrieved successfully"
            )
            
        elif "username" in data:
            # View user by username
            username = data["username"]
            user = UserService.get_user_by_username(db, username)
            
            if not user:
                return APIResponse.error("User not found")
            
            return APIResponse.success(
                data={
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "full_name": user.full_name,
                    "is_active": user.is_active
                },
                message="User retrieved successfully"
            )
            
        else:
            # View all users with pagination
            page = data.get("page", 1)
            size = data.get("size", 10)
            
            if page < 1:
                page = 1
            if size < 1 or size > 100:
                size = 10
            
            skip = (page - 1) * size
            users = UserService.get_users(db, skip=skip, limit=size)
            
            user_list = []
            for user in users:
                user_list.append({
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "full_name": user.full_name,
                    "is_active": user.is_active
                })
            
            return APIResponse.success(
                data={
                    "users": user_list,
                    "pagination": {
                        "page": page,
                        "size": size,
                        "total": len(user_list)
                    }
                },
                message="Users retrieved successfully"
            )
            
    except Exception as e:
        logger.error(f"Error viewing user: {e}")
        return APIResponse.server_error("Failed to retrieve user information")
