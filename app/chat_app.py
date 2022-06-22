import os
import socket
import sys
from typing import Tuple
from app.connection_handler import ConnectionHandler
from app.windows.chat_window import ChatWindow
from app.windows.main_window import MainWindow
from app.windows.open_server_window import OpenServerWindow
from app.windows.connect_window import ConnectWindow
from app.windows.request_dialog import RequestDialog
from PyQt5 import QtCore, QtWidgets, QtGui


def resource_path(relative: str) -> str:
    """
    Функция составления пути для логотипа приложения.

    :param relative: str, относительный путь до логотипа
    :return: str, абсолютный путь до логотипа
    """

    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(os.path.abspath("."), relative)


class KuznechikChatApp(QtWidgets.QApplication):
    """
    Класс всего оконного приложения.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowIcon(QtGui.QIcon(resource_path('logo.ico')))
        self.connection_handler = ConnectionHandler()
        self.main_window = MainWindow()
        self.open_port_window = OpenServerWindow()
        self.connect_window = ConnectWindow()
        self.request_dialog = RequestDialog()
        self.chat_window = ChatWindow()
        self.thread = QtCore.QThread()
        self.configure()
        self.main_window.show()

    def configure(self) -> None:
        """
        Метод начальной конфигурации всех окон приложения.

        :return: None
        """

        # Конфигурация обработчика соединения
        self.connection_handler.moveToThread(self.thread)
        self.connection_handler.SERVER_SUCCESS_SIGNAL.connect(self.server_is_opened)
        self.connection_handler.SERVER_ERROR_SIGNAL.connect(self.main_window.server_error)
        self.connection_handler.WAITING_CONN_SIGNAL.connect(self.main_window.waiting_for_companion)
        self.connection_handler.CONN_SUCCESS_SIGNAL.connect(self.main_window.connection_success)
        self.connection_handler.CONN_ERROR_SIGNAL.connect(self.main_window.connection_error)
        self.connection_handler.GOT_REQUEST_SIGNAL.connect(self.show_request_dialog)
        self.connection_handler.GET_MESSAGE_SIGNAL.connect(self.show_received_message)
        self.connection_handler.DISCONNECTED_COMPANION_SIGNAL.connect(self.disconnected_companion)
        self.thread.started.connect(self.connection_handler.run)
        self.thread.start()
        # Конфигурация главного окна
        self.main_window.CLOSE_APP_SIGNAL.connect(self.close_app)
        self.main_window.SHOW_SERVER_SIGNAL.connect(self.show_server_window)
        self.main_window.SHOW_CONNECTION_SIGNAL.connect(self.show_connection_window)
        self.main_window.CLOSE_CONNECTION_SIGNAL.connect(self.close_connection)
        self.main_window.START_CHATTING_SIGNAL.connect(self.show_chat_window)
        # Конфигурация модального окна открытия сервера
        self.open_port_window.OPEN_SERVER_SIGNAL.connect(self.open_server)
        self.open_port_window.setWindowModality(QtCore.Qt.ApplicationModal)
        # Конфигурация модального окна соединения
        self.connect_window.CONNECTING_SIGNAL.connect(self.open_connection)
        self.connect_window.setWindowModality(QtCore.Qt.ApplicationModal)
        # Конфигурация модального диалога обработки запроса
        self.request_dialog.REQUEST_APPLIED_SIGNAL.connect(self.apply_request)
        self.request_dialog.REQUEST_REJECTED_SIGNAL.connect(self.reject_request)
        self.request_dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        # Конфигурация окна чата
        self.chat_window.SEND_SIGNAL.connect(self.send_message)
        self.chat_window.DISCONNECT_SIGNAL.connect(self.disconnect_chat)

    def disconnect_myself(self) -> None:
        """
        Метод отключения серверного сокета.

        :return: None
        """

        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((self.connection_handler.ip, self.connection_handler.port))
        sock.close()

    def close_app(self, event: QtGui.QCloseEvent) -> None:
        """
        Метод закрытия приложения.

        Вызывает диалоговое окно для подтверждения закрытия приложения.

        :param event: QtGui.QCloseEvent object, события закрытия главного окна приложения
        :return: None
        """

        reply = QtWidgets.QMessageBox.question(
            self.main_window, 'Выход', 'Закрыть приложение?',
            QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            if self.connection_handler.is_waiting:
                self.disconnect_myself()
            self.connection_handler.is_end = True
            self.thread.exit()
            event.accept()
            self.closeAllWindows()
        else:
            event.ignore()

    def open_server(self, ip_port: Tuple[str, int]) -> None:
        """
        Метод для открытия серверного сокета.

        Переводит обработчик соединения в режим прослушивания сокета.

        :param ip_port: tuple, кортеж (IP-адрес, порт)
        :return: None
        """

        self.connection_handler.ip = ip_port[0]
        self.connection_handler.port = ip_port[1]
        self.connection_handler.is_waiting = True

    def server_is_opened(self) -> None:
        """
        Метод, вызывающийся при успешном открытии серверного сокета.

        :return: None
        """

        self.main_window.server_is_opened(server=(self.connection_handler.ip, self.connection_handler.port))

    def open_connection(self, data: Tuple[str, int]) -> None:
        """
        Метод для открытия соединения с собеседником по указанным данным.

        :param data: tuple, кортеж (IP-адрес, порт)
        :return: None
        """

        self.connection_handler.companion = data
        self.connection_handler.is_connecting = True

    def show_server_window(self) -> None:
        """
        Метод, открывающий окно для ввода данных серверного сокета.

        :return: None
        """

        if self.connection_handler.is_waiting:
            _msg = 'Ваше устройство станет недоступно для поиска по сети. Продолжить?'
        else:
            _msg = 'Войдя в сеть, Ваше устройство станет доступно для поиска по сети. Продолжить?'
        reply = QtWidgets.QMessageBox.warning(
            self.main_window, 'Предупреждение', _msg,
            QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            if self.connection_handler.is_waiting:
                self.disconnect_myself()
                self.main_window.server_is_closed()
            else:
                try:
                    self.open_port_window.show()
                except ValueError:
                    _msg = 'Не удалось войти в сеть.' \
                           '\nПричина:\n' \
                           '\nНет ни одного IP-адреса или интерфейса, к которому можно привязать сервер.\n'\
                           '\nПроверьте настройки сети, перезапустите приложение и попробуйте ещё раз.'
                    QtWidgets.QMessageBox.warning(self.main_window, 'Ошибка', _msg, QtWidgets.QMessageBox.Ok)

    def show_connection_window(self) -> None:
        """
        Метод, открывающий окно для ввода данных подключения к собеседнику.

        :return: None
        """

        if self.connection_handler.is_connecting:
            self.connection_handler.socket.close()
        else:
            self.connect_window.is_connect = False
            self.connect_window.show()

    def show_chat_window(self) -> None:
        """
        Метод, открывающий окно чата.

        :return: None
        """

        self.chat_window.show()
        self.chat_window.start_chatting(companion=self.connection_handler.companion)

    def show_request_dialog(self) -> None:
        """
        Метод, открывающий диалоговое окно при входящем подключении.

        :return: None
        """

        self.request_dialog.curr_requester = self.connection_handler.companion
        self.request_dialog.show()

    def apply_request(self) -> None:
        """
        Метод, вызывающийся при принятии входящего запроса на водключение.

        :return: None
        """

        self.request_dialog.close()
        self.connection_handler.is_applied = True

    def reject_request(self) -> None:
        """
        Метод, вызывающийся при отклонении входящего запроса на водключение.

        :return: None
        """

        self.request_dialog.close()
        self.connection_handler.is_rejected = True

    def close_connection(self) -> None:
        """
        Метод, вызывающийся при отклонение исходящего запроса на подключение.

        :return: None
        """

        if self.connection_handler.connection:
            self.connection_handler.connection.close()
        self.connection_handler.connection = None

    def show_received_message(self) -> None:
        """
        Метод, выводящий на экран полученное от собеседника сообщение.

        :return: None
        """

        _msg = self.connection_handler.received_message
        self.chat_window.chat_plain.Text(f'Собеседник: {_msg}')

    def send_message(self) -> None:
        """
        Метод для отправки сообщения собеседнику.

        Передаёт сообщение обработчику соединения.
        После успешной отправки сообщения, выводит его на экран.

        :return: None
        """

        _msg = self.chat_window.msg_input_line.text()
        if _msg != '':
            try:
                self.connection_handler.send(msg=_msg)
                self.chat_window.chat_plain.appendPlainText(f'Вы: {_msg}')
                self.chat_window.msg_input_line.clear()
            except (ConnectionRefusedError, ConnectionResetError, AttributeError):
                self.disconnected_companion()

    def disconnected_companion(self) -> None:
        """
        Метод, вызывающийся при отключении собеседника.

        :return: None
        """

        self.chat_window.show_disconnected_message()

    def disconnect_chat(self) -> None:
        """
        Метод, выполняющий отключение от чата.

        :return: None
        """

        if self.chat_window.lost_companion:
            self.chat_window.lost_companion = False
            self.chat_window.close()
            self.main_window.server_is_closed()
            self.main_window.show()
        else:
            _msg = 'Отключиться от чата?'
            reply = QtWidgets.QMessageBox.warning(
                self.chat_window, 'Подтверждение', _msg,
                QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.Yes:
                self.connection_handler.disconnect()
                self.chat_window.close()
                self.main_window.server_is_closed()
                self.main_window.show()

