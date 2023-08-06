import json
import sys
import os
import unittest

from config.settings import ENCODING
from config.utils import send_message, get_message

sys.path.append(os.path.join(os.getcwd(), '..'))


class TestSocket:
    '''
    Тестовый класс для тестирования отправки и получения,
    при создании требует словарь, который будет прогонятся
    через тестовую функцию
    '''

    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message_to_send):
        """
        Тестовая функция отправки, корретно  кодирует сообщение,
        так-же сохраняет что должно было отправлено в сокет.
        message_to_send - то, что отправляем в сокет
        :param message_to_send:
        :return:
        """
        json_test_message = json.dumps(self.test_dict)
        # кодирует сообщение
        self.encoded_message = json_test_message.encode(ENCODING)
        # сохраняем что должно было отправлено в сокет
        self.received_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class TestUtils(unittest.TestCase):
    test_dict_send = {
        "action": "presence",
        "time": 1.1,
        "type": "status",
        "user": {
            "account_name": 'Guest',
            "status": "Yep, I am here!"
        }
    }
    test_answer_200 = {
        "response": 200,
        "alert": "Необязательное сообщение/уведомление"
    }

    def test_get_message(self):
        test_socket_ans_200 = TestSocket(self.test_answer_200)
        self.assertEqual(get_message(test_socket_ans_200), self.test_answer_200)

    def test_send_message(self):
        test_socket = TestSocket(self.test_dict_send)
        send_message(test_socket, self.test_dict_send)
        self.assertEqual(test_socket.encoded_message, test_socket.received_message)


if __name__ == '__main__':
    unittest.main()
