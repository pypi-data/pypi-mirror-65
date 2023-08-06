import sys
import logging
import socket

sys.path.append('../')

# Метод определения модуля, источника запуска:
if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')


def log(func_for_log):
    '''
    Декоратор, выполняющий логирование вызовов функций.
    Сохраняет события типа debug, содержащие
    информацию о имени вызываемой функиции, параметры с которыми
    вызывается функция, и модуль, вызывающий функцию.
    '''

    def log_create(*args, **kwargs):
        res = func_for_log(*args, **kwargs)
        LOGGER.debug(f'Вызвана функция {func_for_log.__name__} с параматреми '
                     f'{args}, {kwargs}. Вызов из модуля '
                     f'{func_for_log.__module__}')
        return res

    return log_create


def login_required(func):
    '''
    Декоратор, проверяющий, что клиент авторизован на сервере.
    Проверяет, что передаваемый объект сокета находится в
    списке авторизованных клиентов.
    За исключением передачи словаря-запроса
    на авторизацию. Если клиент не авторизован,
    генерирует исключение TypeError
    '''
    def checker(*args, **kwargs):
        # Проверяем, что первый аргумент - экземпляр MessageProcessor
        # Импортировать необходимо тут, иначе ошибка рекурсивного импорта.
        from server.server.core import MessageProcessor
        from server.common.settings import ACTION, PRESENCE
        if isinstance(args[0], MessageProcessor):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    # Проверяем, что данный сокет есть в списке names
                    # класса MessageProcessor
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True

            # Теперь надо проверить, что передаваемые аргументы
            # не presence сообщение
            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        found = True
            # Если не авторизован и не сообщение начала авторизации,
            # то вызываем исключение.
            if not found:
                raise TypeError

        return func(*args, **kwargs)

    return checker
