from uuid import UUID
from typing import Sequence

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

import src.schemas.users as scheme
from src.database.tables import User
from src.entities import UserStatus


async def get_user(session: AsyncSession, email: str = None, user_id: UUID = None) -> User:
    if email:
        stmt = select(User).where(User.email == email)
    elif user_id:
        stmt = select(User).where(User.id == user_id)
    else:
        raise ValueError("Не передан ни один из параметров: email, user_id")

    result = await session.scalar(stmt)

    return result


async def get_all_users(session: AsyncSession) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)

    return result.all()


async def create_user(session: AsyncSession, user_create: scheme.UserCreateIn) -> User:
    user = User(**user_create.model_dump())

    session.add(user)

    await session.commit()
    await session.refresh(user)

    return user


async def is_user_exists(session: AsyncSession, user_id: UUID) -> bool:
    stmt = select(User).where(User.id == user_id)
    result = await session.scalar(stmt)
    return result is not None


async def is_user_email_verified(session: AsyncSession, user_id: UUID) -> bool:
    stmt = select(User).where(User.id == user_id)
    result = await session.scalar(stmt)

    return result.status == UserStatus.ACTIVATED


async def verify_user_email(session: AsyncSession, email: str) -> bool:
    """
    Обновляет статус верификации email пользователя

    Args:
        session: Сессия базы данных
        email: Email пользователя

    Returns:
        bool: True если статус успешно обновлен
    """
    try:
        stmt = (
            update(User).where(User.email == email).values(status=UserStatus.ACTIVATED)
        )
        result = await session.execute(stmt)
        await session.commit()

        return result.rowcount > 0
    except Exception as e:
        await session.rollback()
        print(f"Database error: {e}")
        return False


async def delete_user(session: AsyncSession, user_id: UUID) -> bool:
    stmt = delete(User).where(User.id == user_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0
