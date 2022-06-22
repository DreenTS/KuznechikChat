from socket import AF_INET6
import psutil
from PyQt5 import QtCore, QtGui, QtWidgets


class OpenServerWindow(QtWidgets.QWidget):
    """
    Класс окна открытия сервера.

    """

    OPEN_SERVER_SIGNAL = QtCore.pyqtSignal(tuple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_valid_port = False
        self.ip = None
        self.port = None
        self.setupUi()

    def setupUi(self) -> None:
        """
        Метод установки параметров UI окна.

        :return: None
        """

        self.setObjectName("Dialog")
        self.setFixedSize(QtCore.QSize(420, 200))
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        # Установка шрифта
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.setFont(font)
        # Метка для выбора IP-адреса
        self.ip_label_layout = QtWidgets.QVBoxLayout()
        self.ip_label_layout.setObjectName("ip_label_layout")
        self.ip_label = QtWidgets.QLabel(self)
        self.ip_label.setObjectName("ip_label")
        self.ip_label_layout.addWidget(self.ip_label)
        self.gridLayout.addLayout(self.ip_label_layout, 0, 0, 1, 1)
        # Выпадающий список для выбора IP-адреса
        self.ip_combobox_layout = QtWidgets.QVBoxLayout()
        self.ip_combobox_layout.setObjectName("ip_combobox_layout")
        self.ip_combobox = QtWidgets.QComboBox(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ip_combobox.setFont(font)
        self.ip_combobox.setObjectName("ip_combobox")
        self.ip_combobox_layout.addWidget(self.ip_combobox)
        self.gridLayout.addLayout(self.ip_combobox_layout, 1, 0, 1, 1)
        # Метка для ввода порта
        self.port_label_layout = QtWidgets.QVBoxLayout()
        self.port_label_layout.setObjectName("port_label_layout")
        self.port_label = QtWidgets.QLabel(self)
        self.port_label.setObjectName("port_label")
        self.port_label_layout.addWidget(self.port_label)
        self.gridLayout.addLayout(self.port_label_layout, 2, 0, 1, 1)
        # Поле для ввода порта
        self.port_input_layout = QtWidgets.QVBoxLayout()
        self.port_input_layout.setObjectName("port_input_layout")
        self.port_input = QtWidgets.QLineEdit(self)
        self.port_input.setFixedSize(QtCore.QSize(150, 30))
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
        self.button_box_layout.addWidget(self.button_box, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        self.gridLayout.addLayout(self.button_box_layout, 4, 0, 2, 1)
        # Привязка функций к кнопкам
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.port_input.returnPressed.connect(self.button_box.accepted)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self) -> None:
        """
        Метод адаптации текста.

        :return: None
        """

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Войти в сеть"))
        self.ip_label.setText(_translate("Dialog", "Выберите IP-адрес:"))
        self.port_label.setText(_translate("Dialog", "Введите порт для открытия сервера:"))

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Метод, вызывающийся при закрытии окна.

        Если введённый порт валиден - вызывает соответствующее событие.

        :param event: QtGui.QCloseEvent object, событие закрытия окна
        :return: None
        """

        super().closeEvent(event)
        if self.is_valid_port:
            self.OPEN_SERVER_SIGNAL.emit((self.ip, self.port))
        self.port_input.setText('')
        self.is_valid_port = False

    def show(self) -> None:
        """
        Метод, вызывающийся при открытии окна.

        Сканирует систему на наличие доступных интерфейсов.
        При их отсутствии вызывает исключение.

        :return: None
        """

        self.ip_combobox.clear()
        _interfaces = psutil.net_if_addrs()
        _stats = psutil.net_if_stats()
        _translate = QtCore.QCoreApplication.translate
        _index = 0
        for _int in _interfaces:
            try:
                if _interfaces[_int][0][1] != '127.0.0.1' and getattr(_interfaces[_int][1], "family") != AF_INET6:
                    if _int not in _stats or (_int in _stats and getattr(_stats[_int], "isup")):
                        self.ip_combobox.addItem("")
                        self.ip_combobox.setItemText(_index, _translate("Dialog", f"{_int} := {_interfaces[_int][1][1]}"))
                        _index += 1
            except Exception:
                raise ValueError
        if self.ip_combobox.count() == 0:
            raise ValueError
        super().show()

    def validate_port(self) -> bool:
        """
        Метод валидации введённого порта.

        :return: bool, является ли введённый порт валидным
        """

        try:
            _port = int(self.port_input.text())
            if _port in range(1, 65536):
                self.port = _port
                return True
        except (OSError, ValueError):
            return False

    def accept(self) -> None:
        """
        Метод, вызывающийся при нажатии на кнопку "ОК".

        Отправляет введённый порт на вход метода валидации.
        Если порт валиден - закрывает окно.
        Если порт введён неверно - показывает окно с соответствующим уведомлением.

        :return: None
        """

        _ip = self.ip_combobox.currentText()
        self.ip = _ip[_ip.find(' := ') + 4:]
        self.is_valid_port = self.validate_port()
        if self.is_valid_port:
            self.close()
        else:
            _msg = 'Были введены неверные данные.' \
                   '\nПорт должен быть формата:\n' \
                   '\n[1-65535]\n' \
                   '\nПроверьте правильность введённых данных и попробуйте ещё раз.'
            QtWidgets.QMessageBox.warning(self, 'Уведомление', _msg, QtWidgets.QMessageBox.Ok)

    def reject(self) -> None:
        """
        Метод, вызывающийся при нажатии на кнопку "Cancel".

        :return: None
        """

        self.close()
