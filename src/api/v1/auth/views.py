from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import src.security.tokens as tokens
import src.api.v1.auth.service as service
from src.database import database
from src.schemas.auth import TokenInfo
from src.database.crud import blacklisted_tokens
from src.database.tables import User

from src.exceptions import CustomHTTPException
import src.exceptions.error_codes as error_code

router = APIRouter(tags=["Авторизация"])


@router.post("/login/", response_model=TokenInfo)
async def login(user: Annotated[User, Depends(service.get_login_credentials)]):
    access_token = tokens.create_token(
        user=user, token_type=tokens.TokenType.ACCESS_TOKEN_TYPE
    )
    refresh_token = tokens.create_token(
        user=user, token_type=tokens.TokenType.REFRESH_TOKEN_TYPE
    )

    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh/", response_model=TokenInfo)
async def refresh_token(
    user: Annotated[User | None, Depends(service.get_current_auth_user_for_refresh)],
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный тип токена"
        )

    access_token = tokens.create_token(
        user=user, token_type=tokens.TokenType.ACCESS_TOKEN_TYPE
    )
    refresh_token = tokens.create_token(
        user=user, token_type=tokens.TokenType.REFRESH_TOKEN_TYPE
    )

    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout/")
async def logout(
    user: Annotated[User | None, Depends(service.get_current_auth_user_for_access)],
    payload: Annotated[dict, Depends(service.get_payload_from_token)],
    session: Annotated[AsyncSession, Depends(database.session_getter)],
):
    """
    Выход из системы - деактивация текущего access токена.
    После этого токен становится недействительным.
    """
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный тип токена"
        )

    # Получаем информацию о токене
    jti = payload.get(tokens.TOKEN_ID_FIELD)
    token_type = payload.get(tokens.TOKEN_TYPE_FIELD)

    if not jti:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Токен не содержит идентификатор",
        )

    # Получаем время истечения токена из JWT payload
    try:
        expires_at = tokens.get_token_expire_time_from_payload(payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка извлечения времени истечения токена: {e}",
        )

    try:
        # очищаем любые истекшие токены из БД
        await blacklisted_tokens.cleanup_expired_tokens(session=session)
        # добавляем токен в черный список
        await blacklisted_tokens.add_to_blacklist(
            session=session,
            jti=jti,
            token_type=token_type,
            user_id=user.id,
            expires_at=expires_at,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при деактивации токена: {e}",
        )

    return {
        "message": "Выход выполнен успешно",
        "user_email": user.email,
        "token_deactivated": True,
    }


# @router.post("/test_access_token/")
# async def test_access_token(
#     user: Annotated[User | None, Depends(service.get_current_auth_user_for_access)],
# ):
#     if user:
#         return {"message": "Token is valid", "user": user.email}
#     return {"message": "Token is invalid"}


# @router.post("/test_refresh_token/")
# async def test_refresh_token(
#     user: Annotated[User | None, Depends(service.get_current_auth_user_for_refresh)],
# ):
#     if user:
#         return {"message": "Token is valid", "user": user.email}
#     return {"message": "Token is invalid"}
