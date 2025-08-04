from typing import Annotated

from fastapi import Form, Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import src.security.tokens as tokens
import src.api.v1.auth.service as service
import src.security.hashing_encoding as jwt_utils

from src.database.crud import users
from src.database import database
from src.database.tables import User
from src.schemas.auth import TokenInfo

router = APIRouter(tags=["Авторизация"])


async def get_login_credentials(
    session: Annotated[AsyncSession, Depends(database.session_getter)],
    username: str = Form(), 
    password: str = Form()
) -> User:
    unauthorized_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные учетные данные"
    )
    if not (user := await users.get_user(session=session, email=username)):
        raise unauthorized_exc

    if not jwt_utils.verify_password(password=password, hashed_password=user.password):
        raise unauthorized_exc

    if not user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Пользователь не активен"
        )

    return user


@router.post("/login/", response_model=TokenInfo)
async def login(
    user: Annotated[User, Depends(get_login_credentials)],
):
    access_token = tokens.create_token(user=user, token_type=tokens.TokenType.ACCESS_TOKEN_TYPE)
    refresh_token = tokens.create_token(user=user, token_type=tokens.TokenType.REFRESH_TOKEN_TYPE)

    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post("/test_access_token/")
async def test_access_token(
    user: Annotated[User | None, Depends(service.get_current_auth_user_for_access)],
):
    if user:
        return {"message": "Token is valid", "user": user.email}
    return {"message": "Token is invalid"}


@router.post("/test_refresh_token/")
async def test_refresh_token(
    user: Annotated[User | None, Depends(service.get_current_auth_user_for_refresh)],
):
    if user:
        return {"message": "Token is valid", "user": user.email}
    return {"message": "Token is invalid"}


@router.post("/refresh/", response_model=TokenInfo)
async def refresh_token(
    user: Annotated[
        User | None, Depends(service.get_current_auth_user_for_refresh)
    ],
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный тип токена"
        )

    access_token = tokens.create_token(user=user, token_type=tokens.TokenType.ACCESS_TOKEN_TYPE)
    refresh_token = tokens.create_token(user=user, token_type=tokens.TokenType.REFRESH_TOKEN_TYPE)

    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout/")
async def logout(
    user: Annotated[User | None, Depends(service.get_current_auth_user_for_access)],
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный тип токена"
        )

    return {"message": f"Logout placeholder for {user.email}"}
