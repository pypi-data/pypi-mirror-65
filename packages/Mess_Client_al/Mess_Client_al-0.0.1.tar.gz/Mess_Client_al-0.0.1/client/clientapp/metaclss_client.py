import dis


class ClientVerifier(type):
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
                        if i.argval == ('socket' or 'accept' or 'listen'):
                            # проверка на отсутствие вызовов accept и listen для сокетов;
                            # проверка на отсутствие создания сокетов на уровне классов
                            raise TypeError('В классе обнаружено использование запрещённого метода')
                        elif i.argval not in methods:
                            methods.append(i.argval)

        if ('send_message' or 'get_message') not in methods:
            # проверка на использование сокетов для работы по TCP;
            raise TypeError('Отсутствуют вызовы функций, работающих с сокетами.')

        super().__init__(cls_name, bases, cls_dict)
