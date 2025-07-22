from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.tables import User
import src.schemas.users as scheme 


async def get_all_users(
    session: AsyncSession
) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)

    return result.all()


async def create_user(
    session: AsyncSession,
    user_create: scheme.UserCreateIn
) -> User:
    user = User(**user_create.model_dump())

    session.add(user)

    await session.commit()
    await session.refresh(user)

    return user
