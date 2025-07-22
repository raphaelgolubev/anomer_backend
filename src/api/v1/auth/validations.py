from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.security import tokens, hashing_encoding
from src.database.ram_db import user_db
from src.schemas.users import UserCredentials

http_bearer = HTTPBearer()


def get_current_user_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    token = credentials.credentials
    try:
        # pyjwt самостоятельно проверит время жизни токена
        # и выбросит исключение, если токен просрочен
        payload = hashing_encoding.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Ошибка декодирования токена: {e}",
        )

    return payload


def get_user_from_token_payload(payload: dict):
    username: str | None = payload.get("sub")

    if user := user_db.get(username):
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен неверный"
    )


def validate_token_type(payload: dict, token_type: tokens.TokenType) -> bool:
    current_token_type: str | None = payload.get(tokens.TOKEN_TYPE_FIELD)

    if current_token_type == token_type.value:
        return True

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"""Невалидный тип токена {current_token_type!r}, 
        ожидался {token_type.value!r}""",
    )


def get_auth_user_from_token_of_type(token_type: tokens.TokenType):
    def get_auth_user_from_token(
        payload: dict = Depends(get_current_user_token_payload),
    ):
        if validate_token_type(payload, token_type):
            return get_user_from_token_payload(payload)

    return get_auth_user_from_token


get_current_auth_user = get_auth_user_from_token_of_type(
    tokens.TokenType.ACCESS_TOKEN_TYPE
)
get_current_auth_user_for_refresh = get_auth_user_from_token_of_type(
    tokens.TokenType.REFRESH_TOKEN_TYPE
)


def get_current_active_auth_user(
    user: UserCredentials = Depends(get_current_auth_user),
):
    if user and user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Пользователь не существует или не активен",
    )
