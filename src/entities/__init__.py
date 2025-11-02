from enum import Enum


class DeviceType(Enum):
    MOBILE = "MOBILE"
    """ Мобильное устройство """

    DESKTOP = "DESKTOP"
    """ Настольное устройство """
    
    WEB = "WEB"
    """ Веб-сайт """


class UserStatus(Enum):
    CREATED = "CREATED"
    """ Пользователь создан """

    WAIT_ACTIVATION = "WAIT_ACTIVATION"
    """ В процессе подтверждения """

    ACTIVATED = "ACTIVATED"
    """ Пользователь подтвердил эл. почту """

    BANNED = "BANNED"
    """ Пользователь забанен """


class UserRole(Enum):
    USER = "USER"
    """ Обычный пользователь """

    ADMIN = "ADMIN"
    """ Администратор """

    MODERATOR = "MODERATOR"
    """ Модератор """
