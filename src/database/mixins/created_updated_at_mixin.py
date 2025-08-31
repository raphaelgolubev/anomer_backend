from datetime import datetime, timezone
from typing import Union

from sqlalchemy import Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import FunctionElement


class unix_timestamp(FunctionElement):
    type = Integer()
    inherit_cache = True


@compiles(unix_timestamp, "postgresql")
def pg_unix_timestamp(element, compiler, **kw):
    return "EXTRACT(EPOCH FROM NOW())::INTEGER"


class TimestampMixin:
    """
    Миксин для добавления полей created_at и updated_at в Unix timestamp формате.
    """
    
    created_at: Mapped[int] = mapped_column(
        BigInteger, 
        nullable=False, 
        server_default=unix_timestamp(),
        comment="Unix timestamp создания записи (секунды от epoch)"
    )
    updated_at: Mapped[int] = mapped_column(
        BigInteger,
        nullable=True,
        index=True,
        server_default=unix_timestamp(),
        server_onupdate=unix_timestamp(),
        comment="Unix timestamp последнего обновления записи (секунды от epoch)"
    )
    
    @property
    def created_at_datetime(self) -> datetime:
        """Возвращает created_at как datetime объект в UTC"""
        return datetime.fromtimestamp(self.created_at, tz=timezone.utc)
    
    @property
    def updated_at_datetime(self) -> Union[datetime, None]:
        """Возвращает updated_at как datetime объект в UTC или None"""
        if self.updated_at is None:
            return None
        return datetime.fromtimestamp(self.updated_at, tz=timezone.utc)
    
    def to_dict_with_datetime(self) -> dict:
        """Возвращает словарь с datetime полями для API"""
        result = {}
        for key, value in self.__dict__.items():
            if key in ['created_at', 'updated_at'] and value is not None:
                # Добавляем оба варианта: timestamp и datetime
                result[f"{key}_timestamp"] = value
                result[f"{key}_datetime"] = datetime.fromtimestamp(value, tz=timezone.utc).isoformat()
            else:
                result[key] = value
        return result
