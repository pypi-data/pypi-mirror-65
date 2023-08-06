# Создание именованного логгера;
# Сообщения лога должны иметь следующий формат: "<дата-время> <уровеньважности> <имямодуля> <сообщение>";
# Журналирование должно производиться в лог-файл;

# Журналирование обработки исключений try/except.
# Вместо функции print() использовать журналирование и обеспечить вывод служебных сообщений в лог-файл;
# Журналирование функций, исполняемых на серверной и клиентской сторонах при работе мессенджера.

import logging
import os
import sys

from config.settings import LOG_DIR, CLIENT_LOG_FILE, ENCODING, LOGGING_LEVEL
sys.path.append('../')

# Определить формат сообщений
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(filename)s: %(message)s")

# Создать регистратор верхнего уровня с именем 'client'
CLIENT_LOG = logging.getLogger('client')
CLIENT_LOG.setLevel(LOGGING_LEVEL)
CLIENT_LOG.propagate = False

# Создать несколько обработчиков
FILE_PATH = os.path.join(LOG_DIR, CLIENT_LOG_FILE)
# STREAM_HANDLER = logging.StreamHandler(sys.stderr)
FILE_HANDLER = logging.FileHandler(FILE_PATH, encoding=ENCODING)
FILE_HANDLER.setFormatter(formatter)

# Добавить несколько обработчиков в регистратор 'client'
CLIENT_LOG.addHandler(FILE_HANDLER)
# CLIENT_LOG.addHandler(STREAM_HANDLER)

if __name__ == '__main__':
    CLIENT_LOG.debug(f'Test debug')
    CLIENT_LOG.info('Test info')
    CLIENT_LOG.warning('Test warning')
    CLIENT_LOG.error('Test error')
    CLIENT_LOG.critical('Test critical')

