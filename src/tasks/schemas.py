from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# class CreateTask(BaseModel):
#     number: int
#     username: str
#     priority: str
#     status: str
#     title: str
#     description: str
#     executor: str
#     creator: str
#     created_at: datetime
#     updated_at: datetime
#     type: str
#     blocking_tasks: str

class TaskBase(BaseModel):
    type: str
    priority: Optional[str] = None
    status: str
    title: Optional[str] = None
    description: Optional[str] = None
    executor: Optional[int] = None
    creator: str

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskInDB(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
