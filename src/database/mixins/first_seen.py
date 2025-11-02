from datetime import datetime, timezone

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.database.pg_func import unix_timestamp


class FirstSeen:
    """
    Миксин для добавления поля `first_seen` в Unix timestamp формате.
    """
    
    first_seen: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default=unix_timestamp()
    )
    
    @property
    def first_seen_datetime(self) -> datetime:
        """Возвращает first_seen как datetime объект в UTC"""
        return datetime.fromtimestamp(self.first_seen, tz=timezone.utc)