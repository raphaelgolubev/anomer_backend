from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.database import database
from src.security import tokens, hashing_encoding
from src.database.crud import users
from src.database.tables import User

http_bearer = HTTPBearer()


async def get_payload_from_token(
    http_creds: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    """
    Получает текущего авторизованного пользователя из токена в заголовке `Authorization`.

    Args:
        - `http_creds`: заголовок Authorization в формате `Bearer <token>`

    Raises:
        - `HTTPException`: если токен недействителен.

    Returns:
        `dict`: payload токена.
    """

    # получаем токен из заголовка Authorization
    token = http_creds.credentials

    try:
        # pyJWT самостоятельно проверит время жизни токена
        # и выбросит исключение, если токен просрочен
        payload: dict = hashing_encoding.decode_jwt(
            token=token
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = f"Ошибка декодирования токена: {e}"
        )

    return payload


async def get_user_from_payload(payload: dict) -> User | None:
    """
    Получает пользователя из БД по email из payload токена.
    Проверяет, что пользователь активирован.

    Args:
        - `payload`: payload токена.

    Raises:
        - `HTTPException`: если пользователь не найден или не активирован.

    Returns:
        `User`: текущий авторизованный пользователь.
    """

    # получаем email из payload
    subject: str | None = payload.get("sub")

    async with database.session_factory() as session:
        # получаем пользователя из БД
        if not (user := await users.get_user(session=session, email=subject)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден"
            )
        # проверяем, что пользователь активирован
        if not user.is_email_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Пользователь не активен"
            )

    return user


async def get_current_auth_user_for_access(payload: dict = Depends(get_payload_from_token)) -> User | None:
    """
    Получает текущего авторизованного пользователя из токена в заголовке `Authorization`.
    Проверяет, что токен имеет тип "access".
    """
    # проверяем, что токен имеет тип "access"
    if payload.get(tokens.TOKEN_TYPE_FIELD) != tokens.TokenType.ACCESS_TOKEN_TYPE.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный тип токена"
        )
    return await get_user_from_payload(payload)


async def get_current_auth_user_for_refresh(payload: dict = Depends(get_payload_from_token)) -> User | None:
    """
    Получает текущего авторизованного пользователя из токена в заголовке `Authorization`.
    Проверяет, что токен имеет тип "refresh".
    """
    # проверяем, что токен имеет тип "refresh"
    if payload.get(tokens.TOKEN_TYPE_FIELD) != tokens.TokenType.REFRESH_TOKEN_TYPE.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный тип токена"
        )
    return await get_user_from_payload(payload)
