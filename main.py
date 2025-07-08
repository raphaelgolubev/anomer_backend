import uvicorn

from src.config import settings


def main():
    uvicorn.run(
        app="src.app:main_app",
        host=settings.server.host,
        port=settings.server.port,
        lifespan="on",
        reload=True
    )


if __name__ == "__main__":
    main()
