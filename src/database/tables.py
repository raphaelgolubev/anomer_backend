from sqlalchemy import MetaData
from sqlalchemy.orm import Mapped, DeclarativeBase, declared_attr, mapped_column

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
