from enum import Enum

import src.security.hashing_encoding as jwt_utils
from src.config import settings
from src.database.tables import User

TOKEN_TYPE_FIELD = "type"


class TokenType(Enum):
    ACCESS_TOKEN_TYPE = "access"
    REFRESH_TOKEN_TYPE = "refresh"


def create_jwt(token_type: TokenType, token_data: dict) -> str:
    """
    Создает JWT токен и добавляет в него информацию о типе токена
    в поле "type".
    
    Пример токена:
    ```json
    {
        "type": <token_type>,
        <token_data>,
    }
    ```

    Args:
        - `token_type`: тип токена
        - `token_data`: данные токена

    Returns:
        `str`: JWT токен
    """
    jwt_payload = {TOKEN_TYPE_FIELD: token_type.value}
    jwt_payload.update(token_data)

    match token_type:
        case TokenType.ACCESS_TOKEN_TYPE:
            return jwt_utils.encode_jwt(
                payload=jwt_payload,
                expire_minutes=settings.security.access_token_expire_minutes,
            )

        case TokenType.REFRESH_TOKEN_TYPE:
            return jwt_utils.encode_jwt(
                payload=jwt_payload,
                expire_minutes=settings.security.refresh_token_expire_minutes,
            )

        case _:
            raise ValueError(f"Unknown token type: {token_type}")


def create_token(user: User, token_type: TokenType) -> str:
    """
    Создает JWT токен и добавляет в него информацию о пользователе в
    поле "sub", информацию о типе токена в поле "type".

    Пример токена:
    ```json
    {
        "sub": "user@example.com",
        "type": "access"
    }
    ```

    Args:
        - `user`: пользователь
        - `token_type`: тип токена

    Returns:
        `str`: JWT токен
    """
    jwt_payload = {
        "sub": user.email,
    }
    return create_jwt(token_type=token_type, token_data=jwt_payload)
