from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from datetime import datetime
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.utils.logging import get_logger

logger = get_logger(__name__)


class TaskService:
    """Service class for task-related operations."""
    
    @staticmethod
    def create_task(db: Session, task_data: TaskCreate) -> Task:
        """Create a new task."""
        try:
            # Verify that the owner exists
            owner = db.query(User).filter(User.id == task_data.owner_id).first()
            if not owner:
                raise ValueError("User not found")
            
            # Create task object
            db_task = Task(
                title=task_data.title,
                description=task_data.description,
                status=task_data.status,
                priority=task_data.priority,
                due_date=task_data.due_date,
                owner_id=task_data.owner_id
            )
            
            db.add(db_task)
            db.commit()
            db.refresh(db_task)
            
            logger.info(f"Task created successfully: {task_data.title} for user {task_data.owner_id}")
            return db_task
            
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Database integrity error creating task: {e}")
            raise ValueError("Task creation failed due to database constraint")
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating task: {e}")
            raise
    
    @staticmethod
    def get_task_by_id(db: Session, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if not task:
                logger.warning(f"Task not found with ID: {task_id}")
            return task
        except Exception as e:
            logger.error(f"Error getting task by ID {task_id}: {e}")
            raise
    
    @staticmethod
    def get_tasks_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get tasks for a specific owner."""
        try:
            tasks = db.query(Task).filter(Task.owner_id == owner_id).offset(skip).limit(limit).all()
            return tasks
        except Exception as e:
            logger.error(f"Error getting tasks for owner {owner_id}: {e}")
            raise
    
    @staticmethod
    def get_all_tasks(db: Session, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get all tasks with pagination."""
        try:
            tasks = db.query(Task).offset(skip).limit(limit).all()
            return tasks
        except Exception as e:
            logger.error(f"Error getting all tasks: {e}")
            raise
    
    @staticmethod
    def get_tasks_by_status(db: Session, status: TaskStatus, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get tasks by status."""
        try:
            tasks = db.query(Task).filter(Task.status == status).offset(skip).limit(limit).all()
            return tasks
        except Exception as e:
            logger.error(f"Error getting tasks by status {status}: {e}")
            raise
    
    @staticmethod
    def get_tasks_by_priority(db: Session, priority: TaskPriority, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get tasks by priority."""
        try:
            tasks = db.query(Task).filter(Task.priority == priority).offset(skip).limit(limit).all()
            return tasks
        except Exception as e:
            logger.error(f"Error getting tasks by priority {priority}: {e}")
            raise
    
    @staticmethod
    def search_tasks(db: Session, search_term: str, skip: int = 0, limit: int = 100) -> List[Task]:
        """Search tasks by title or description."""
        try:
            tasks = db.query(Task).filter(
                (Task.title.contains(search_term)) | 
                (Task.description.contains(search_term))
            ).offset(skip).limit(limit).all()
            return tasks
        except Exception as e:
            logger.error(f"Error searching tasks with term '{search_term}': {e}")
            raise
    
    @staticmethod
    def update_task(db: Session, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        """Update a task."""
        try:
            task = TaskService.get_task_by_id(db, task_id)
            if not task:
                raise ValueError("Task not found")
            
            # Update fields
            update_data = task_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(task, field, value)
            
            # If status is being updated to completed, set completed_at
            if task_data.status == TaskStatus.COMPLETED and task.status != TaskStatus.COMPLETED:
                task.completed_at = datetime.utcnow()
            
            # If status is being updated from completed to something else, clear completed_at
            elif task_data.status and task_data.status != TaskStatus.COMPLETED and task.status == TaskStatus.COMPLETED:
                task.completed_at = None
            
            db.commit()
            db.refresh(task)
            
            logger.info(f"Task updated successfully: {task.title}")
            return task
            
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Database integrity error updating task: {e}")
            raise ValueError("Task update failed due to database constraint")
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating task {task_id}: {e}")
            raise
    
    @staticmethod
    def delete_task(db: Session, task_id: int) -> bool:
        """Delete a task."""
        try:
            task = TaskService.get_task_by_id(db, task_id)
            if not task:
                raise ValueError("Task not found")
            
            db.delete(task)
            db.commit()
            
            logger.info(f"Task deleted successfully: {task.title}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting task {task_id}: {e}")
            raise
    
    @staticmethod
    def get_task_with_owner(db: Session, task_id: int) -> Optional[dict]:
        """Get a task with owner information."""
        try:
            task = db.query(Task).join(User).filter(Task.id == task_id).first()
            if not task:
                return None
            
            # Convert to dict with owner info
            task_dict = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "due_date": task.due_date,
                "completed_at": task.completed_at,
                "created_at": task.created_at,
                "updated_at": task.updated_at,
                "owner": {
                    "id": task.owner.id,
                    "username": task.owner.username,
                    "full_name": task.owner.full_name,
                    "email": task.owner.email
                }
            }
            
            return task_dict
            
        except Exception as e:
            logger.error(f"Error getting task with owner {task_id}: {e}")
            raise
    
    @staticmethod
    def get_overdue_tasks(db: Session, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get overdue tasks (due date has passed and not completed)."""
        try:
            current_time = datetime.utcnow()
            overdue_tasks = db.query(Task).filter(
                Task.due_date < current_time,
                Task.status != TaskStatus.COMPLETED
            ).offset(skip).limit(limit).all()
            
            return overdue_tasks
            
        except Exception as e:
            logger.error(f"Error getting overdue tasks: {e}")
            raise
