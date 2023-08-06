"""Настройки журналирования серверной части приложения"""

import sys
import os

import logging.handlers

from common.settings import LOGGING_LEVEL

sys.path.append('../')

# Создаём формировщик логов (formatter):
SERVER_FORMATTER = logging.Formatter("%(asctime)s %(levelname)s "
                                     "%(module)s %(message)s")

# Подготовка имени файла для логирования:
# PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.getcwd()
PATH = os.path.join(PATH, 'server.log')

# Создаём потоки вывода логов:
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(SERVER_FORMATTER)
STREAM_HANDLER.setLevel(logging.ERROR)
FILE_HANDLER = logging.handlers.TimedRotatingFileHandler(PATH, interval=1,
                                                         when='d',
                                                         encoding='utf-8')
FILE_HANDLER.setFormatter(SERVER_FORMATTER)

# Создаём регистратор и настраиваем его:
LOGGER = logging.getLogger('server')
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(LOGGING_LEVEL)

# Отладка:
if __name__ == '__main__':
    LOGGER.critical('critical тестовый запуск')
    LOGGER.error('error тестовый запуск')
    LOGGER.warning('warning тестовый запуск')
    LOGGER.info('info тестовый запуск')
    LOGGER.debug('debug тестовый запуск')
