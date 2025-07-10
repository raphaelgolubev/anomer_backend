from typing import Annotated

from fastapi import Depends, APIRouter

import src.api.v1.auth.validations as validator
from src.config import settings
from src.api.v1.users.schemas import UserCredentials

router = APIRouter(prefix=settings.app.v1.users, tags=["Пользователи"])


@router.get("/users/me/")
async def get_current_user(
    payload: Annotated[dict, Depends(validator.get_current_user_token_payload)],
    user: Annotated[UserCredentials, Depends(validator.get_current_active_auth_user)],
):
    iat = payload.get("iat")
    return {"logged_in_at": iat, "username": user.username, "email": user.email}
