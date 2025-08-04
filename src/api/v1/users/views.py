from uuid import UUID
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import src.schemas.users as scheme
import src.api.v1.auth.service as auth_service
import src.database.crud.users as crud
import src.api.v1.users.service as service
from src.database import database
from src.database.tables import User
from src.security.hashing_encoding import hash_password

router = APIRouter(tags=["Пользователи"])


@router.post("/create/")
async def create_new_user(
    user: scheme.UserCreateIn,
    session: Annotated[AsyncSession, Depends(database.session_getter)],
) -> scheme.UserCreateOut:
    # хешируем сырой пароль
    user.password = hash_password(user.password).decode()
    # создаем юзера в БД
    try:
        user = await crud.create_user(session=session, user_create=user)
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Пользователь с таким email уже существует"
        )
    # возвращаем созданного юзера
    return user


@router.post("/send-verification/")
async def send_verification_email(
    email_data: scheme.EmailVerificationIn,
    session: Annotated[AsyncSession, Depends(database.session_getter)],
) -> scheme.EmailVerificationOut:
    """
    Отправляет код верификации на email
    """
    # проверяем, существует ли пользователь
    user_exists = await crud.is_user_exists(session, email_data.id)
    if not user_exists:
        raise HTTPException(status_code=400, detail="Пользователь не найден")

    # проверяем, верифицирован ли email
    is_verified = await crud.is_user_email_verified(session, email_data.id)
    if is_verified:
        raise HTTPException(status_code=400, detail="Email уже верифицирован")

    success = await service.send_verification_email(email_data.email)

    if not success:
        raise HTTPException(
            status_code=500, detail="Не удалось отправить код верификации"
        )

    return scheme.EmailVerificationOut(message="Код верификации отправлен на ваш email")


@router.post("/verify-code/")
async def verify_email_code(
    verify_data: scheme.VerifyCodeIn,
    session: Annotated[AsyncSession, Depends(database.session_getter)],
) -> scheme.VerifyCodeOut:
    """
    Проверяет код верификации и обновляет статус пользователя
    """
    # Проверяем код
    code_valid = await service.verify_email_code(verify_data.email, verify_data.code)

    if not code_valid:
        return scheme.VerifyCodeOut(
            verified=False, message="Неверный код верификации или код истек"
        )

    # Обновляем статус в базе данных
    updated = await crud.verify_user_email(session, verify_data.email)

    if not updated:
        return scheme.VerifyCodeOut(
            verified=False, message="Пользователь с таким email не найден"
        )

    return scheme.VerifyCodeOut(verified=True, message="Email успешно подтвержден")


@router.get("/")
async def get_all_users(
    session: Annotated[AsyncSession, Depends(database.session_getter)],
) -> list[scheme.UserRead]:
    users = await crud.get_all_users(session=session)
    return users


@router.get("/me/")
async def get_current_user(
    user: Annotated[
        User | None, Depends(auth_service.get_current_auth_user_for_access)
    ],
) -> scheme.UserRead:
    return user


@router.delete("/delete/{user_id}")
async def delete_user(
    user_id: UUID, session: Annotated[AsyncSession, Depends(database.session_getter)]
) -> scheme.UserDeleteOut:
    deleted = await crud.delete_user(session=session, user_id=user_id)
    return scheme.UserDeleteOut(is_deleted=deleted)
