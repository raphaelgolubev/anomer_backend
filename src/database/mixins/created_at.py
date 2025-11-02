from datetime import datetime, timezone

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.database.pg_func import unix_timestamp


class CreatedAt:
    """
    Миксин для добавления поля `created_at` в Unix timestamp формате.
    """
    
    created_at: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default=unix_timestamp()
    )
    
    @property
    def created_at_datetime(self) -> datetime:
        """Возвращает created_at как datetime объект в UTC"""
        return datetime.fromtimestamp(self.created_at, tz=timezone.utc)