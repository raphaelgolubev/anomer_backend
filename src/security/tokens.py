from enum import Enum

import src.security.hashing_encoding as jwt_utils
from src.api.v1.users.schemas import UserCredentials
from src.config import settings

TOKEN_TYPE_FIELD = "type"


class TokenType(Enum):
    ACCESS_TOKEN_TYPE = "access"
    REFRESH_TOKEN_TYPE = "refresh"


def create_jwt(token_type: TokenType, token_data: dict) -> str:
    jwt_payload = {
        TOKEN_TYPE_FIELD: token_type.value
    }
    jwt_payload.update(token_data)

    match token_type:
        case TokenType.ACCESS_TOKEN_TYPE:
            return jwt_utils.encode_jwt(
                payload=jwt_payload,
                expire_minutes=settings.security.access_token_expire_minutes
            )

        case TokenType.REFRESH_TOKEN_TYPE:
            return jwt_utils.encode_jwt(
                payload=jwt_payload,
                expire_minutes=settings.security.refresh_token_expire_minutes
            )

        case _:
            raise ValueError(f"Unknown token type: {token_type}")


def create_access_token(user: UserCredentials) -> str:
    jwt_payload = {
        "sub": user.username,
        "email": user.email,
    }
    return create_jwt(
        token_type=TokenType.ACCESS_TOKEN_TYPE,
        token_data=jwt_payload
    )


def create_refresh_token(user: UserCredentials) -> str:
    jwt_payload = {
        "sub": user.username,
    }
    return create_jwt(
        token_type=TokenType.REFRESH_TOKEN_TYPE,
        token_data=jwt_payload
    )
