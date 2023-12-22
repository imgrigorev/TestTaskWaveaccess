from fastapi import APIRouter
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session

from datetime import datetime
from src.tasks.schemas import TaskBase, TaskCreate, TaskUpdate, TaskInDB

router = APIRouter(
    prefix="/tasks",
    tags = ["tasks"]
)


@router.post("/tasks/", response_model=TaskInDB)
def create_task(task_create: TaskCreate, session : AsyncSession = Depends(get_async_session)):
    db_task = TaskBase(**task_create.dict(), created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.get("/tasks/{task_id}", response_model=TaskInDB)
def read_task(task_id: int, session : AsyncSession = Depends(get_async_session)):
    task = session.query(TaskBase).filter(TaskBase.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=TaskInDB)
def update_task(task_id: int, task_update: TaskUpdate, session : AsyncSession = Depends(get_async_session)):
    db_task = session.query(TaskBase).filter(TaskBase.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in task_update.dict().items():
        setattr(db_task, field, value)

    db_task.updated_at = datetime.utcnow()
    session.commit()
    session.refresh(db_task)
    return db_task

@router.delete("/tasks/{task_id}", response_model=TaskInDB)
def delete_task(task_id: int, session : AsyncSession = Depends(get_async_session)):
    task = session.query(TaskBase).filter(TaskBase.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return task
