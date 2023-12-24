from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, field_validator


class UserRole(str, Enum):
    developer = "developer"
    manager = "manager"
    test_engineer = "test engineer"
    team_lead = "team lead"

class TaskType(str, Enum):
    bug = "bug"
    task = "task"

class TaskPriority(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"

class TaskStatus(str, Enum):
    Todo = "todo"
    InProgress = "inprogress"
    CodeReview = "codereview"
    DevTest = "devtest"
    Testing = "testing"
    Done = "done"
    WontFix = "wontfix"


class TaskBase(BaseModel):
    # id: int
    type: TaskType
    priority: TaskPriority
    status: TaskStatus
    title: str = None
    description: str = None
    executor_id: int = None
    creator: str = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = False


class TaskCreate(BaseModel):
    pass

class TaskUpdate(BaseModel):
    type: Optional[TaskType] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    title: Optional[str] = None
    description: Optional[str] = None
    executor_id: Optional[int] = None
    creator: Optional[str] = None
    created_at: datetime = None
    updated_at: datetime = None

    def check_status_transition(self, current_status: str, new_status: str):
        allowed_transitions = {
            TaskStatus.Todo: {TaskStatus.Todo, TaskStatus.InProgress, TaskStatus.WontFix},
            TaskStatus.InProgress: {TaskStatus.InProgress, TaskStatus.Todo, TaskStatus.CodeReview, TaskStatus.WontFix},
            TaskStatus.CodeReview: {TaskStatus.CodeReview, TaskStatus.DevTest, TaskStatus.Todo, TaskStatus.WontFix},
            TaskStatus.DevTest: {TaskStatus.DevTest, TaskStatus.Testing, TaskStatus.Todo, TaskStatus.WontFix},
            TaskStatus.Testing: {TaskStatus.Testing, TaskStatus.Done, TaskStatus.Todo, TaskStatus.WontFix},
            TaskStatus.Done: {TaskStatus.Done, TaskStatus.Todo, TaskStatus.WontFix},
            TaskStatus.WontFix: {TaskStatus.WontFix, TaskStatus.Todo},
        }

        if current_status not in allowed_transitions:
            raise ValueError(f"Invalid current status: {current_status}")

        if new_status not in allowed_transitions[current_status]:
            raise ValueError(f"Invalid status transition: {current_status} to {new_status}")

    def check_executor_constraints(self, executor_role):
        if executor_role == "manager":
            raise ValueError("Manager cannot be assigned as an executor.")

        if not self.executor_id and self.status != TaskStatus.InProgress:
            return

        if self.status in {TaskStatus.InProgress, TaskStatus.CodeReview,
                           TaskStatus.DevTest} and executor_role == "test engineer":
            raise ValueError(f"{self.status} cannot have Test Engineer as an executor.")

        if self.status == TaskStatus.Testing and executor_role == "developer":
            raise ValueError("Testing cannot have Developer as an executor.")

class TaskInDB(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
