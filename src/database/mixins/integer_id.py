from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class IntIdPkMixin:
    id: Mapped[int] = mapped_column(
        BigInteger, 
        autoincrement="auto", 
        primary_key=True
    )
