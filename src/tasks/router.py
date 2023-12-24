from fastapi import APIRouter
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from database import get_async_session
from sqlalchemy import select, delete, update

from tasks.schemas import TaskBase, TaskCreate, TaskUpdate, TaskInDB

from models.models import Task

from auth.dependecies import CurrentUser

import tasks.utils as utils

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@router.get("/")
async def get_all(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Task))
    tasks = result.scalars().all()
    return {"tasks": tasks}


@router.post("/", response_model=TaskBase)
async def create_task(task_create: TaskBase, session: AsyncSession = Depends(get_async_session)):
    try:
        tasks = Task(**task_create.dict())
        session.add(tasks)
        await session.commit()
        await session.refresh(tasks)
        return tasks
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Error creating task: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating task: {str(e)}")


@router.get("/{task_id}", response_model=TaskInDB)
async def read_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().one()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}")
async def update_task(task_id: int, task_update: TaskUpdate, session: AsyncSession = Depends(get_async_session)):
    if not task_update.dict():
        raise HTTPException(status_code=400, detail="No data provided for update")

    task = await utils.get_task_by_id(session, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        task_update.check_status_transition(task.status, task_update.status)
        task_update.check_executor_constraints()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = await session.execute(update(Task).where(Task.id == task_id).values(**task_update.dict()))
    await session.commit()

    return {"message": result}



@router.delete("/{task_id}", response_model=TaskInDB)
async def delete_task(task_id: int, current_user: CurrentUser, session: AsyncSession = Depends(get_async_session)):
    if current_user.role.lower() != "manager":
        raise HTTPException(status_code=403, detail="Permission denied. Only manager can delete tasks.")
    task = await utils.get_task_by_id(session, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await session.execute(delete(Task).where(Task.id == id))
    await session.commit()
    return task
