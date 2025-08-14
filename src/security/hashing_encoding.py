"""Набор функций хэширования, кодирования, декодирования и верификации хэша"""

from datetime import datetime, timezone, timedelta

import jwt
import bcrypt

from src.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.security.secret_pem_file.read_text(),
    algorithm: str = settings.security.algorithm,
    expire_timedelta: timedelta | None = None,
    expire_minutes: int | None = None,
):
    """
    Кодирует payload в JWT токен. Добавляет в payload поля:
    - `exp` (expire) - время истечения токена
    - `iat` (issued_at) - время создания токена

    Args:
        - `payload`: данные токена
        - `private_key`: приватный ключ
        - `algorithm`: алгоритм шифрования
        - `expire_timedelta`: время жизни токена
        - `expire_minutes`: время жизни токена в минутах

    Returns:
        `str`: JWT токен
    """
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)

    if expire_timedelta:
        expire = now + expire_timedelta
    elif expire_minutes:
        expire = now + timedelta(minutes=expire_minutes)
    else:
        raise ValueError(
            "Не передан ни один из параметров 'expire_timedelta', 'expire_minutes'"
        )
    # добавляем поля expire (когда истекает) и issued_at (когда создан)
    to_encode.update(exp=expire, iat=now)

    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.security.public_pem_file.read_text(),
    algorithm: str = settings.security.algorithm,
) -> dict:
    """
    Декодирует JWT токен с использованием публичного ключа.
    Возвращает payload, полученный из токена.

    Args:
        - `token`: JWT токен
        - `public_key`: публичный ключ
        - `algorithm`: алгоритм шифрования

    Returns:
        `dict`: данные токена (payload)
    """
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    """
    Хеширует пароль с добавлением рандомой соли.
    Возвращает хэш пароля в байтах.

    Args:
        - `password`: пароль

    Returns:
        `bytes`: хешированный пароль
    """
    # генерируем соль
    salt = bcrypt.gensalt()
    # получаем пароль, кастим в байты
    pwd_bytes: bytes = password.encode("utf-8")
    # хэшируем пароль используя соль
    return bcrypt.hashpw(pwd_bytes, salt)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Проверяет, совпадает ли хэш пароля `password` с хэшем `hashed_password`.

    Args:
        - `password`: пароль
        - `hashed_password`: хешированный пароль

    Returns:
        `bool`: True, если пароль совпадает с хешированным паролем, False в противном случае
    """
    return bcrypt.checkpw(
        password=password.encode("utf-8"),
        hashed_password=hashed_password.encode("utf-8"),
    )
