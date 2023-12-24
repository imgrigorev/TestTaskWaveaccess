from fastapi import APIRouter
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from database import get_async_session
from sqlalchemy import select, delete, update

from tasks.schemas import TaskBase, TaskCreate, TaskUpdate, TaskInDB

from models.models import Task

from auth.dependecies import CurrentUser
from auth.utils import get_user_by_id

import tasks.utils as utils

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@router.get("/")
async def get_all(current_user: CurrentUser, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Task))
    tasks = result.scalars().all()
    return {"tasks": tasks}


@router.post("/")
async def create_task(current_user: CurrentUser, task_create: TaskBase, session: AsyncSession = Depends(get_async_session)):
    if task_create.executor_id is not None and task_create.executor_id != 0 :
        executor = await get_user_by_id(session, task_create.executor_id)
        if executor is None:
            raise HTTPException(status_code=400, detail="Executor not found")
    try:
        task = Task(**task_create.dict())
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Error creating task: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating task: {str(e)}")


@router.get("/{task_id}", response_model=TaskUpdate)
async def read_task(current_user: CurrentUser, task_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().one()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskUpdate)
async def update_task(task_id: int, current_user: CurrentUser, task_update: TaskUpdate, session: AsyncSession = Depends(get_async_session)):
    if not task_update.dict():
        raise HTTPException(status_code=400, detail="No data provided for update")
    current_task_status = await utils.get_task_by_id(session, task_id)
    if current_task_status is None:
        raise HTTPException(status_code=404, detail="Task not found")
    executor = None
    if task_update.executor_id is not None and task_update.executor_id != 0:
        executor = await get_user_by_id(session, task_update.executor_id)
        if executor is None:
            raise HTTPException(status_code=400, detail="Executor not found")
    try:
        task_update.check_status_transition(current_task_status, task_update.status)
        if executor is not None:
            task_update.check_executor_constraints(executor.role)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    update_query = update(Task).where(Task.id == task_id).values(**task_update.dict())
    await session.execute(update_query)
    await session.commit()

    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().one()
    return task

@router.delete("/{task_id}")
async def delete_task(task_id: int, current_user: CurrentUser, session: AsyncSession = Depends(get_async_session)):
    if current_user.role.lower() != "manager":
        raise HTTPException(status_code=403, detail="Permission denied. Only manager can delete tasks.")
    task = await utils.get_task_by_id(session, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await session.execute(delete(Task).where(Task.id == id))
    await session.commit()
    task = {"message": "Task deleted successfully"}
    return task
