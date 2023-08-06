# Создание именованного логгера;
# Сообщения лога должны иметь следующий формат: "<дата-время> <уровеньважности> <имямодуля> <сообщение>";
# Журналирование должно производиться в лог-файл;
# На стороне сервера необходимо настроить ежедневную ротацию лог-файлов.

# Журналирование обработки исключений try/except. Вместо функции print() использовать журналирование
# и обеспечить вывод служебных сообщений в лог-файл;
# Журналирование функций, исполняемых на серверной и клиентской сторонах при работе мессенджера.

import logging.handlers
import os
import sys

from config.settings import LOG_DIR, SERVER_LOG_FILE, ENCODING, LOGGING_LEVEL
sys.path.append('../')

# Определить формат сообщений
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(filename)s: %(message)s")

# Создать регистратор верхнего уровня с именем 'client'
SERVER_LOG = logging.getLogger('server')
SERVER_LOG.setLevel(LOGGING_LEVEL)
SERVER_LOG.propagate = False

# Создать несколько обработчиков
FILE_PATH = os.path.join(LOG_DIR, SERVER_LOG_FILE)
# STREAM_HANDLER = logging.StreamHandler(sys.stderr)
LOG_FILE = logging.handlers.TimedRotatingFileHandler(FILE_PATH, when='D', interval=1, encoding=ENCODING)
LOG_FILE.setFormatter(formatter)

# Добавить несколько обработчиков в регистратор 'client'
SERVER_LOG.addHandler(LOG_FILE)
# SERVER_LOG.addHandler(STREAM_HANDLER)

if __name__ == '__main__':
    SERVER_LOG.debug(f'Test debug')
    SERVER_LOG.info('Test info')
    SERVER_LOG.warning('Test warning')
    SERVER_LOG.error('Test error')
    SERVER_LOG.critical('Test critical')
