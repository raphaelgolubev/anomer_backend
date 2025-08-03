from typing import Sequence
from uuid import UUID

from sqlalchemy import select, update
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


async def is_user_exists(
    session: AsyncSession,
    user_id: UUID
) -> bool:
    stmt = select(User).where(User.id == user_id)
    result = await session.scalar(stmt)
    return result is not None


async def is_user_email_verified(
    session: AsyncSession,
    user_id: UUID
) -> bool:
    stmt = select(User).where(User.id == user_id)
    result = await session.scalar(stmt)
    return result.is_email_verified


async def verify_user_email(
    session: AsyncSession,
    email: str
) -> bool:
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
            update(User)
            .where(User.email == email)
            .values(is_email_verified=True)
        )
        result = await session.execute(stmt)
        await session.commit()
        
        return result.rowcount > 0
    except Exception as e:
        await session.rollback()
        print(f"Database error: {e}")
        return False
