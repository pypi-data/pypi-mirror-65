"""
3.	Реализовать дескриптор для класса серверного сокета, а в нем — проверку номера порта.
Это должно быть целое число (>=0). Значение порта по умолчанию равняется 7777.
Дескриптор надо создать в отдельном классе. Его экземпляр добавить в пределах класса серверного сокета.
Номер порта передается в экземпляр дескриптора при запуске сервера.
"""

import sys

import logs.server_log_config as log


class GetPort:
    def __set__(self, instance, value):
        # проверим подходящий номер порта
        if not 1023 < value < 65536:
            log.SERVER_LOG.critical(f'Attempt to start a client: port: {value}. '
                                    f'Allowed ports 1024-65535. Client closed.')
            sys.exit(1)
        # напрямую обращаемся к объекту __dict__
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        # привязать имя атрибута к дескриптору
        self.name = name
