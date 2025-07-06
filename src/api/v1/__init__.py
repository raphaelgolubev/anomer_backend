from fastapi import APIRouter

from src.api.v1.auth.views import router as auth_router
from src.api.v1.users.views import router as users_router
from src.config import settings

main_router = APIRouter(prefix=f"{settings.app.prefix}/v1")
main_router.include_router(auth_router)
main_router.include_router(users_router)
