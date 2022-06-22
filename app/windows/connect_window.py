import socket
from typing import Tuple
from PyQt5 import QtCore, QtGui, QtWidgets


class ConnectWindow(QtWidgets.QWidget):
    """
    Класс окна подключения.

    """

    CONNECTING_SIGNAL = QtCore.pyqtSignal(tuple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_connect = False
        self.connection_data = None
        self.setupUi()

    def setupUi(self) -> None:
        """
        Метод установки параметров UI окна.

        :return: None
        """

        self.setObjectName("Dialog")
        self.setFixedSize(QtCore.QSize(350, 200))
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        # Установка шрифта
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.setFont(font)
        # Метка для ввода IP-адреса
        self.ip_label_layout = QtWidgets.QVBoxLayout()
        self.ip_label_layout.setObjectName("ip_label_layout")
        self.ip_label = QtWidgets.QLabel(self)
        self.ip_label.setFont(font)
        self.ip_label.setObjectName("ip_label")
        self.ip_label_layout.addWidget(self.ip_label)
        self.gridLayout.addLayout(self.ip_label_layout, 0, 0, 1, 1)
        # Поле для ввода IP-адреса
        self.ip_input_layout = QtWidgets.QVBoxLayout()
        self.ip_input_layout.setObjectName("ip_input_layout")
        self.ip_input = QtWidgets.QLineEdit(self)
        self.ip_input.setFixedSize(QtCore.QSize(250, 30))
        self.ip_input.setObjectName("ip_input")
        self.ip_input_layout.addWidget(self.ip_input, 0, QtCore.Qt.AlignLeft)
        self.gridLayout.addLayout(self.ip_input_layout, 1, 0, 1, 1)
        # Метка для ввода порта
        self.port_label_layout = QtWidgets.QVBoxLayout()
        self.port_label_layout.setObjectName("port_label_layout")
        self.port_label = QtWidgets.QLabel(self)
        self.port_label.setFont(font)
        self.port_label.setObjectName("port_label")
        self.port_label_layout.addWidget(self.port_label)
        self.gridLayout.addLayout(self.port_label_layout, 2, 0, 1, 1)
        # Поле для ввода порта
        self.port_input_layout = QtWidgets.QVBoxLayout()
        self.port_input_layout.setObjectName("port_input_layout")
        self.port_input = QtWidgets.QLineEdit(self)
        self.port_input.setFixedSize(QtCore.QSize(250, 30))
        self.port_input.setObjectName("port_input")
        self.port_input_layout.addWidget(self.port_input, 0, QtCore.Qt.AlignLeft)
        self.gridLayout.addLayout(self.port_input_layout, 3, 0, 1, 1)
        # Кнопки
        self.button_box_layout = QtWidgets.QVBoxLayout()
        self.button_box_layout.setObjectName("button_box_layout")
        self.button_box = QtWidgets.QDialogButtonBox(self)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.button_box_layout.addWidget(self.button_box, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        self.gridLayout.addLayout(self.button_box_layout, 4, 0, 1, 1)
        # Привязка функций к кнопкам
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.ip_input.returnPressed.connect(self.button_box.accepted)
        self.port_input.returnPressed.connect(self.button_box.accepted)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self) -> None:
        """
        Метод адаптации текста.

        :return: None
        """

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Подключиться к..."))
        self.ip_label.setText(_translate("Dialog", "Введите IP-адрес собеседника:"))
        self.port_label.setText(_translate("Dialog", "Введите порт для подключения:"))

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Метод, вызывающийся при закрытии окна.

        Если поля ввода для подключения были заполнены корректно -
        вызывает соответствующее событие.
        Очищает поля ввода.

        :param event: QtGui.QCloseEvent object, событие закрытия окна
        :return: None
        """

        super().closeEvent(event)
        if self.is_connect:
            self.CONNECTING_SIGNAL.emit(self.connection_data)
            self.is_connect = False
        self.ip_input.setText('')
        self.port_input.setText('')

    def validate_ip_port(self) -> Tuple[bool, tuple]:
        """
        Метод валидации данных.

        Проводит валидацию введённых данных для подключения:
        IP-адрес и порт.

        :return: tuple, кортеж (валидны_ли_данные, кортеж_данных)
        """

        try:
            if len(self.ip_input.text()) not in range(7, 16):
                raise ValueError
            _ip_str_bytes = socket.inet_aton(self.ip_input.text())
            _ip = socket.inet_ntoa(bytes(_ip_str_bytes))
            _port = int(self.port_input.text())
            if _port in range(65536) and _ip not in ('0.0.0.0', '127.0.0.1'):
                return True, (_ip, _port)
            else:
                return False, ()
        except (OSError, ValueError):
            return False, ()

    def accept(self) -> None:
        """
        Метод, вызывающийся при нажатии на кнопку "ОК".

        Отправляет данные на вход метода валидации.
        Если данные валидны - закрывает окно и устанавливает соответствующий флаг.
        Если данные введены неверно - показывает окно с соответствующим уведомлением.

        :return: None
        """

        _is_valid_data = self.validate_ip_port()
        if _is_valid_data[0]:
            self.is_connect = True
            self.connection_data = _is_valid_data[1]
            self.close()
        else:
            _msg = 'Были введены неверные данные.\nIP-адрес должен быть формата:\n' \
                   '\n[0-255].[0-255].[0-255].[0-255]\n' \
                   '\nИсключены IP-адреса: 0.0.0.0, 127.0.0.1\n' \
                   '\nПорт должен быть формата:\n' \
                   '\n[0-65535]\n' \
                   '\nПроверьте правильность введённых данных и попробуйте ещё раз.'
            QtWidgets.QMessageBox.warning(self, 'Уведомление', _msg, QtWidgets.QMessageBox.Ok)

    def reject(self) -> None:
        """
        Метод, вызывающийся при нажатии на кнопку "Cancel".

        :return: None
        """

        self.close()
