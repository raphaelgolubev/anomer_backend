from sqlalchemy import MetaData
from sqlalchemy.orm import Mapped, DeclarativeBase, declared_attr, mapped_column

from src.config import settings
from src.database.mixins import UuidMixin, TimestampMixin
from src.utils.case_converter import camel_case_to_snake_case


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

    role: Mapped[str] = mapped_column(nullable=False, default="USER")
