import logging
import sys
import ipaddress
import socket


SERVER_LOGGER = logging.getLogger('server')


class ServerPort:
    '''
    Класс - дескриптор для номера порта.
    Позволяет использовать только порты с 1023 по 65536.
    При попытке установить неподходящий номер порта генерирует исключение.
    '''
    def __set__(self, instance, port):
        if not 1023 < port < 65535:
            SERVER_LOGGER.critical(f'Попытка запуска с неподходящим номером '
                                   f'порта: {port}. Номер порта должен '
                                   f'находиться в диапозоне от 1024 до 65535')
            raise TypeError('Некорректный номер порта')

        instance.__dict__[self.port] = port

    def __set_name__(self, owner, port):
        self.port = port


class ServerAddress:
    '''
    Класс - дескриптор для ip адреса.
    Позволяет использовать только ip адреса или имя хоста.
    При попытке ввода неподходящего адреса генерирует исключение.
    '''
    def __set__(self, instance, value):
        try:
            ipaddress.ip_address(socket.gethostbyname(value))
        except socket.gaierror:
            SERVER_LOGGER.critical(f'Попытка запуска с неккоректным '
                                   f'ip адресом: {value}')
            sys.exit(1)

        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
