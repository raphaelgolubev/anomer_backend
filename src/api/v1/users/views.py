from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import src.schemas.users as scheme
import src.api.v1.auth.service as auth_service
import src.database.crud.users as crud
import src.api.v1.users.service as service
from src.database import database
from src.database.tables import User
from src.security.hashing_encoding import hash_password

from src.config import settings

from src.exceptions import CustomHTTPException
import src.exceptions.error_codes as error_code

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
        raise CustomHTTPException(
            error_code.USER_ALREADY_EXISTS,
            scheme.UserCreateOut(
                created=False, message="Пользователь с таким email уже существует"
            ),
        )

    # возвращаем созданного юзера
    user.created = True
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
    if not (user := await crud.get_user(session=session, user_id=email_data.id)):
        raise CustomHTTPException(
            error_code.USER_NOT_FOUND,
            scheme.EmailVerificationOut(sent=False, message="Пользователь не найден"),
        )

    # проверяем, верифицирован ли email
    is_verified = await crud.is_user_email_verified(session, email_data.id)
    if is_verified:
        raise CustomHTTPException(
            error_code.EMAIL_ALREADY_VERIFIED,
            scheme.EmailVerificationOut(sent=False, message="Email уже верифицирован"),
        )

    success = await service.send_verification_email(user.email)

    if not success:
        raise CustomHTTPException(
            error_code.UNABLE_SEND_EMAIL,
            scheme.EmailVerificationOut(
                sent=False, message="Не удалось отправить код верификации"
            ),
        )

    return scheme.EmailVerificationOut(
        sent=True,
        message="Код верификации отправлен на ваш email",
        code_expires_in_seconds=settings.redis.verification_code_ttl,
    )


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
        raise CustomHTTPException(
            error_code.INCORRECT_VERIFICATION_CODE,
            scheme.VerifyCodeOut(
                verified=False, message="Неверный код верификации или код истек"
            ),
        )

    # Обновляем статус в базе данных
    updated = await crud.verify_user_email(session, verify_data.email)

    if not updated:
        raise CustomHTTPException(
            error_code.USER_NOT_FOUND,
            scheme.VerifyCodeOut(
                verified=False, message="Пользователь с таким email не найден"
            ),
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
    user_id: int, session: Annotated[AsyncSession, Depends(database.session_getter)]
) -> scheme.UserDeleteOut:
    """
    Удаляет пользователя и все связанные с ним данные каскадом.

    Args:
        user_id: ID пользователя для удаления
        session: Сессия базы данных

    Returns:
        UserDeleteOut: Результат операции удаления
    """
    try:
        deleted = await crud.delete_user(session=session, user_id=user_id)
        if not deleted:
            raise CustomHTTPException(
                error_code.USER_NOT_FOUND,
                scheme.UserDeleteOut(
                    deleted=False, message=f"Пользователь с ID {user_id} не найден"
                ),
            )

        return scheme.UserDeleteOut(
            deleted=True,
            message=f"Пользователь {user_id} и все связанные данные успешно удалены",
        )
    except Exception as e:
        # Логируем ошибку для отладки
        print(f"Error deleting user {user_id}: {e}")
        raise CustomHTTPException(
            error_code.USER_DELETE_ERROR,
            scheme.UserDeleteOut(
                deleted=False, message="Произошла ошибка при удалении пользователя"
            ),
        )
