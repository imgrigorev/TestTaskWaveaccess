from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import get_user_by_token
from models.models import User
from database import get_async_session

# from app.db.session import SessionLocal


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="access_token")




# async def get_current_user(
#     session : AsyncSession = Depends(get_async_session), token: str = Depends(oauth2_scheme)
# ) -> User: #-> User
#     """Get user based on token."""
#     user = await get_user_by_token(session, token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     # return {"status" : "success"}
#     return user
async def get_current_user(
        request: Request, session: AsyncSession = Depends(get_async_session)
) -> User:
    """Get user based on token."""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await get_user_by_token(session, token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


# DBSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
#
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
# from sqlalchemy.ext.asyncio import AsyncSession
#
# import auth.utils as utils
# from database import get_async_session
# from typing import Optional
#
# SECRET_KEY = "your_secret_key"  # Замените на ваш секретный ключ
# ALGORITHM = "HS256"  # Выберите подходящий алгоритм подписи для JWT
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_async_session)):
#     print(f"{token} - from dependencies")
#
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     user = await utils.get_user_by_token(session, token)
#     if user is None:
#         raise credentials_exception
#     return user


# # Пример использования middleware в роуте
# @router.get("/protected-data/")
# async def get_protected_data(current_user: str = Depends(check_user_activity)):
#     # Ваш код для обработки запроса от авторизованного пользователя
#     return {"message": "Access granted"}
