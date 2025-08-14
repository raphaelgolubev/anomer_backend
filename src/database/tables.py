from datetime import datetime

from sqlalchemy import String, DateTime, MetaData, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
    relationship,
    declared_attr,
    mapped_column,
)

from src.config import settings
from src.utils.case_converter import camel_case_to_snake_case
from src.database.mixins.uuid_id_pk_mixin import UuidMixin
from src.database.mixins.created_updated_at_mixin import TimestampMixin


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(naming_convention=settings.db.naming_conventions)

    @declared_attr.directive
    def __tablename__(self) -> str:
        return f"{camel_case_to_snake_case(self.__name__)}s"


class User(Base, UuidMixin, TimestampMixin):
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

    is_email_verified: Mapped[bool] = mapped_column(
        nullable=False, default=False, server_default="FALSE"
    )
    """ Флаг, указывающий подтвердил ли пользователь электронную почту """

    # Связь с деактивированными токенами
    blacklisted_tokens: Mapped[list["BlacklistedToken"]] = relationship(
        "BlacklistedToken", back_populates="user", cascade="all, delete-orphan"
    )


class BlacklistedToken(Base, UuidMixin, TimestampMixin):
    """Таблица для черного списка токенов (деактивированные токены)"""

    jti: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    """ JWT ID - уникальный идентификатор токена """

    token_type: Mapped[str] = mapped_column(String(50), nullable=False)
    """ Тип токена (access, refresh) """

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    """ ID пользователя, которому принадлежал токен """

    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    """ Время истечения токена (для автоматической очистки) """

    # Связь с пользователем
    user: Mapped["User"] = relationship("User", back_populates="blacklisted_tokens")
