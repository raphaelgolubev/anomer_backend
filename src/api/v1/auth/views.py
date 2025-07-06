from fastapi import APIRouter, Depends, Form, HTTPException, status

import src.api.v1.auth.validations as validator
import src.security.hashing_encoding as jwt_utils
import src.security.tokens as tokens
from src.api.v1.auth.schemas import TokenInfo
from src.api.v1.users.schemas import UserCredentials
from src.database.ram_db import user_db

router = APIRouter(prefix="/auth", tags=["Авторизация"])


def get_login_credentials(
    username: str = Form(),
    password: str = Form()
):
    unauthorized_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Неверные учетные данные'
    )
    if not (user := user_db.get(username)):
        raise unauthorized_exc

    if not jwt_utils.verify_password(
        password=password,
        hashed_password=user.password
    ):
        raise unauthorized_exc

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Пользователь не активен'
        )

    return user


@router.post('/login/', response_model=TokenInfo)
async def login(
    credentials: UserCredentials = Depends(get_login_credentials)
):
    access_token = tokens.create_access_token(user=credentials)
    refresh_token = tokens.create_refresh_token(user=credentials)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post(
    '/refresh/',
    response_model=TokenInfo,
    response_model_exclude_none=True
)
async def refresh_token(
    credentials: UserCredentials = Depends(validator.get_current_auth_user_for_refresh)
):
    access_token = tokens.create_access_token(user=credentials)

    return TokenInfo(
        access_token=access_token
    )



