from datetime import datetime, timezone

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.database.pg_func import unix_timestamp


class LastSeen:
    """
    Миксин для добавления поля `last_seen` в Unix timestamp формате.
    """
    
    last_seen: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default=unix_timestamp()
    )
    
    @property
    def last_seen_datetime(self) -> datetime:
        """Возвращает last_seen как datetime объект в UTC"""
        return datetime.fromtimestamp(self.last_seen, tz=timezone.utc)