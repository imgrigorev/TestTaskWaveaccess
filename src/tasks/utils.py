from datetime import datetime, timedelta

from sqlalchemy import select, update
from fastapi import HTTPException
from models.models import Task

from tasks.schemas import TaskCreate, TaskUpdate, TaskInDB, TaskBase
from auth.utils import get_user_by_id


async def create_task(session, task: TaskCreate) -> TaskInDB:
    db_task = TaskBase(**task.dict(),
                       created_at=datetime.utcnow(),
                       updated_at=datetime.utcnow())
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task


async def get_task_by_id(session, id: int):
    stmt = select(Task).where(Task.id == id)
    result = await session.execute(stmt)
    task = result.scalars().first()

    return task.status



