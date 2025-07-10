from datetime import datetime
from uuid import UUID as UuidType

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID as UuidColumn
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import FunctionElement
from sqlalchemy.orm import Mapped, mapped_column


class utcnow(FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('Europe/Moscow', CURRENT_TIMESTAMP)"


class UuidMixin:
    id: Mapped[UuidType] = mapped_column(
        UuidColumn(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=func.gen_random_uuid(),
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=utcnow(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        index=True,
        server_default=utcnow(),
        server_onupdate=utcnow(),
    )