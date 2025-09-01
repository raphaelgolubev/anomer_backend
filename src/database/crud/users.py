from typing import Sequence

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

import src.schemas.users as scheme
from src.database.tables import User
from src.entities import UserStatus


async def get_user(session: AsyncSession, email: str = None, user_id: int = None) -> User:
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


async def is_user_exists(session: AsyncSession, user_id: int) -> bool:
    stmt = select(User).where(User.id == user_id)
    result = await session.scalar(stmt)
    return result is not None


async def is_user_email_verified(session: AsyncSession, user_id: int) -> bool:
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


async def delete_user(session: AsyncSession, user_id: int) -> bool:
    """
    Удаляет пользователя и все связанные с ним данные каскадом.
    
    Args:
        session: Сессия базы данных
        user_id: ID пользователя для удаления
        
    Returns:
        bool: True если пользователь успешно удален
    """
    # Получаем пользователя с загруженными связями
    user = await get_user(session=session, user_id=user_id)
    if not user:
        return False
    
    # Удаляем пользователя - SQLAlchemy автоматически удалит связанные записи
    # благодаря cascade="all, delete-orphan" в relationship
    await session.delete(user)
    await session.commit()
    
    return True
