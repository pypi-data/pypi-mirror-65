"""Декораторы"""

import traceback
import logging
from socket import socket

import logs.config_server_log
import logs.config_client_log


class Log:
    """Декоратор логирования"""
    def __init__(self, script_name):
        self.script_name = script_name

    def __call__(self, func):

        LOGGER = logging.getLogger(self.script_name)

        def log_saver(*args, **kwargs):
            res = func(*args, **kwargs)
            LOGGER.debug(
                f'\tБыла вызвана функция {func.__name__} c параметрами {args}, {kwargs}.\n'
                f'\tВызов из модуля {func.__module__}.{"/".join([i.name for i in traceback.extract_stack()[1:]])} \n'
                f'\tФункция вернула {res}\n'
            )

            return res
        return log_saver


def login_required(func):
    """Декоратор проверки что пользователь зарегестрирован"""
    def checker(*args, **kwargs):
        from server.core import MessageProcessor
        from system.config import ACTION, PRESENCE
        if isinstance(args[0], MessageProcessor):
            found = False
            for arg in args:
                if isinstance(arg, socket):
                    # Проверяем, что данный сокет есть в списке names класса MessageProcessor
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True

            # Теперь надо проверить, что передаваемые аргументы не presence сообщение
            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        found = True
            # Если не не авторизован и не сообщение начала авторизации, то вызываем исключение.
            if not found:
                raise TypeError

        return func(*args, **kwargs)

    return checker