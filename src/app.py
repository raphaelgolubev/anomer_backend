from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1 import main_router as api_v1_router
from src.config import settings
from src.database import database


async def startup():
    """Выполняется при запуске приложения"""
    print("Startup")
    # Проверяем соединение с БД (соединение закроется или вернется в пул автоматически)
    try:
        await database.check_db_connection()
    except Exception:
        raise RuntimeError("Database connection check failed!")


async def shutdown():
    """Выполняется при остановке приложения"""
    print("Shutdown")
    # Закрываем все соединения в пуле
    await database.dispose()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Жизненный цикл приложения"""
    await startup()
    yield
    await shutdown()


main_app = FastAPI(
    lifespan=lifespan,
    version=settings.app.app_version,
    description="Anoma backend monolith",
)

main_app.include_router(api_v1_router)
