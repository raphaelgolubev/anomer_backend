import random
import string

from src.utils.emails import send_verification_code
from src.utils.redis_client import redis_client


def generate_verification_code():
    """Генерирует 6-значный код для верификации"""
    return "".join(random.choices(string.digits, k=6))


async def send_verification_email(email: str) -> bool:
    """
    Генерирует код верификации, сохраняет в Redis и отправляет на email

    Args:
        email: Email пользователя

    Returns:
        bool: True если код успешно отправлен
    """
    # Генерируем код
    code = generate_verification_code()

    # Сохраняем в Redis с TTL
    saved = await redis_client.set_verification_code(email, code)
    if not saved:
        return False

    # Отправляем email
    email_sent = await send_verification_code(email, code)
    return email_sent


async def verify_email_code(email: str, code: str) -> bool:
    """
    Проверяет код верификации для email

    Args:
        email: Email пользователя
        code: Код верификации

    Returns:
        bool: True если код верный
    """
    stored_code = await redis_client.get_verification_code(email)
    if not stored_code:
        return False

    if stored_code == code:
        # Удаляем использованный код
        await redis_client.delete_verification_code(email)
        return True

    return False
