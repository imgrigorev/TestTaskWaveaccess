from datetime import datetime, timedelta

from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models.models import User, UserToken
from auth.schemas import UserCreate


async def get_user_by_email(session, email: str) -> User:
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    return result.scalars().first()


async def get_user_by_token(session, token: str) -> User:
    statement = (
        select(UserToken)
        .where(UserToken.token == token)
        .options(joinedload(UserToken.user))
    )
    result = await session.execute(statement)
    token = result.scalars().first()
    return token.user


async def create_user(session, user: UserCreate) -> User:
    db_user = User(
        email=user.email,
        name=user.name,
        password=user.password,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def create_user_token(session, user: User) -> UserToken:
    db_token = UserToken(
        user=user, expires=datetime.now() + timedelta(weeks=2)
    )
    # db_token = session.execute(insert(UserToken).values( user=user, expires=datetime.now() + timedelta(weeks=2)))
    session.add(db_token)
    await session.commit()
    return db_token


# async def update_user_key(
#     db: AsyncSession,
#     user: User,
#     public_key: str,
# ) -> UserKeys:
#     statement = (
#         update(UserKeys).where(UserKeys.user == user).values(is_revoked=True)
#     )
#     await db.execute(statement)
#     db_key = UserKeys(user=user, public_key=public_key)
#     db.add(db_key)
#     await db.commit()
#     await db.refresh(db_key)
#     return db_key


# async def get_user_key(
#     db: AsyncSession,
#     user: User,
# ) -> UserKeys:
#     statement = select(UserKeys).where(
#         (UserKeys.user == user) & (UserKeys.is_revoked == False)
#     )
#     result = await db.execute(statement)
#     return result.scalars().first()