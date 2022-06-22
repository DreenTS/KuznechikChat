from typing import Tuple
from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    """
    Класс главного окна приложения.

    """

    CLOSE_APP_SIGNAL = QtCore.pyqtSignal(QtCore.QEvent)
    SHOW_SERVER_SIGNAL = QtCore.pyqtSignal()
    SHOW_CONNECTION_SIGNAL = QtCore.pyqtSignal()
    CLOSE_CONNECTION_SIGNAL = QtCore.pyqtSignal()
    START_CHATTING_SIGNAL = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi()

    def setupUi(self) -> None:
        """
        Метод установки параметров UI окна.

        :return: None
        """

        self.setObjectName("MainWindow")
        self.setFixedSize(QtCore.QSize(400, 400))
        self.setStyleSheet("background-color: rgb(241, 241, 241);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        # Метка лого
        self.logo_label_layout = QtWidgets.QVBoxLayout()
        self.logo_label_layout.setSpacing(7)
        self.logo_label_layout.setObjectName("logo_label_layout")
        self.logo_label = QtWidgets.QLabel(self.centralwidget)
        font_logo = QtGui.QFont()
        font_logo.setFamily("Times New Roman")
        font_logo.setPointSize(26)
        font_logo.setBold(True)
        font_logo.setWeight(75)
        self.logo_label.setFont(font_logo)
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)
        self.logo_label.setObjectName("logo_label")
        self.logo_label_layout.addWidget(self.logo_label)
        self.gridLayout.addLayout(self.logo_label_layout, 0, 0, 1, 1)
        # Метка статуса в сети
        self.log_io_label_layout = QtWidgets.QVBoxLayout()
        self.log_io_label_layout.setObjectName("log_io_label_layout")
        self.log_io_label = QtWidgets.QLabel(self.centralwidget)
        self.log_io_label.setStyleSheet("color: rgb(255, 0, 0);")
        self.log_io_label.setAlignment(QtCore.Qt.AlignCenter)
        self.log_io_label.setObjectName("log_io_label")
        self.log_io_label_layout.addWidget(self.log_io_label)
        self.gridLayout.addLayout(self.log_io_label_layout, 1, 0, 1, 1)
        # Кнопка входа в сеть
        self.log_io_btn_layout = QtWidgets.QVBoxLayout()
        self.log_io_btn_layout.setContentsMargins(0, -1, 0, 0)
        self.log_io_btn_layout.setObjectName("log_io_btn_layout")
        self.log_in_out_btn = QtWidgets.QPushButton(self.centralwidget)
        self.log_in_out_btn.setFixedSize(QtCore.QSize(200, 35))
        self.log_in_out_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.log_in_out_btn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.log_in_out_btn.setObjectName("log_in_out_btn")
        self.log_io_btn_layout.addWidget(self.log_in_out_btn, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.gridLayout.addLayout(self.log_io_btn_layout, 2, 0, 1, 1)
        # Кнопка подключения к собеседнику
        self.connect_btn_layout = QtWidgets.QVBoxLayout()
        self.connect_btn_layout.setContentsMargins(0, -1, -1, 60)
        self.connect_btn_layout.setObjectName("connect_btn_layout")
        self.connect_btn = QtWidgets.QPushButton(self.centralwidget)
        self.connect_btn.setFixedSize(QtCore.QSize(260, 35))
        self.connect_btn.setObjectName("connect_btn")
        self.connect_btn_layout.addWidget(self.connect_btn, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.gridLayout.addLayout(self.connect_btn_layout, 3, 0, 1, 1)
        # Установка шрифта
        self.log_io_label.setFont(font)
        self.log_in_out_btn.setFont(font)
        self.connect_btn.setFont(font)
        # Привязка функций к кнопкам
        self.log_in_out_btn.clicked.connect(self.SHOW_SERVER_SIGNAL.emit)
        self.connect_btn.clicked.connect(self.SHOW_CONNECTION_SIGNAL.emit)

        self.setCentralWidget(self.centralwidget)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self) -> None:
        """
        Метод адаптации текста.

        :return: None
        """

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "KuznechikChat"))
        self.logo_label.setText(_translate("MainWindow", "KuznechikChat"))
        self.log_io_label.setText(_translate("MainWindow", "Вы не в сети."))
        self.log_in_out_btn.setText(_translate("MainWindow", "Войти в сеть"))
        self.connect_btn.setText(_translate("MainWindow", "Подключиться к собеседнику"))

    def hide(self) -> None:
        """
        Метод сокрытия окна.

        Вызывает события начала обмна сообщениями.

        :return: None
        """

        super().hide()
        self.START_CHATTING_SIGNAL.emit()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Метод, вызывающийся при закрытии окна.

        Вызывает соответствующее событие для приложения.

        :param event: QtGui.QCloseEvent object, событие закрытия окна
        :return: None
        """

        self.CLOSE_APP_SIGNAL.emit(event)

    def server_is_opened(self, server: Tuple[str, int]) -> None:
        """
        Метод, вызывающийся при открытии серверного сокета.

        Меняет внешний вид главного окна.

        :param server: tuple, кортеж (IP-адрес, порт)
        :return: None
        """

        self.connect_btn.setEnabled(False)
        self.log_io_label.setStyleSheet('color: rgb(0, 130, 0);')
        self.log_io_label.setText(f'Вы в сети!\n'
                                  f'Сервер открыт: {server[0]}:{server[1]}\n'
                                  f'Ожидайте запроса на обмен сообщениями.')
        self.log_in_out_btn.setText('Отключиться')

    def server_is_closed(self) -> None:
        """
        Метод, вызывающийся при закрытии серверного сокета.

        Меняет внешний вид главного окна.

        :return: None
        """

        self.log_in_out_btn.setEnabled(True)
        self.connect_btn.setEnabled(True)
        self.log_io_label.setStyleSheet('color: rgb(255, 0, 0);')
        self.log_io_label.setText('Вы не в сети.')
        self.log_in_out_btn.setText('Войти в сеть')
        self.connect_btn.setText('Подключиться к собеседнику')

    def server_error(self) -> None:
        """
        Метод, вызывающийся при ошибки открытия серверного сокета.

        Показывает окно с соответствующей ошибкой.

        :return: None
        """

        _msg = 'Не удалось войти в сеть.' \
               '\nПричина:\n' \
               '\nПорт должен быть открыт для соединения и не использоваться ' \
               'системой на момент входа в сеть.\n' \
               '\nПроверьте настройки сети и попробуйте ещё раз.'
        QtWidgets.QMessageBox.warning(self, 'Ошибка', _msg, QtWidgets.QMessageBox.Ok)

    def waiting_for_companion(self) -> None:
        """
        Метод, вызывающийся при ожидании ответа на запрос.

        Меняет внешний вид главного окна.

        :return: None
        """

        self.log_io_label.setStyleSheet('color: rgb(0, 0, 255);')
        self.log_io_label.setText(f'Запрос на соединение отправлен.\nОжидайте ответа.')
        self.log_in_out_btn.setEnabled(False)
        self.connect_btn.setText('Отключиться')

    def connection_success(self) -> None:
        """
        Метод, вызывающийся при успешном подключении к собеседнику.

        Меняет внешний вид главного окна.
        Запускает таймер на 2 секунды.

        :return: None
        """

        self.log_io_label.setStyleSheet('color: rgb(255, 0, 200);')
        self.log_io_label.setText('Соединение установлено!')
        QtCore.QTimer.singleShot(2000, self.hide)

    def connection_error(self, response_error: bool = False) -> None:
        """
        Метод, вызывающийся при отклонении входящего/исходящего запроса на водключение.

        :param response_error: bool, флаг, указывающий, был ли запрос исходящий
        :return: None
        """

        _msg = 'Соединение прервано. Возможные причины:\n\n' \
               '1) Вы отозвали/отклонили запрос на соединение.\n\n' \
               '2) Собеседник отклонил запрос на соединение.\n\n' \
               '3) Собеседник находится вне сети.'
        QtWidgets.QMessageBox.warning(self, 'Уведомление', _msg, QtWidgets.QMessageBox.Ok)
        self.CLOSE_CONNECTION_SIGNAL.emit()
        if not response_error:
            self.server_is_closed()
