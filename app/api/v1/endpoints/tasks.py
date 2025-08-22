from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.task import Task as DBTask
from app.models.user import User as DBUser
from app.schemas.tasks import (
    TaskCreate, 
    TaskUpdate, 
    TaskResponse, 
    TaskListResponse,
    TaskStatus,
    ActionType,
    BaseRequest
)
from app.api.v1.schemas.base import SuccessResponse, ErrorResponse

router = APIRouter()

def get_task(db: Session, task_id: int):
    return db.query(DBTask).filter(DBTask.id == task_id).first()

def get_tasks(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    assignee_id: Optional[int] = None,
    status: Optional[TaskStatus] = None,
    created_by_id: Optional[int] = None
):
    query = db.query(DBTask)
    
    if assignee_id is not None:
        query = query.filter(DBTask.assignee_id == assignee_id)
    
    if status is not None:
        query = query.filter(DBTask.status == status)
        
    if created_by_id is not None:
        query = query.filter(DBTask.created_by_id == created_by_id)
    
    return query.offset(skip).limit(limit).all()

def create_task(db: Session, task: TaskCreate, created_by_id: int):
    db_task = DBTask(
        **task.dict(exclude={"assignee_id"}),
        created_by_id=created_by_id,
        assignee_id=task.assignee_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, db_task: DBTask, task_update: TaskUpdate) -> DBTask:
    update_data = task_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.post("/", response_model=SuccessResponse, responses={
    200: {"model": SuccessResponse},
    500: {"model": ErrorResponse}
})
async def handle_task_request(
    request: Dict[str, Any],
    current_user: DBUser = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        # Validate base request
        base_request = BaseRequest(**request)
        
        if base_request.action == ActionType.CREATE:
            task_create = TaskCreate(**request)
            task = create_task(db=db, task=task_create, created_by_id=current_user.id)
            return SuccessResponse(
                success=True,
                data=TaskResponse.from_orm(task).dict()
            )
            
        elif base_request.action == ActionType.EDIT:
            if "id" not in request:
                return SuccessResponse(
                    success=False,
                    data={"reason": "Task ID is required for editing"}
                )
            
            task_id = request["id"]
            db_task = get_task(db, task_id=task_id)
            if not db_task:
                return SuccessResponse(
                    success=False,
                    data={"reason": "Task not found"}
                )
            
            # Only allow task creator or assignee to edit
            if db_task.created_by_id != current_user.id and db_task.assignee_id != current_user.id:
                return SuccessResponse(
                    success=False,
                    data={"reason": "Not authorized to edit this task"}
                )
            
            task_update = TaskUpdate(**request)
            task = update_task(db=db, db_task=db_task, task_update=task_update)
            return SuccessResponse(
                success=True,
                data=TaskResponse.from_orm(task).dict()
            )
            
        elif base_request.action == ActionType.VIEW:
            if "id" in request:
                # View single task
                task_id = request["id"]
                db_task = get_task(db, task_id=task_id)
                if not db_task:
                    return SuccessResponse(
                        success=False,
                        data={"reason": "Task not found"}
                    )
                
                # Only allow task creator, assignee, or admins to view
                if not (db_task.created_by_id == current_user.id or 
                       db_task.assignee_id == current_user.id or 
                       current_user.is_superuser):
                    return SuccessResponse(
                        success=False,
                        data={"reason": "Not authorized to view this task"}
                    )
                
                return SuccessResponse(
                    success=True,
                    data=TaskResponse.from_orm(db_task).dict()
                )
            else:
                # List tasks
                skip = request.get("skip", 0)
                limit = min(100, request.get("limit", 100))
                assignee_id = request.get("assignee_id")
                status = request.get("status")
                
                # Non-admins can only see their own tasks or tasks assigned to them
                if not current_user.is_superuser:
                    created_by_id = current_user.id
                else:
                    created_by_id = request.get("created_by_id")
                
                tasks = get_tasks(
                    db, 
                    skip=skip, 
                    limit=limit,
                    assignee_id=assignee_id,
                    status=status,
                    created_by_id=created_by_id
                )
                
                # Get total count for pagination
                query = db.query(DBTask)
                if not current_user.is_superuser:
                    query = query.filter(
                        (DBTask.created_by_id == current_user.id) | 
                        (DBTask.assignee_id == current_user.id)
                    )
                total = query.count()
                
                return SuccessResponse(
                    success=True,
                    data={
                        "tasks": [TaskResponse.from_orm(task).dict() for task in tasks],
                        "total": total,
                        "skip": skip,
                        "limit": limit
                    }
                )
    
    except Exception as e:
        # Log the error and return a generic error message
        import logging
        logging.exception("Error processing task request")
        return SuccessResponse(
            success=False,
            data={"reason": "An error occurred while processing your request"}
        )
