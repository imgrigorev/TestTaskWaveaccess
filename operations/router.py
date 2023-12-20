from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.models import task
from operations.schemas import CreateTask

router = APIRouter(
    prefix="/operations",
    tags = ["operation"]
)

@router.get("/")
async def get_operations(session: AsyncSession = Depends(get_async_session)):
    query = select(task).where(task.c.id)
    return

@router.post("/set_task")
async def create_task(new_operation : CreateTask, session : AsyncSession = Depends(get_async_session) ):
    stmt = insert(task).values(new_operation.model_dump())
    await session.execute(stmt)
    await session.commit()

    return {"status" : "success"}
