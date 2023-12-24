from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from auth.dependecies import CurrentUser
from database import get_async_session
import auth.utils as utils
from auth.schemas import Login, User, UserCreate, UserUpdateRole, UserUpdateLogin


router = APIRouter()

"""!!!!Доделать!!!!"""
@router.post("/change_password/") #, response_model=User
async def create_user(user: UserCreate, session : AsyncSession = Depends(get_async_session)):
    user_db = await utils.get_user_by_email(session, email=user.email)
    if user_db:
        raise HTTPException(status_code=400, detail="User already registered")
    # user = await utils.create_user(session, user=user)
    # # user.token = await utils.create_user_token(session, user=user)
    # return {"registration status": "success"}



@router.post("/sign-up/") #, response_model=User
async def create_user(user: UserCreate, session : AsyncSession = Depends(get_async_session)):
    user_db = await utils.get_user_by_email(session, email=user.email)
    if user_db:
        raise HTTPException(status_code=400, detail="User already registered")
    user = await utils.create_user(session, user=user)
    # user.token = await utils.create_user_token(session, user=user)
    return {"registration status": "success"}


@router.post("/login/") #, response_model=User
async def login(user: Login, session : AsyncSession = Depends(get_async_session)):
    user_db = await utils.get_user_by_email(session, email=user.email)
    if not user_db:
        raise HTTPException(status_code=400, detail="User not found")
    if user_db.password != user.password:
        raise HTTPException(status_code=400, detail="User not found")
    user_db.token = await utils.create_user_token(session, user=user_db)
    if not user_db.token :
        raise HTTPException(status_code=500, detail="Internal server error")

    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(key="access_token", value=user_db.token.token)

    return response


@router.get("/users/me/", response_model=User) #, response_model=User
async def me(current_user: CurrentUser): #, session : AsyncSession = Depends(get_async_session)
    return current_user


""" Управление пользователями для админа """
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




