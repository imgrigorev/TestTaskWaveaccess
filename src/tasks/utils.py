from datetime import datetime, timedelta

from sqlalchemy import select, update
from sqlalchemy.orm import joinedload

from models.models import Task

from tasks.schemas import TaskCreate, TaskUpdate, TaskInDB, TaskBase

async def create_task(session, task: TaskCreate) -> TaskInDB:
    db_task = TaskBase(**task.dict(),
                       created_at=datetime.utcnow(),
                       updated_at=datetime.utcnow())
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task


async def get_task_by_id(session, id : int) :
    db_task = await session.execute(select(Task).where(Task.id == id))
    return db_task.scalars().one()


