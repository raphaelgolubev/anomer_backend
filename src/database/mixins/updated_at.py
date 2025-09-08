from datetime import datetime, timezone
from typing import Union
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.database.pg_func import unix_timestamp


class UpdatedAt:
    """
    Миксин для добавления поля updated_at в Unix timestamp формате.
    """
    
    updated_at: Mapped[int] = mapped_column(
        BigInteger,
        nullable=True,
        index=True,
        server_default=unix_timestamp(),
        server_onupdate=unix_timestamp(),
    )
    
    @property
    def updated_at_datetime(self) -> Union[datetime, None]:
        """Возвращает updated_at как datetime объект в UTC или None"""
        if self.updated_at is None:
            return None
        return datetime.fromtimestamp(self.updated_at, tz=timezone.utc)