import logging
import sys
import socket

# sys.path.append('../')


# проверка - логи клиента или сервера
if sys.argv[0].find('client.py') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')


def func_to_log(func):
    """Функция-декоратор"""
    def log_saver(*args, **kwargs):
        LOGGER.debug(f'Function {func.__name__} called from {func.__module__}')
        return func(*args, **kwargs)
    return log_saver


# Функция проверки, что клиент авторизован на сервере
# Проверяет, что передаваемый объект сокета находится в списке клиентов. Если его там нет закрывает сокет
def login_required(func):
    """Функция-декоратор"""
    def checker(*args, **kwargs):
        # Если первый аргумент - экземпляр Server, a сокет в остальных аргументах
        # Импортить необходимо тут, иначе ошибка рекурсивного импорта.
        from server import Server
        from config.settings import REGISTRATION, ACTION, PRESENCE
        if isinstance(args[0], Server):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    # Проверяем, что данный сокет есть в списке names класса Server
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True

            # Теперь надо проверить, что передаваемые аргументы не presence сообщение и не регистрация
            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and (arg[ACTION] == PRESENCE or arg[ACTION] == REGISTRATION):
                        found = True
            # Если не авторизован и не сообщение начала авторизации, то вызываем исключение.
            if not found:
                raise TypeError

        return func(*args, **kwargs)

    return checker
