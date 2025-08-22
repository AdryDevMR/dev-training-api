from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user, get_password_hash
from app.models.user import User as DBUser
from app.schemas.users import (
    UserCreate, 
    UserUpdate, 
    UserResponse, 
    UserListResponse,
    ActionType,
    BaseRequest
)
from app.api.v1.schemas.base import SuccessResponse, ErrorResponse

router = APIRouter()

def get_user(db: Session, user_id: int):
    return db.query(DBUser).filter(DBUser.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(DBUser).filter(DBUser.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBUser).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = DBUser(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: DBUser, user_update: UserUpdate) -> DBUser:
    update_data = user_update.dict(exclude_unset=True)
    
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/", response_model=SuccessResponse, responses={
    200: {"model": SuccessResponse},
    500: {"model": ErrorResponse}
})
async def handle_user_request(
    request: Dict[str, Any],
    current_user: DBUser = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        # Validate base request
        base_request = BaseRequest(**request)
        
        if base_request.action == ActionType.CREATE:
            if not current_user.is_superuser:
                return SuccessResponse(
                    success=False,
                    data={"reason": "Not authorized to create users"}
                )
            
            user_create = UserCreate(**request)
            db_user = get_user_by_email(db, email=user_create.email)
            if db_user:
                return SuccessResponse(
                    success=False,
                    data={"reason": "Email already registered"}
                )
            
            user = create_user(db=db, user=user_create)
            return SuccessResponse(
                success=True,
                data=UserResponse.from_orm(user).dict()
            )
            
        elif base_request.action == ActionType.EDIT:
            if "id" not in request:
                return SuccessResponse(
                    success=False,
                    data={"reason": "User ID is required for editing"}
                )
            
            user_id = request["id"]
            db_user = get_user(db, user_id=user_id)
            if not db_user:
                return SuccessResponse(
                    success=False,
                    data={"reason": "User not found"}
                )
            
            # Only allow users to edit their own profile or admins
            if db_user.id != current_user.id and not current_user.is_superuser:
                return SuccessResponse(
                    success=False,
                    data={"reason": "Not authorized to edit this user"}
                )
            
            user_update = UserUpdate(**request)
            user = update_user(db=db, db_user=db_user, user_update=user_update)
            return SuccessResponse(
                success=True,
                data=UserResponse.from_orm(user).dict()
            )
            
        elif base_request.action == ActionType.VIEW:
            if "id" in request:
                # View single user
                user_id = request["id"]
                db_user = get_user(db, user_id=user_id)
                if not db_user:
                    return SuccessResponse(
                        success=False,
                        data={"reason": "User not found"}
                    )
                
                # Only allow users to view their own profile or admins
                if db_user.id != current_user.id and not current_user.is_superuser:
                    return SuccessResponse(
                        success=False,
                        data={"reason": "Not authorized to view this user"}
                    )
                
                return SuccessResponse(
                    success=True,
                    data=UserResponse.from_orm(db_user).dict()
                )
            else:
                # List users (only for admins)
                if not current_user.is_superuser:
                    return SuccessResponse(
                        success=False,
                        data={"reason": "Not authorized to list users"}
                    )
                
                skip = request.get("skip", 0)
                limit = min(100, request.get("limit", 100))
                users = get_users(db, skip=skip, limit=limit)
                total = db.query(DBUser).count()
                
                return SuccessResponse(
                    success=True,
                    data={
                        "users": [UserResponse.from_orm(user).dict() for user in users],
                        "total": total,
                        "skip": skip,
                        "limit": limit
                    }
                )
    
    except Exception as e:
        # Log the error and return a generic error message
        import logging
        logging.exception("Error processing user request")
        return SuccessResponse(
            success=False,
            data={"reason": "An error occurred while processing your request"}
        )
