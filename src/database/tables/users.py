from typing import TYPE_CHECKING
from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column,
)

from src.database.mixins.int_id_pk_mixin import IntIdPkMixin
from src.database.mixins.created_updated_at_mixin import TimestampMixin

from src.database.tables.base import Base

from src.entities import UserStatus


class User(Base, IntIdPkMixin, TimestampMixin):
    """Таблица пользователей"""

    username: Mapped[str] = mapped_column(nullable=True, unique=True)
    """ Имя пользователя """

    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    """ Электронная почта """

    password: Mapped[str] = mapped_column(nullable=False)
    """Хэшированный пароль"""

    role: Mapped[str] = mapped_column(
        nullable=False, default="USER", server_default="USER"
    )
    """ Уровень доступа """

    status: Mapped[UserStatus] = mapped_column(
        nullable=False,
        default=UserStatus.CREATED,
        server_default=UserStatus.CREATED.value,
    )
    """ Статус пользователя """

    # Связь с деактивированными токенами
    blacklisted_tokens: Mapped[list["BlacklistedToken"]] = relationship(
        "BlacklistedToken", 
        back_populates="user", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )


if TYPE_CHECKING:
    from src.database.tables.blacklisted_tokens import BlacklistedToken