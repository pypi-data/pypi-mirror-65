import json
import time

from config.settings import ENCODING, MAX_PACKAGE_LENGTH
from clientapp.decorators import func_to_log


@func_to_log
def get_message(sock):
    """ загрузка ответа, если он в формате json """
    data = sock.recv(MAX_PACKAGE_LENGTH)
    try:
        js_data = json.loads(data)
        return js_data
    except json.JSONDecodeError:
        print('Не удалось декодировать полученную Json строку.')
        print(data)
        exit(1)


@func_to_log
def send_message(sock, msg):
    """ кодировка json-сообщения и его отправка """
    js_msg = json.dumps(msg)
    enc_msg = js_msg.encode(ENCODING)
    sock.send(enc_msg)
    time.sleep(0.2)
