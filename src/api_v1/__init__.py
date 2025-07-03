from fastapi import APIRouter

from src.api_v1.auth.views import router as auth_router

main_router = APIRouter(prefix="/api/v1")

main_router.include_router(auth_router)
