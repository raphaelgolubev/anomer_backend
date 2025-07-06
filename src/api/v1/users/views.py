from fastapi import APIRouter, Depends

import src.api.v1.auth.validations as validator
from src.api.v1.users.schemas import UserCredentials

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get('/users/me/')
async def get_current_user(
    payload: dict = Depends(validator.get_current_user_token_payload),
    user: UserCredentials = Depends(validator.get_current_active_auth_user)
):
    iat = payload.get('iat')
    return {
        'logged_in_at': iat,
        'username': user.username,
        'email': user.email,
    }
