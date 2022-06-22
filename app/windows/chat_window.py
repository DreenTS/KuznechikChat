from typing import Tuple
from PyQt5 import QtCore, QtGui, QtWidgets


class ChatWindow(QtWidgets.QMainWindow):
    """
    Класс окна чата.

    """

    SEND_SIGNAL = QtCore.pyqtSignal()
    DISCONNECT_SIGNAL = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lost_companion = False
        self.setupUi()

    def setupUi(self) -> None:
        """
        Метод установки параметров UI окна.

        :return: None
        """

        self.setObjectName("ChatWindow")
        self.setFixedSize(QtCore.QSize(600, 550))
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        # Установка шрифта
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.setFont(font)
        # Поле чата
        self.chat_plain_layout = QtWidgets.QVBoxLayout()
        self.chat_plain_layout.setObjectName("chat_plain_layout")
        self.chat_plain = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.chat_plain.setFixedSize(QtCore.QSize(550, 350))
        self.chat_plain.setFocusPolicy(QtCore.Qt.NoFocus)
        self.chat_plain.setStyleSheet(
            "QPlainTextEdit {\n"
            "border: 1px solid black;\n"
            "}"
        )
        self.chat_plain.setObjectName("chat_plain")
        self.chat_plain_layout.addWidget(self.chat_plain, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.gridLayout.addLayout(self.chat_plain_layout, 0, 0, 1, 1)
        # Поле ввода сообщения
        self.msg_input_layout = QtWidgets.QVBoxLayout()
        self.msg_input_layout.setObjectName("msg_input_layout")
        self.msg_input_line = QtWidgets.QLineEdit(self.centralwidget)
        self.msg_input_line.setFixedSize(QtCore.QSize(550, 40))
        self.msg_input_line.setObjectName("msg_input_line")
        self.msg_input_layout.addWidget(self.msg_input_line, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.gridLayout.addLayout(self.msg_input_layout, 1, 0, 1, 1)
        # Кнопки отправки сообщения и отключения от чата
        self.send_disconnect_layout = QtWidgets.QHBoxLayout()
        self.send_disconnect_layout.setObjectName("send_disconnect_layout")
        self.send_btn = QtWidgets.QPushButton(self.centralwidget)
        self.send_btn.setFixedSize(QtCore.QSize(250, 40))
        self.send_btn.setObjectName("send_btn")
        self.disconnect_btn = QtWidgets.QPushButton(self.centralwidget)
        self.disconnect_btn.setFixedSize(QtCore.QSize(250, 40))
        self.disconnect_btn.setObjectName("disconnect_btn")
        self.send_disconnect_layout.addWidget(self.send_btn)
        self.send_disconnect_layout.addWidget(self.disconnect_btn)
        self.gridLayout.addLayout(self.send_disconnect_layout, 2, 0, 1, 1)
        # Привязка функций к кнопкам
        self.send_btn.clicked.connect(self.SEND_SIGNAL.emit)
        self.disconnect_btn.clicked.connect(self.DISCONNECT_SIGNAL.emit)
        self.msg_input_line.returnPressed.connect(self.SEND_SIGNAL.emit)

        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self) -> None:
        """
        Метод адаптации текста.

        :return: None
        """

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("ChatWindow", "KuznechikChat"))
        self.msg_input_line.setPlaceholderText(_translate("ChatWindow", "Текст сообщения..."))
        self.send_btn.setText(_translate("ChatWindow", "Отправить"))
        self.disconnect_btn.setText(_translate("ChatWindow", "Отключиться"))

    def start_chatting(self, companion: Tuple[str, int]) -> None:
        """
        Метод, вызывающийся при старте обмена сообщения.

        Выводит на экран приветственное сообщение
        и устанавливает текст для полосы статуса.

        :param companion: tuple, кортеж (IP-адрес, порт)
        :return: None
        """

        self.chat_plain.setPlainText(f'Добро пожаловать в чат! Ваш собеседник: {companion[0]}')
        self.statusbar.showMessage(f'Connected to: {companion[0]}')

    def show_disconnected_message(self) -> None:
        """
        Метод, вызывающийся при отключении от чата.

        Показывает окно с соответствующим уведомлением
        и вызывает события закрытия соединения.

        :return: None
        """

        self.lost_companion = True
        _msg = 'Соединение завершено. Возможные причины:\n\n' \
               '1) Вы отключились от чата\n\n' \
               '2) Собеседник отключился от чата.'
        QtWidgets.QMessageBox.warning(self, 'Уведомление', _msg, QtWidgets.QMessageBox.Ok)
        self.DISCONNECT_SIGNAL.emit()
