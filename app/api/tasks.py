from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime
from app.database import get_db
from app.services.task_service import TaskService
from app.services.user_service import UserService
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.schemas.common import TaskActionRequest
from app.models.task import TaskStatus, TaskPriority
from app.utils.responses import APIResponse
from app.utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/")
async def handle_task_action(request: TaskActionRequest, db: Session = Depends(get_db)):
    """
    Handle task actions: create, edit, view
    All responses return either 200 (success/error) or 500 (server error)
    """
    try:
        action = request.action
        data = request.data or {}
        
        logger.info(f"Processing task action: {action}")
        
        if action == "create":
            return await create_task(data, db)
        elif action == "edit":
            return await edit_task(data, db)
        elif action == "view":
            return await view_task(data, db)
        else:
            return APIResponse.error(f"Invalid action: {action}")
            
    except Exception as e:
        logger.error(f"Error processing task action: {e}")
        return APIResponse.server_error("Failed to process task action")


async def create_task(data: Dict[str, Any], db: Session) -> APIResponse:
    """Create a new task."""
    try:
        # Validate required fields
        required_fields = ["title", "owner_id"]
        for field in required_fields:
            if field not in data:
                return APIResponse.error(f"Missing required field: {field}")
        
        # Validate owner exists
        owner = UserService.get_user_by_id(db, data["owner_id"])
        if not owner:
            return APIResponse.error("Owner user not found")
        
        # Prepare task data
        task_data = TaskCreate(
            title=data["title"],
            description=data.get("description"),
            status=data.get("status", TaskStatus.PENDING),
            priority=data.get("priority", TaskPriority.MEDIUM),
            due_date=data.get("due_date"),
            owner_id=data["owner_id"]
        )
        
        # Validate status and priority
        if task_data.status not in TaskStatus:
            return APIResponse.error(f"Invalid status: {task_data.status}")
        if task_data.priority not in TaskPriority:
            return APIResponse.error(f"Invalid priority: {task_data.priority}")
        
        # Create task
        task = TaskService.create_task(db, task_data)
        
        # Return success response
        return APIResponse.success(
            data={
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "due_date": task.due_date,
                "owner_id": task.owner_id,
                "created_at": task.created_at
            },
            message="Task created successfully"
        )
        
    except ValueError as e:
        return APIResponse.error(str(e))
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return APIResponse.server_error("Failed to create task")


async def edit_task(data: Dict[str, Any], db: Session) -> APIResponse:
    """Edit an existing task."""
    try:
        # Validate required fields
        if "id" not in data:
            return APIResponse.error("Missing required field: id")
        
        task_id = data["id"]
        
        # Get existing task
        existing_task = TaskService.get_task_by_id(db, task_id)
        if not existing_task:
            return APIResponse.error("Task not found")
        
        # Prepare update data
        update_data = {}
        allowed_fields = ["title", "description", "status", "priority", "due_date"]
        
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
        
        if not update_data:
            return APIResponse.error("No valid fields to update")
        
        # Validate status and priority if provided
        if "status" in update_data and update_data["status"] not in TaskStatus:
            return APIResponse.error(f"Invalid status: {update_data['status']}")
        if "priority" in update_data and update_data["priority"] not in TaskPriority:
            return APIResponse.error(f"Invalid priority: {update_data['priority']}")
        
        # Update task
        task_update = TaskUpdate(**update_data)
        updated_task = TaskService.update_task(db, task_id, task_update)
        
        # Return success response
        return APIResponse.success(
            data={
                "id": updated_task.id,
                "title": updated_task.title,
                "description": updated_task.description,
                "status": updated_task.status,
                "priority": updated_task.priority,
                "due_date": updated_task.due_date,
                "completed_at": updated_task.completed_at,
                "updated_at": updated_task.updated_at
            },
            message="Task updated successfully"
        )
        
    except ValueError as e:
        return APIResponse.error(str(e))
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        return APIResponse.server_error("Failed to update task")


