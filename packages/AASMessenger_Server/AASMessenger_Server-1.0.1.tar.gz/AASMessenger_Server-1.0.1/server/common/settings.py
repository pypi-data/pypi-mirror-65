"""Настройки по умолчанию"""

import logging

# Порт по умолчанию
DEFAULT_PORT = 7777
# IP адрес для подключения по умолчанию
DEFAULT_IP_ADDRESS = '127.0.0.1'
# Максимальная очередь подключения клиента
MAX_CONNECTIONS = 5
# Максимальная длина сообщения в байтах
MAX_PACKAGE_LENGTH = 10240
# Кодировка проекта
ENCODING = 'utf-8'
# Текущий уровень логирования
LOGGING_LEVEL = logging.DEBUG
# База данных для хранения данных сервера
SERVER_CONFIG = 'server.ini'

# Потокол JIM. Основные ключи
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
DESTINATION = 'to'
DATA = 'bin'
PUBLIC_KEY = 'pubkey'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'msg_text'
EXIT = 'exit'
GET_CONTACTS = 'get_contacts'
LIST_INFO = 'data_list'
REMOVE_CONTACT = 'remove'
ADD_CONTACT = 'add'
USERS_REQUEST = 'get_users'
PUBLIC_KEY_REQUEST = 'pubkey_need'

# Словари с ответами
# 200
RESPONSE_200 = {RESPONSE: 200}
# 202
RESPONSE_202 = {
    RESPONSE: 202,
    LIST_INFO: None
}
# 400
RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None
}
# 205
RESPONSE_205 = {
    RESPONSE: 205
}

# 511
RESPONSE_511 = {
    RESPONSE: 511,
    DATA: None
}


