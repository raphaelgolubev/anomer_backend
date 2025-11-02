from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.entities import UserStatus, UserRole
from src.database.tables.base import Base

import src.database.mixins as mixins



class User(Base, mixins.IntIDMixin, mixins.CreatedAt, mixins.UpdatedAt):
    """ Таблица пользователей """

    username: Mapped[str] = mapped_column(nullable=True, unique=True)
    """ Имя пользователя """

    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    """ Электронная почта """

    password: Mapped[str] = mapped_column(nullable=False)
    """ Хэшированный пароль """

    role: Mapped[UserRole] = mapped_column(
        nullable=False, default=UserRole.USER, server_default=UserRole.USER.value
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
        passive_deletes=True,
    )


if TYPE_CHECKING:
    from src.database.tables.blacklisted_tokens import BlacklistedToken
