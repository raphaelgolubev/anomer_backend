from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api_v1 import main_router as api_v1_router


async def startup():
    """ Выполняется при запуске приложения """
    print("Startup")


async def shutdown():
    """ Выполняется при остановке приложения """
    print("Shutdown")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """  """
    await startup()
    yield
    await shutdown()


app = FastAPI(
    lifespan=lifespan,
)

app.include_router(api_v1_router)
