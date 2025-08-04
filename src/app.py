
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.v1 import main_router as api_v1_router
from src.config import settings
from src.database import database


async def startup():
    """Выполняется при запуске приложения"""
    print("Startup")

    print("\nmodel dumps:")
    print("\nserver", f"\n{settings.server.model_dump_json(indent=4)}")
    print("\napp", f"\n{settings.app.model_dump_json(indent=4)}")
    print("\nsecurity", f"\n{settings.security.model_dump_json(indent=4)}")
    print("\ndb", f"\n{settings.db.model_dump_json(indent=4)}")
    print("\nmail", f"\n{settings.mail.model_dump_json(indent=4)}")
    print("\nredis", f"\n{settings.redis.model_dump_json(indent=4)}")

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
async def lifespan(_app: FastAPI):
    """Жизненный цикл приложения"""
    await startup()
    yield
    await shutdown()


app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    version=settings.app.app_version,
    description="Anomer backend monolith",
)

app.include_router(api_v1_router)
