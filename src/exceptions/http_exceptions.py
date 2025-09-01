from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from pydantic import BaseModel
from src.exceptions import ErrorCode
import src.exceptions.error_codes as error_code
        

class CustomHTTPException(HTTPException):
    """
    Базовый класс для кастомных HTTP исключений.
    Расширяет стандартный HTTPException с дополнительными возможностями.
    """
    
    def __init__(
        self,
        error_code: ErrorCode,
        model: BaseModel = None,
        headers: Optional[Dict[str, str]] = None,
        additional_data: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=error_code.http_code, 
            detail=error_code.message, 
            headers=headers
        )
        self.model_dict = model.model_dump() if model else {}
        self.error_code = error_code
        self.additional_data = additional_data or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Возвращает исключение в виде словаря для JSON ответа."""
        to_return = {}
        
        if self.model_dict:
            to_return = self.model_dict.copy()
            
        if self.additional_data:
            to_return.update(self.additional_data)

        to_return.update(error_code=self.error_code.exception_code)
            
        return to_return

# === ОШИБКИ БАЗЫ ДАННЫХ ===

class DatabaseError(CustomHTTPException):
    """Ошибка базы данных."""
    
    def __init__(self, original_error: Optional[str] = None):
        super().__init__(
            error_code=ErrorCode(status.HTTP_500_INTERNAL_SERVER_ERROR, "DATABASE_ERROR"),
            additional_data={"original_error": original_error}
        )


# === ОШИБКИ ВАЛИДАЦИИ ===

class ValidationError(CustomHTTPException):
    """Ошибка валидации данных."""
    
    def __init__(self, field_errors: Optional[Dict[str, str]] = None):
        super().__init__(
            error_code=ErrorCode(status.HTTP_422_UNPROCESSABLE_ENTITY, "VALIDATION_ERROR"),
            additional_data={"field_errors": field_errors}
        )


# === ОШИБКИ ОГРАНИЧЕНИЙ ===

class RateLimitExceededError(CustomHTTPException):
    """Превышен лимит запросов."""
    
    def __init__(self, retry_after: Optional[int] = None):
        headers = {"Retry-After": str(retry_after)} if retry_after else None
        
        super().__init__(
            error_code=ErrorCode(status.HTTP_429_TOO_MANY_REQUESTS, "RATE_LIMIT_EXCEEDED"),
            headers=headers,
            additional_data={"retry_after": retry_after}
        )
