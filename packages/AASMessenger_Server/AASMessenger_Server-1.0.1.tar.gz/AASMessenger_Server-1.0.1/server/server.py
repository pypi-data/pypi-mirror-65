"""Серверная часть приложения"""

import argparse
import configparser
import os
import sys
import logging

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from common.settings import DEFAULT_PORT
from log import server_log_config
from server.core import MessageProcessor
from server.database import ServerDataBase
from server.main_window import MainWindow
from common.decos import log

# Инициализация логирования
SERVER_LOGGER = logging.getLogger('server')


@log
def args_handler(default_port, default_address):
    '''Парсер аргументов коммандной строки.'''
    SERVER_LOGGER.debug(
        f'Инициализация парсера аргументов коммандной строки: {sys.argv}')
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest='port', type=int,
                        default=default_port, nargs='?')
    parser.add_argument('-a', dest='ip', default=default_address, nargs='?')
    parser.add_argument('--no_gui', action='store_true')

    args = parser.parse_args()
    listen_address = args.ip
    listen_port = args.port
    gui_flag = args.no_gui

    SERVER_LOGGER.debug('Аргументы успешно загружены.')

    return listen_address, listen_port, gui_flag


@log
def config_load():
    '''Парсер конфигурационного ini файла.'''
    config = configparser.ConfigParser()
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.getcwd()
    config.read(f"{dir_path}/{'server.ini'}")
    # Если конфиг файл загружен правильно, запускаемся,
    # иначе конфиг по умолчанию.
    if 'SETTINGS' in config:
        return config
    else:
        config.add_section('SETTINGS')
        config.set('SETTINGS', 'Default_port', str(DEFAULT_PORT))
        config.set('SETTINGS', 'Listen_Address', '')
        config.set('SETTINGS', 'Database_path', '')
        config.set('SETTINGS', 'Database_file', 'server_database.db3')
        return config


@log
def main():
    '''Запуск серверного приложения'''
    # Загрузка файла конфигурации сервера:
    config = config_load()

    # Загрузка параметров командной строки, если нет параметров,
    # то задаём значения по умоланию:
    listen_address, listen_port, gui_flag = args_handler(
        config['SETTINGS']['Default_port'],
        config['SETTINGS']['Listen_Address'])

    # Инициализация базы данных
    database = ServerDataBase(
        os.path.join(
            config['SETTINGS']['Database_path'],
            config['SETTINGS']['Database_file']))

    # Создание экземпляра класса - сервера и его запуск:
    server = MessageProcessor(listen_address, listen_port, database)
    server.deamon = True
    server.start()

    # Если  указан параметр без GUI то запускаем обработчик
    # консольного ввода:
    if gui_flag:
        while True:
            command = input('Введите exit для завершения работы сервера.')
            # Если выход, то завршаем основной цикл сервера:
            if command == 'exit':
                server.running = False
                server.join()
                break

    # Если не указан запуск без GUI, то запускаем GUI:
    else:
        server_app = QApplication(sys.argv)
        server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
        main_window = MainWindow(database, server, config)

        # Запускаем GUI:
        server_app.exec_()

        # По закрытию окон останавливаем обработчик сообщений:
        server.running = False


if __name__ == '__main__':
    main()
