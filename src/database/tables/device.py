from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.database.tables import Base

from src.entities import DeviceType

import src.database.mixins as mixins


class Device(Base, mixins.UuidIDMixin, mixins.FirstSeen, mixins.LastSeen, mixins.CreatedAt, mixins.UpdatedAt):
    """ Таблица, содержащая информацию об устройствах пользователей """

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    """ ID пользователя, которому принадлежит устройство """

    device_type: Mapped[DeviceType | None] = mapped_column()
    """ Тип устройства """
    
    brand: Mapped[str | None] = mapped_column()
    """ Марка устройства """
    
    model: Mapped[str | None] = mapped_column()
    """ Модель устройства """
    
    platform_name: Mapped[str | None] = mapped_column()
    """ Название платформы устройства """
    
    platform_version: Mapped[str | None] = mapped_column()
    """ Версия платформы устройства """
    
    browser_name: Mapped[str | None] = mapped_column()
    """ Название браузера устройства """
    
    browser_version: Mapped[str | None] = mapped_column()
    """ Версия браузера устройства """
    
    app_name: Mapped[str | None] = mapped_column()
    """ Название приложения устройства """
    
    app_version: Mapped[str | None] = mapped_column()
    """ Версия приложения устройства """
    
    app_build: Mapped[str | None] = mapped_column()
    """ Версия сборки приложения устройства """
    
    is_trusted: Mapped[bool] = mapped_column(default=False)
    """ Является ли устройство доверенным """
    
    # Связь с пользователем
    user: Mapped["User"] = relationship(
        "User", back_populates="devices", passive_deletes=True
    )
    

class DeviceSession(Base, mixins.UuidIDMixin, mixins.CreatedAt, mixins.UpdatedAt):
    """ Таблица, содержащая информацию о сессиях устройств пользователей """
    
    device_id: Mapped[str] = mapped_column(
        ForeignKey("devices.id", ondelete="CASCADE"), nullable=False
    )
    """ ID устройства, которому принадлежит сессия """
    
    ip_address: Mapped[str | None] = mapped_column()
    """ IP-адрес сессии """
    
    user_agent: Mapped[str | None] = mapped_column()
    """ User-Agent сессии """
    
    # Связь с устройством
    device: Mapped["Device"] = relationship(
        "Device", back_populates="sessions", passive_deletes=True
    )
    
    # Связь с пользователем
    user: Mapped["User"] = relationship(
        "User", back_populates="sessions", passive_deletes=True
    )


if TYPE_CHECKING:
    from src.database.tables.users import User
