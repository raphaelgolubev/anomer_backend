from contextlib import asynccontextmanager

from fastapi import FastAPI


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
