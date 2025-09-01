from enum import Enum


class UserStatus(Enum):
    CREATED = "CREATED"
    """ Пользователь создан """

    WAIT_ACTIVATION = "WAIT_ACTIVATION"
    """ В процессе подтверждения """

    ACTIVATED = "ACTIVATED"
    """ Пользователь подтвердил эл. почту """

    BANNED = "BANNED"
    """ Пользователь забанен """
