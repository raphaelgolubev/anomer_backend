from typing import Union
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, ProgrammingError
from pydantic import ValidationError as PydanticValidationError

from .http_exceptions import CustomHTTPException, DatabaseError, ValidationError


async def custom_http_exception_handler(
    request: Request, exc: CustomHTTPException
) -> JSONResponse:
    """
    Обработчик для кастомных HTTP исключений.
    Возвращает структурированный JSON ответ с дополнительной информацией.
    """
    return JSONResponse(
        status_code=exc.status_code, content=exc.to_dict(), headers=exc.headers
    )


async def validation_exception_handler(
    request: Request, exc: Union[RequestValidationError, PydanticValidationError]
) -> JSONResponse:
    """
    Обработчик для ошибок валидации Pydantic.
    Преобразует ошибки валидации в структурированный формат.
    """
    field_errors = {}

    for error in exc.errors():
        field_name = " -> ".join(str(loc) for loc in error["loc"])
        field_errors[field_name] = error["msg"]

    custom_error = ValidationError(field_errors=field_errors)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=custom_error.to_dict()
    )


async def sqlalchemy_exception_handler(
    request: Request, exc: SQLAlchemyError
) -> JSONResponse:
    """
    Обработчик для ошибок SQLAlchemy.
    Преобразует ошибки БД в структурированный формат.
    """
    # Логируем оригинальную ошибку для отладки
    print(f"Database error: {exc}")

    if isinstance(exc, IntegrityError):
        # Ошибки целостности данных (дубликаты, нарушение внешних ключей)
        detail = "Нарушение целостности данных"
        if "duplicate key" in str(exc).lower():
            detail = "Запись уже существует"
        elif "foreign key" in str(exc).lower():
            detail = "Нарушение внешнего ключа"
    elif isinstance(exc, ProgrammingError):
        if len(exc.args) > 0:
            if "UndefinedTableError" in exc.args[0]:
                detail = "Таблица не найдена"
    else:
        detail = "Ошибка базы данных"

    custom_error = DatabaseError(original_error=detail)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=custom_error.to_dict(),
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Общий обработчик для всех необработанных исключений.
    """
    # Логируем ошибку для отладки
    print(f"Unhandled exception: {exc}")
    print(f"Request URL: {request.url}")
    print(f"Request method: {request.method}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "Необработанное исключение. Внутренняя ошибка сервера",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "error_code": "UNHANDLED_INTERNAL_SERVER_ERROR",
        },
    )


def register_exception_handlers(app):
    """
    Регистрирует все обработчики исключений в FastAPI приложении.

    Args:
        app: FastAPI приложение
    """
    from sqlalchemy.exc import SQLAlchemyError

    # Регистрируем обработчики
    app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(PydanticValidationError, validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
