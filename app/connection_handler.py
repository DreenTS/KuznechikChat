import binascii
import random
import socket
import time
from typing import Tuple
from PyQt5 import QtCore
from gost.crypto import GOST34122018
from gost.utils import data_splitting
from gost.consts import PRIMES


class ConnectionHandler(QtCore.QObject):
    """
    Класс обработчика соединения.

    """

    SERVER_SUCCESS_SIGNAL = QtCore.pyqtSignal()
    SERVER_ERROR_SIGNAL = QtCore.pyqtSignal()
    WAITING_CONN_SIGNAL = QtCore.pyqtSignal()
    CONN_SUCCESS_SIGNAL = QtCore.pyqtSignal()
    CONN_ERROR_SIGNAL = QtCore.pyqtSignal()
    GOT_REQUEST_SIGNAL = QtCore.pyqtSignal()
    GET_MESSAGE_SIGNAL = QtCore.pyqtSignal()
    SENT_MESSAGE_SIGNAL = QtCore.pyqtSignal()
    DISCONNECTED_COMPANION_SIGNAL = QtCore.pyqtSignal()
    CLIENT = 'client'
    SERVER = 'server'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = None
        self.ip = None
        self.port = None
        self.is_waiting = False
        self.is_connecting = False
        self.is_chatting = False
        self.is_applied = False
        self.is_rejected = False
        self.is_end = False
        self.socket = None
        self.gost = None
        self.companion = None
        self.connection = None
        self.role = None
        self.received_message = None

    @QtCore.pyqtSlot()
    def run(self) -> None:
        """
        Метод запуска потока обработчика.

        Ориентирует свою работу по полям-флагам класса.

        :return: None
        """

        while True:
            if self.is_end:
                break
            if self.is_waiting:
                self.server_waiting()
            if self.is_connecting:
                self.connect_to(_to=self.companion)
            if self.is_chatting:
                self.chatting()

    def server_waiting(self) -> None:
        """
        Метод, вызывающийся для открытия серверного сокета.

        Ожидает входящий запрос на соединение.
        Если запрос был подтверждён - начинает процесс обмена сообщениями.

        :return: None
        """

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.role = self.SERVER
        try:
            self.socket.bind((self.ip, self.port))
            self.SERVER_SUCCESS_SIGNAL.emit()
            while True:
                self.socket.listen(1)
                conn, addr = self.socket.accept()
                if addr[0] == self.ip:
                    conn.close()
                    break
                elif self.connection:
                    conn.close()
                else:
                    self.connection = conn
                    self.companion = addr
                    self.is_chatting = self.request_and_response()
                    if self.is_chatting:
                        self.CONN_SUCCESS_SIGNAL.emit()
                        break
                    else:
                        self.connection.close()
                        self.connection = None
                        self.companion = None
        except OSError:
            self.SERVER_ERROR_SIGNAL.emit()
            self.socket.close()
        self.is_waiting = False

    def connect_to(self, _to: Tuple[str, int]) -> None:
        """
        Метод для открытия клиентского сокета.

        Осуществляет подключение к серверу.
        Если Запрос на подключение принят - начинает процесс обмена сообщениями.

        :param _to: tuple, кортеж (IP-адрес, порт)
        :return: None
        """

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.role = self.CLIENT
        try:
            self.WAITING_CONN_SIGNAL.emit()
            self.socket.connect(_to)
            self.is_chatting = self.request_and_response()
            if self.is_chatting:
                self.CONN_SUCCESS_SIGNAL.emit()
            else:
                raise ConnectionRefusedError
        except (OSError, ConnectionRefusedError, ConnectionResetError):
            self.socket.close()
            self.CONN_ERROR_SIGNAL.emit()
        self.is_connecting = False

    def request_and_response(self) -> bool:
        """
        Метод, вызывающийся при входящем/исходящем запросе на подключение.

        Ожидает ответ от сервера (пользователя сервера).
        Сервер и клиент постоянно обмениваются "системными" сообщениями о том,
        что ответ всё ещё ожидается.
        При получении ответа, происходит отправка соответствующего сообщения.

        :return: bool, принят ли запрос на подключение
        """

        if self.role == self.CLIENT:
            while True:
                self.socket.send('WAITING'.encode(encoding='utf-8'))
                data = self.socket.recv(1024).decode(encoding='utf-8')
                if data == 'OK':
                    return True
                elif data in ['', 'NOK']:
                    return False
        else:
            self.GOT_REQUEST_SIGNAL.emit()
            while True:
                try:
                    data = self.connection.recv(1024).decode(encoding='utf-8')
                    if not data:
                        return False
                    if self.is_applied:
                        self.is_applied = False
                        self.connection.send('OK'.encode(encoding='utf-8'))
                        return True
                    elif self.is_rejected:
                        self.is_rejected = False
                        self.connection.send('NOK'.encode(encoding='utf-8'))
                        return False
                    else:
                        self.connection.send('WAIT'.encode(encoding='utf-8'))
                except (ConnectionRefusedError, ConnectionResetError):
                    return False

    def chatting(self) -> None:
        """
        Метод, обрабатывающий процесс обмена сообщениями.

        В начале процесса обмена сообщениями, формирует мастер-ключ
        при помощи алгоритма Диффи-Хеллмана.
        Постоянно проверяет сокет на наличие новых сообщений от собеседника.

        :return: None
        """

        if self.role == self.CLIENT:
            self.connection = self.socket
        master = list(binascii.unhexlify(self.masterkey_exchange()))
        self.gost = GOST34122018(master_key=master)
        while True:
            if self.is_chatting:
                try:
                    data = self.connection.recv(8192)
                    if data:
                        self.received_message = self.get(cipher=data)
                        self.GET_MESSAGE_SIGNAL.emit()
                    else:
                        raise ConnectionRefusedError
                except Exception:
                    self.disconnect()
                    self.DISCONNECTED_COMPANION_SIGNAL.emit()
            else:
                break

    def masterkey_exchange(self) -> str:
        """
        Метод формирование мастер-ключа.

        Формирует открытый и закрытые ключи.
        Получает закрытый ключ собеседника и вычисляет мастер-ключ.

        :return: str, мастер-ключ длиной 256 бит
        """

        my_secret = f'{self.socket.getsockname()[0].replace(".", "")}' \
                    f'{self.socket.getsockname()[1]}' \
                    f'{int(time.time())}'
        k = 64 - len(my_secret)
        my_secret += ''.join(random.choices('0123456789abcdef', k=k))
        p1, p2 = PRIMES
        my_open = f'{pow(p1, int(my_secret, 16), p2)}'.encode(encoding='utf-8')
        try:
            self.connection.send(bytes(my_open))
            data = self.connection.recvfrom(1024)[0].decode(encoding='utf-8')
            int_master = pow(int(data), int(my_secret, 16), p2)
            hex_master = hex(int_master)
            return hex_master[2:66]
        except (ConnectionRefusedError, ConnectionResetError, AttributeError) as exc:
            raise exc

    def send(self, msg: str) -> None:
        """
        Метод обработки отправляемого сообщения.

        Шифрует сообщение и отправляет его собеседнику.

        :param msg: str, текст отправляемого сообщения (открытый текст)
        :return: None
        """

        open_message_blocks = data_splitting(data=msg)
        cipher_text_blocks = []
        for block in open_message_blocks:
            cipher_text = self.gost.message_prehandling(msg=block, flag='encrypt')
            cipher_text_blocks.extend(cipher_text)
        try:
            self.connection.sendall(bytes(cipher_text_blocks))
        except (ConnectionRefusedError, ConnectionResetError, AttributeError) as exc:
            raise exc

    def get(self, cipher: bytes) -> str:
        """
        Метод обработки полученного сообщения.

        Дешифрует полученное сообщение.

        :param cipher: bytes, зашифрованное сообщение собеседника
        :return: str, текст дешифрованного сообщения собеседника
        """

        _cipher = list(cipher)
        decrypted_message_blocks = []
        for i in range(0, len(_cipher), 16):
            decrypted_message = self.gost.message_prehandling(msg=_cipher[i:i + 16], flag='decrypt')
            decrypted_message_blocks.extend(decrypted_message)
        while decrypted_message_blocks[0] == 0:
            decrypted_message_blocks.pop(0)
        hex_decrypted = ''.join([f'{x:02x}' for x in decrypted_message_blocks])
        recovered = bytes.fromhex(hex_decrypted).decode(encoding='utf-8')
        return recovered

    def disconnect(self) -> None:
        """
        Метод закрытия подключения.

        :return: None
        """

        self.is_chatting = False
        if self.connection:
            self.connection.close()
        self.socket.close()
        self.connection = None
