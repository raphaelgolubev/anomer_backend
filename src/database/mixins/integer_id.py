from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class IntIDMixin:
    """ Миксин для добавления поля `id` в целочисленном формате """
    
    id: Mapped[int] = mapped_column(
        BigInteger, 
        autoincrement="auto", 
        primary_key=True,
        index=True,
    )
