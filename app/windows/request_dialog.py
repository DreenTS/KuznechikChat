from PyQt5 import QtCore, QtGui, QtWidgets


class RequestDialog(QtWidgets.QWidget):
    """
    Класс диалогового окна обработки запроса.

    """

    REQUEST_APPLIED_SIGNAL = QtCore.pyqtSignal()
    REQUEST_REJECTED_SIGNAL = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.curr_requester = None
        self.setupUi()

    def setupUi(self) -> None:
        """
        Метод установки параметров UI окна.

        :return: None
        """

        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setObjectName("RequestDialog")
        self.setFixedSize(QtCore.QSize(360, 145))
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.setFont(font)
        # Метка инфо-сообщения
        self.info_label_layout = QtWidgets.QVBoxLayout()
        self.info_label_layout.setObjectName("info_label_layout")
        self.info_label = QtWidgets.QLabel(self)
        self.info_label.setObjectName("info_label")
        self.info_label_layout.addWidget(self.info_label, 0, QtCore.Qt.AlignVCenter)
        self.gridLayout.addLayout(self.info_label_layout, 0, 0, 1, 1)
        # Метка для вывода IP-адреса
        self.ip_label_layout = QtWidgets.QVBoxLayout()
        self.ip_label_layout.setObjectName("ip_label_layout")
        self.ip_label = QtWidgets.QLabel(self)
        self.ip_label.setText("")
        self.ip_label.setObjectName("ip_label")
        self.ip_label_layout.addWidget(self.ip_label, 0, QtCore.Qt.AlignVCenter)
        self.gridLayout.addLayout(self.ip_label_layout, 1, 0, 1, 1)
        # Кнопки
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.setObjectName("buttons_layout")
        self.accept_btn = QtWidgets.QPushButton(self)
        self.accept_btn.setObjectName("accept_btn")
        self.buttons_layout.addWidget(self.accept_btn)
        self.reject_btn = QtWidgets.QPushButton(self)
        self.reject_btn.setObjectName("reject_btn")
        self.buttons_layout.addWidget(self.reject_btn)
        self.gridLayout.addLayout(self.buttons_layout, 2, 0, 1, 1)
        # Привязка функций к кнопкам
        self.accept_btn.clicked.connect(self.REQUEST_APPLIED_SIGNAL.emit)
        self.reject_btn.clicked.connect(self.REQUEST_REJECTED_SIGNAL.emit)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self) -> None:
        """
        Метод адаптации текста.

        :return: None
        """

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("RequestDialog", "Запрос"))
        self.info_label.setText(_translate("RequestDialog", "Поступил запрос на подключение от:"))
        self.accept_btn.setText(_translate("RequestDialog", "Принять"))
        self.reject_btn.setText(_translate("RequestDialog", "Отклонить"))

    def show(self) -> None:
        """
        Метод, вызывающийся при открытии окна.

        Устанавливает текст метки-адреса входящего подключения.

        :return: None
        """

        self.ip_label.setText(f'IP-адрес: {self.curr_requester[0]}')
        super().show()
