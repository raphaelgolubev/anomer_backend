from uuid import UUID as UuidType, uuid4

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as UuidColumn


class UuidIDMixin:
    """ Миксин для добавления поля `id` в UUID формате """
    
    id: Mapped[UuidType] = mapped_column(
        UuidColumn(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid4,
        index=True,
        server_default=func.gen_random_uuid(),
    )
