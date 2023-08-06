import dis


class ServerVerifier(type):
    def __init__(cls, cls_name, bases, cls_dict):
        methods = []
        for func in cls_dict:
            try:
                operations = dis.get_instructions(cls_dict[func])
            except TypeError:
                pass
            else:
                for i in operations:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)

                if len(methods) > 0:
                    if 'connect' in methods:
                        # проверка на отсутствие вызовов connect для сокетов;
                        raise TypeError('Использование метода connect недопустимо в серверном классе')
                    if ('SOCK_STREAM' and 'AF_INET') not in methods:
                        # проверка на отсутствие вызовов connect для сокетов;
                        raise TypeError('Некорректная инициализация сокета.')

        super().__init__(cls_name, bases, cls_dict)
