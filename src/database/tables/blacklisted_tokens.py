from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.database.mixins.int_id_pk_mixin import IntIdPkMixin
from src.database.mixins.created_updated_at_mixin import TimestampMixin

from src.database.tables.base import Base


class BlacklistedToken(Base, IntIdPkMixin, TimestampMixin):
    """Таблица для черного списка токенов (деактивированные токены)"""

    jti: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    """ JWT ID - уникальный идентификатор токена """

    token_type: Mapped[str] = mapped_column(String(50), nullable=False)
    """ Тип токена (access, refresh) """

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    """ ID пользователя, которому принадлежал токен """

    expires_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    """ Время истечения токена в Unix timestamp (секунды от epoch) """

    # Связь с пользователем
    user: Mapped["User"] = relationship(
        "User", back_populates="blacklisted_tokens", passive_deletes=True
    )


if TYPE_CHECKING:
    from src.database.tables.users import User
