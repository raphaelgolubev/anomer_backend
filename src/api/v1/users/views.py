from typing import Annotated

from fastapi import Depends, APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

import src.api.v1.auth.validations as validator
import src.database.crud.users as crud
from src.database import database
from src.security.hashing_encoding import hash_password
import src.schemas.users as scheme


router = APIRouter(tags=["Пользователи"])


@router.post("/create/")
async def create_new_user(
    user: scheme.UserCreateIn,
    session: Annotated[AsyncSession, Depends(database.session_getter)]
) -> scheme.UserCreateOut:
    # хешируем сырой пароль
    user.password = hash_password(user.password).decode()
    # создаем юзера в БД
    user = await crud.create_user(session=session, user_create=user)
    # возвращаем созданного юзера
    return user


@router.get("/")
async def get_all_users(
    session: Annotated[AsyncSession, Depends(database.session_getter)]
) -> list[scheme.UserRead]:
    users = await crud.get_all_users(session=session)
    return users


# @router.get("/me/")
# async def get_current_user(
#     payload: Annotated[dict, Depends(validator.get_current_user_token_payload)],
#     user: Annotated[scheme.UserCredentials, Depends(validator.get_current_active_auth_user)],
# ):
#     iat = payload.get("iat")
#     return {"logged_in_at": iat, "username": user.username, "email": user.email}
