from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from auth.dependecies import CurrentUser
from database import get_async_session
import auth.utils as utils
from auth.schemas import Login, User, UserCreate


router = APIRouter()


@router.post("/sign-up/") #, response_model=User
async def create_user(user: UserCreate, session : AsyncSession = Depends(get_async_session)):
    user_db = await utils.get_user_by_email(session, email=user.email)
    if user_db:
        raise HTTPException(status_code=400, detail="User already registered")
    user = await utils.create_user(session, user=user)
    user.token = await utils.create_user_token(session, user=user)
    return {"success":"success"}


@router.post("/login/", response_model=User) #, response_model=User
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
    # print(str(user_db.token.token))
    # response.set_cookie(key="access_token", value=str(user_db.token))
    response.set_cookie(key="access_token", value=user_db.token.token)

    return response

    # return user_db
    # return {"success": "success"}
    # return user_db


@router.get("/users/me/", response_model=User) #, response_model=User
async def me(current_user: CurrentUser, session : AsyncSession = Depends(get_async_session)):
    # user = await utils.get_user_by_email(session, email=current_user)
    return current_user
    # return {"success": "success"}
    # return current_user


# @router.post("/users/me/public_key/", response_model=UserKeyInDB)
# async def update_public_key(
#     user_key: UserKey,
#     session : Depends(get_async_session),
#     current_user: CurrentUser,
# ):
#     return await utils.update_user_key(
#         session,
#         current_user,
#         user_key.public_key,
#     )