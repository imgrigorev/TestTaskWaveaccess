from datetime import datetime

from pydantic import BaseModel


class CreateTask(BaseModel):
    number: int
    username: str
    priority: str
    status: str
    title: str
    description: str
    executor: str
    creator: str
    created_at: datetime
    updated_at: datetime
    type: str
    blocking_tasks: str
