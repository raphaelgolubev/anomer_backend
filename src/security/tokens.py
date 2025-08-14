from enum import Enum
import uuid
from datetime import datetime, timezone

import src.security.hashing_encoding as jwt_utils
from src.config import settings
from src.database.tables import User

TOKEN_TYPE_FIELD = "type"
TOKEN_ID_FIELD = "jti"


class TokenType(Enum):
    ACCESS_TOKEN_TYPE = "access"
    REFRESH_TOKEN_TYPE = "refresh"


def create_token(user: User, token_type: TokenType) -> str:
    """
    Создает JWT токен и добавляет в него: 
    - информацию о пользователе в поле "sub"
    - информацию о типе токена в поле "type" 
    - уникальный идентификатор токена в поле "jti".

    Пример токена:
    ```json
    {
        "sub": "user@example.com",
        "type": "access",
        "jti": "unique-token-id"
    }
    ```

    Args:
        - `user`: пользователь
        - `token_type`: тип токена

    Returns:
        `str`: JWT токен
    """
    # Генерируем уникальный идентификатор для токена
    jti = str(uuid.uuid4())

    jwt_payload = {
        TOKEN_TYPE_FIELD: token_type.value,
        TOKEN_ID_FIELD: jti,
        "sub": user.email
    }

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


def get_token_expire_time_from_payload(payload: dict) -> datetime:
    """
    Извлекает время истечения токена из JWT payload.
    Это гарантирует, что время совпадает с тем, что зашито в JWT.
    
    Args:
        payload: раскодированный JWT payload
        
    Returns:
        datetime: время истечения токена из JWT
        
    Raises:
        ValueError: если поле exp отсутствует в payload
    """
    exp_timestamp = payload.get("exp")
    if exp_timestamp is None:
        raise ValueError("Отсутствует поле 'exp' в JWT payload")

    # JWT exp - это timestamp в секундах от epoch
    return datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
