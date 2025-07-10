from uuid import UUID as UuidType

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as UuidColumn


class UuidMixin:
    id: Mapped[UuidType] = mapped_column(
        UuidColumn(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=func.gen_random_uuid(),
    )