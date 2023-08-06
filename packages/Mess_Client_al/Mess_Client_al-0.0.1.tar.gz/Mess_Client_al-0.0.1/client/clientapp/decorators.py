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