async def view_task(data: Dict[str, Any], db: Session) -> APIResponse:
    """View task(s) based on criteria."""
    try:
        # Handle different view scenarios
        if "id" in data:
            # View specific task by ID
            task_id = data["id"]
            include_owner = data.get("include_owner", False)
            
            if include_owner:
                task = TaskService.get_task_with_owner(db, task_id)
                if not task:
                    return APIResponse.error("Task not found")
                
                return APIResponse.success(
                    data=task,
                    message="Task retrieved successfully"
                )
            else:
                task = TaskService.get_task_by_id(db, task_id)
                if not task:
                    return APIResponse.error("Task not found")
                
                return APIResponse.success(
                    data={
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "status": task.status,
                        "priority": task.priority,
                        "due_date": task.due_date,
                        "completed_at": task.completed_at,
                        "owner_id": task.owner_id,
                        "created_at": task.created_at,
                        "updated_at": task.updated_at
                    },
                    message="Task retrieved successfully"
                )
                
        elif "owner_id" in data:
            # View tasks by owner
            owner_id = data["owner_id"]
            page = data.get("page", 1)
            size = data.get("size", 10)
            
            if page < 1:
                page = 1
            if size < 1 or size > 100:
                size = 10
            
            skip = (page - 1) * size
            tasks = TaskService.get_tasks_by_owner(db, owner_id, skip=skip, limit=size)
            
            task_list = []
            for task in tasks:
                task_list.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "priority": task.priority,
                    "due_date": task.due_date,
                    "completed_at": task.completed_at,
                    "created_at": task.created_at
                })
            
            return APIResponse.success(
                data={
                    "tasks": task_list,
                    "pagination": {
                        "page": page,
                        "size": size,
                        "total": len(task_list)
                    }
                },
                message="Tasks retrieved successfully"
            )
            
        elif "status" in data:
            # View tasks by status
            status = data["status"]
            if status not in TaskStatus:
                return APIResponse.error(f"Invalid status: {status}")
            
            page = data.get("page", 1)
            size = data.get("size", 10)
            
            if page < 1:
                page = 1
            if size < 1 or size > 100:
                size = 10
            
            skip = (page - 1) * size
            tasks = TaskService.get_tasks_by_status(db, status, skip=skip, limit=size)
            
            task_list = []
            for task in tasks:
                task_list.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "priority": task.priority,
                    "due_date": task.due_date,
                    "owner_id": task.owner_id,
                    "created_at": task.created_at
                })
            
            return APIResponse.success(
                data={
                    "tasks": task_list,
                    "pagination": {
                        "page": page,
                        "size": size,
                        "total": len(task_list)
                    }
                },
                message="Tasks retrieved successfully"
            )
            
        elif "search" in data:
            # Search tasks
            search_term = data["search"]
            page = data.get("page", 1)
            size = data.get("size", 10)
            
            if page < 1:
                page = 1
            if size < 1 or size > 100:
                size = 10
            
            skip = (page - 1) * size
            tasks = TaskService.search_tasks(db, search_term, skip=skip, limit=size)
            
            task_list = []
            for task in tasks:
                task_list.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "priority": task.priority,
                    "due_date": task.due_date,
                    "owner_id": task.owner_id,
                    "created_at": task.created_at
                })
            
            return APIResponse.success(
                data={
                    "tasks": task_list,
                    "pagination": {
                        "page": page,
                        "size": size,
                        "total": len(task_list)
                    }
                },
                message="Tasks retrieved successfully"
            )
            
        else:
            # View all tasks with pagination
            page = data.get("page", 1)
            size = data.get("size", 10)
            
            if page < 1:
                page = 1
            if size < 1 or size > 100:
                size = 10
            
            skip = (page - 1) * size
            tasks = TaskService.get_all_tasks(db, skip=skip, limit=size)
            
            task_list = []
            for task in tasks:
                task_list.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "priority": task.priority,
                    "due_date": task.due_date,
                    "owner_id": task.owner_id,
                    "created_at": task.created_at
                })
            
            return APIResponse.success(
                data={
                    "tasks": task_list,
                    "pagination": {
                        "page": page,
                        "size": size,
                        "total": len(task_list)
                    }
                },
                message="Tasks retrieved successfully"
            )
            
    except Exception as e:
        logger.error(f"Error viewing task: {e}")
        return APIResponse.server_error("Failed to retrieve task information")
