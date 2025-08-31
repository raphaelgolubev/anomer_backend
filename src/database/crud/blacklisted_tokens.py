from typing import Optional
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.tables import BlacklistedToken


async def add_to_blacklist(
    session: AsyncSession, jti: str, token_type: str, user_id: str, expires_at: datetime
) -> BlacklistedToken:
    """
    Добавляет токен в черный список.

    Args:
        session: Сессия базы данных
        jti: JWT ID (уникальный идентификатор токена)
        token_type: Тип токена (access, refresh)
        user_id: ID пользователя
        expires_at: Время истечения токена

    Returns:
        BlacklistedToken: Объект деактивированного токена
    """
    # Конвертируем datetime в Unix timestamp
    if expires_at.tzinfo:
        # Если есть timezone info, конвертируем в UTC timestamp
        expires_timestamp = int(expires_at.astimezone(timezone.utc).timestamp())
    else:
        # Если нет timezone info, считаем что это UTC и конвертируем в timestamp
        expires_timestamp = int(expires_at.replace(tzinfo=timezone.utc).timestamp())

    blacklisted_token = BlacklistedToken(
        jti=jti, token_type=token_type, user_id=user_id, expires_at=expires_timestamp
    )

    session.add(blacklisted_token)
    await session.commit()
    return blacklisted_token


async def is_token_blacklisted(session: AsyncSession, jti: str) -> bool:
    """
    Проверяет, находится ли токен в черном списке.

    Args:
        session: Сессия базы данных
        jti: JWT ID (уникальный идентификатор токена)

    Returns:
        bool: True, если токен в черном списке, False в противном случае
    """
    stmt = select(BlacklistedToken).where(BlacklistedToken.jti == jti)
    result = await session.execute(stmt)
    return result.scalar_one_or_none() is not None


async def get_blacklisted_token(
    session: AsyncSession, jti: str
) -> Optional[BlacklistedToken]:
    """
    Получает информацию о деактивированном токене по его JTI.

    Args:
        session: Сессия базы данных
        jti: JWT ID (уникальный идентификатор токена)

    Returns:
        Optional[BlacklistedToken]: Объект деактивированного токена или None
    """
    stmt = select(BlacklistedToken).where(BlacklistedToken.jti == jti)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def cleanup_expired_tokens(session: AsyncSession) -> int:
    """
    Удаляет истекшие токены из черного списка для очистки БД.

    Args:
        session: Сессия базы данных

    Returns:
        int: Количество удаленных записей
    """
    from sqlalchemy import delete

    # Получаем текущий Unix timestamp
    current_timestamp = int(datetime.now(timezone.utc).timestamp())
    
    stmt = delete(BlacklistedToken).where(
        BlacklistedToken.expires_at < current_timestamp
    )

    result = await session.execute(stmt)
    await session.commit()

    return result.rowcount


async def get_user_blacklisted_tokens(
    session: AsyncSession, user_id: str, limit: int = 50
) -> list[BlacklistedToken]:
    """
    Получает список деактивированных токенов пользователя.

    Args:
        session: Сессия базы данных
        user_id: ID пользователя
        limit: Максимальное количество записей

    Returns:
        list[BlacklistedToken]: Список деактивированных токенов
    """
    stmt = (
        select(BlacklistedToken)
        .where(BlacklistedToken.user_id == user_id)
        .order_by(BlacklistedToken.created_at.desc())
        .limit(limit)
    )

    result = await session.execute(stmt)
    return list(result.scalars().all())
