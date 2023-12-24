from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, UUID4, field_validator
from pydantic.types import constr



class UserRole(str, Enum):
    developer = "developer"
    manager = "manager"
    test_engineer = "test engineer"
    team_lead = "team lead"

class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: UserRole


class TokenBase(BaseModel):
    """Return response data"""

    token: UUID4 = Field(..., alias="access_token")
    expires: datetime
    token_type: Optional[str] = "bearer"

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    @field_validator("token")
    def hexlify_token(cls, value):
        """Convert UUID to pure hex string"""
        return value.hex


class UserCreate(UserBase):
    password: constr(strip_whitespace=True, min_length=8)


class Login(BaseModel):
    email: EmailStr
    password: constr(strip_whitespace=True, min_length=8)


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    token: (TokenBase | None) = None


class UserUpdateRole(BaseModel):
    id: int
    new_role: str
class UserUpdateLogin(BaseModel):
    id: int
    new_email: EmailStr



class UpdateResult(BaseModel):
    success: bool
    message: str
    updated_user: Optional[User] = None

class UserChangePassword(Login):
    new_password: constr(strip_whitespace=True, min_length=8)