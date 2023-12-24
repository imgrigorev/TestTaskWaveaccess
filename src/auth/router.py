from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from auth.dependecies import CurrentUser
from database import get_async_session
import auth.utils as utils
from auth.schemas import Login, User, UserCreate, UserUpdateRole, UserUpdateLogin, UserChangePassword


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/change_password/")
async def change_password(user: UserChangePassword, session : AsyncSession = Depends(get_async_session)):
    user_db = await utils.get_user_by_email(session, email=user.email)
    if not user_db:
        raise HTTPException(status_code=400, detail="User not found")
    if user_db.password != user.password:
        raise HTTPException(status_code=400, detail="Wrong password")
    result = await utils.change_password(session, user)
    return result


@router.post("/sign-up/")
async def create_user(user: UserCreate, session : AsyncSession = Depends(get_async_session)):
    user_db = await utils.get_user_by_email(session, email=user.email)
    if user_db:
        raise HTTPException(status_code=400, detail="User already registered")
    result = await utils.create_user(session, user=user)
    return result


@router.post("/login/")
async def login(user: Login, session : AsyncSession = Depends(get_async_session)):
    user_db = await utils.get_user_by_email(session, email=user.email)
    if not user_db:
        raise HTTPException(status_code=400, detail="User not found")
    if user_db.password != user.password:
        raise HTTPException(status_code=400, detail="User not found")
    user_db.token = await utils.create_user_token(session, user=user_db)
    if not user_db.token :
        raise HTTPException(status_code=500, detail="Internal server error")

    result = JSONResponse(content={"message": "Login successful"})
    result.set_cookie(key="access_token", value=user_db.token.token)

    return result


@router.get("/users/me/", response_model=User)
async def me(current_user: CurrentUser):
    return current_user


@router.put("/users/change_role")
async def update_user_role(user_id: UserUpdateRole, current_user: CurrentUser, session : AsyncSession = Depends(get_async_session)):
    if current_user.role.lower() != "manager":
        raise HTTPException(status_code=403, detail="Permission denied. Only manager can update user roles.")
    user = utils.get_user_by_id(session, user_id.id)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    result = await utils.update_user(session, user_id)
    return result

@router.put("/users/change_login")
async def update_user_role(user_id: UserUpdateLogin, current_user: CurrentUser, session : AsyncSession = Depends(get_async_session)):
    if current_user.role.lower() != "manager":
        raise HTTPException(status_code=403, detail="Permission denied. Only manager can change users login.")
    user = utils.get_user_by_id(session, user_id.id)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    result = await utils.change_login(session, user_id)
    return result




