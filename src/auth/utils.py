from datetime import datetime, timedelta

from sqlalchemy import select, update
from sqlalchemy.orm import joinedload

from models.models import User, UserToken
from auth.schemas import UserCreate, UserUpdateRole, UpdateResult, UserUpdateLogin, UserChangePassword


async def get_user_by_email(session, email: str) -> User:
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    return result.scalars().first()


async def get_user_by_id(session, id: int) -> User:
    statement = select(User).where(User.id == id)
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
        role=user.role,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def create_user_token(session, user: User) -> UserToken:
    db_token = UserToken(
        user=user, expires=datetime.now() + timedelta(weeks=2)
    )
    session.add(db_token)
    await session.commit()
    return db_token


async def update_user(session, user: UserUpdateRole) -> UpdateResult:
    update_query = update(User).where(User.id == user.id).values(role=user.new_role)
    await session.execute(update_query)
    await session.commit()

    updated_user = await session.execute(select(User).where(User.id == user.id))
    updated_user = updated_user.scalar()

    return UpdateResult(success=True, message="User role updated successfully", updated_user=updated_user)

async def change_login(session, user: UserUpdateLogin) -> UpdateResult:
    update_query = update(User).where(User.id == user.id).values(email=user.new_email)
    await session.execute(update_query)
    await session.commit()

    updated_user = await session.execute(select(User).where(User.id == user.id))
    updated_user = updated_user.scalar()

    return UpdateResult(success=True, message="User login changed successfully", updated_user=updated_user)


async def change_password(session, user: UserChangePassword) -> UpdateResult:
    query = update(User).where(User.email == user.email).values(password = user.new_password)
    await session.execute(query)
    await session.commit()
    return {"status":"success"}