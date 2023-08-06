import sys  # sys нужен для передачи argv в QApplication
import time

from socket import AF_INET, SOCK_STREAM, socket
from PyQt5.QtWidgets import QMainWindow, QApplication

import clientapp.client_gui_login as design
from clientapp.client_chat_window import ClientApp
from config.utils import send_message, get_message
from clientapp.database_client import ClientDB
from clientapp.decorators import func_to_log
from logs.client_log_config import CLIENT_LOG as log
from config.settings import DEFAULT_HOST, DEFAULT_PORT, ACTION, PRESENCE, TIME, USER, SENDER, RESPONSE, ERROR, \
    GET_CONTACTS, CONTACTS, PASSWORD, REGISTRATION


def presence_request(sock, client_name, password, request):
    """ сформировать presence-сообщение, отправить его и получить ответ от сервера """
    presence = {
        ACTION: request,
        TIME: time.time(),
        USER: {
            SENDER: client_name,
            PASSWORD: password
        }
    }
    log.debug(f'{client_name}: Presence message created')

    send_message(sock, presence)
    log.debug(f'{client_name}: Presence message send')

    ans = get_message(sock)
    log.debug(f'For presence get answer: {ans}')

    return ans


@func_to_log
def contacts_list_request(sock, client_name):
    message = {
        ACTION: GET_CONTACTS,
        TIME: time.time(),
        SENDER: client_name
    }
    log.debug(f'{client_name}: contacts_list_request created')

    send_message(sock, message)
    log.debug(f'{client_name}: contacts_list_request send')

    ans = get_message(sock)
    contacts = ans[CONTACTS]
    log.debug(f'For contacts_list_request get answer: {ans}')

    return contacts


class StartClient(QMainWindow, design.Ui_Dialog_login):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.server_host, self.server_port = DEFAULT_HOST, DEFAULT_PORT

        # self.sock = socket(AF_INET, SOCK_STREAM)

        self.line_password_2.setHidden(True)

        self.button_ok_login.clicked.connect(lambda: self.accept(PRESENCE))
        self.button_registration.clicked.connect(self.registration_form)

    def accept(self, request):
        self.client_name = self.line_login.text()
        self.password = self.line_password.text()
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((self.server_host, self.server_port))

        # self.keys = get_keys(self.client_name)
        # print('keys', self.keys)

        database = ClientDB(self.client_name)

        # Отправляем приветствие и получаем ответ от сервера
        ans = presence_request(self.sock, self.client_name, self.password, request)
        if ans[ACTION] == PRESENCE:
            if ans[RESPONSE] == 200:

                # запрашиваем список контактов у сервера и добавляем их в свою базу данных
                contacts = contacts_list_request(self.sock, self.client_name)
                database.fill_contacts(contacts)

                self.start_chat(database)
        elif ans[ACTION] == REGISTRATION:
            if ans[RESPONSE] == 200:
                # TODO win 'reg successful'
                print('reg++++')
                self.accept(PRESENCE)

        elif ans[RESPONSE] != 200:
            self.label_error.setText(ans[ERROR])
            log.error(ans[ERROR])

    def registration_form(self):
        self.button_ok_login.setHidden(True)
        self.line_password_2.setHidden(False)
        self.button_registration.clicked.connect(self.registration)

    def registration(self):
        if len(self.line_login.text()) > 0 \
                and len(self.line_password.text()) > 0 \
                and self.line_password.text() == self.line_password_2.text():
            self.accept(REGISTRATION)
        elif len(self.line_login.text()) == 0:
            self.label_error.setText('Введите логин')
        elif len(self.line_password.text()) == 0:
            self.label_error.setText('Введите пароль')
        elif len(self.line_password_2.text()) == 0:
            self.label_error.setText('Введите пароль повторно')
        else:
            self.label_error.setText('Пароли не совпадают')

    def start_chat(self, database):
        # Закрываем окно логина и запускаем окно чата
        self.close()
        self.cl_window = ClientApp(self.client_name, self.sock, database)  # Создаём объект класса ClientApp
        self.cl_window.show()

    # def reject(self):
    #     sys.exit()


# def get_keys(client_name):
#     # Загружаем ключи из файла, если же файла нет, то генерируем новую пару.
#     dir_path = os.path.dirname(os.path.realpath(__file__))
#     key_file = os.path.join(dir_path, f'{client_name}.key')
#     if not os.path.exists(key_file):
#         keys = RSA.generate(2048, os.urandom)
#         with open(key_file, 'wb') as key:
#             key.write(keys.export_key())
#     else:
#         with open(key_file, 'rb') as key:
#             keys = RSA.import_key(key.read())
#
#     return keys.publickey().export_key()


def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    window = StartClient()  # Создаём объект класса StartClient
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
