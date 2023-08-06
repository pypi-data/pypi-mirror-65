"""Клиентская часть приложения"""

import argparse
import os
import sys
import logging

from Crypto.PublicKey import RSA
from PyQt5.QtWidgets import QApplication, QMessageBox

from common.settings import DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.decos import log
from common.errors import ServerError
from client.database import ClientDatabase
from client.transport import ClientTransport
from client.main_window import ClientMainWindow
from client.start_dialog import UserNameDialog

# Инициализация клиентского логера:
CLIENT_LOGGER = logging.getLogger('client')


# Парсер аргументов коммандной строки
@log
def args_handler():
    '''
    Парсер аргументов командной строки, возвращает кортеж из 4 элементов
    адрес сервера, порт, имя пользователя, пароль.
    Выполняет проверку на корректность номера порта.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', type=int, default=DEFAULT_PORT, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    parser.add_argument('-p', '--password', default='', nargs='?')

    args = parser.parse_args()
    server_address = args.addr
    server_port = args.port
    client_name = args.name
    client_passwd = args.password

    # Проверим подходит ли номер порта:
    if not 1023 < server_port < 65535:
        CLIENT_LOGGER.critical(f'Попытка запуска с неподходящим номером '
                               f'порта: {server_port}. Номер порта должен '
                               f'находиться в диапозоне от 1024 до 65535')
        exit(1)

    return server_address, server_port, client_name, client_passwd


# Основная функция клиента
if __name__ == '__main__':
    print('Консольный мессенджер. Клиентский модуль')

    # Загружаем параметы коммандной строки:
    server_address, server_port, client_name, client_passwd = args_handler()

    # Создаём клиентокое приложение
    client_app = QApplication(sys.argv)

    # Если имя пользователя не было указано в командной строке,
    # то запросим его:
    start_dialog = UserNameDialog()

    if not client_name or not client_passwd:
        client_app.exec_()
        # Если пользователь ввёл имя и нажал ОК, то сохраняем ведённое и
        # удаляем объект, иначе выходим:
        if start_dialog.ok_pressed:
            client_name = start_dialog.client_name.text()
            client_passwd = start_dialog.client_passwd.text()
        else:
            exit(0)

    CLIENT_LOGGER.info(f'Клиент запущен с параметрами: '
                       f'IP сервера: {server_address}, '
                       f'порт  сервера: {server_port}, '
                       f'имя пользователя {client_name}')

    # Загружаем ключи с файла, если же файла нет, то генерируем новую пару:
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.getcwd()
    key_file = os.path.join(dir_path, f'{client_name}.key')
    if not os.path.exists(key_file):
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            key.write(keys.export_key())
    else:
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())

    keys.publickey().export_key()
    # Создаём объект базы данных
    database = ClientDatabase(client_name)
    # Создаём объект - транспорт и запускаем транспортный поток:
    try:
        transport = ClientTransport(
            server_port,
            server_address,
            database,
            client_name,
            client_passwd,
            keys)
    except ServerError as error:
        message = QMessageBox()
        message.critical(start_dialog, 'Ошибка сервера', error.text)
        exit(1)
    transport.setDaemon(True)
    transport.start()

    # Удалим объект диалога за ненадобностью
    del start_dialog

    # Создаём GUI
    main_window = ClientMainWindow(database, transport, keys)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Messenger - alpha release - {client_name}')
    client_app.exec_()

    # Раз графическая оболочка закрылась, закрываем транспорт
    transport.transport_shutdown()
    transport.join()
