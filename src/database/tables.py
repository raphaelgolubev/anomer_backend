from sqlalchemy import MetaData
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr

from src.config import settings
from src.database.mixins import UuidMixin, TimestampMixin
from src.utils.case_converter import camel_case_to_snake_case


class Base(DeclarativeBase):
    __abstract__ = True
    
    metadata = MetaData(
        naming_convention=settings.db.naming_conventions
    )

    @declared_attr.directive
    def __tablename__(self) -> str:
        return f"{camel_case_to_snake_case(self.__name__)}s"


class User(Base, UuidMixin, TimestampMixin):
    """ Таблица пользователей """

    username: Mapped[str] = mapped_column(nullable=True, unique=True)
    """ Имя пользователя """