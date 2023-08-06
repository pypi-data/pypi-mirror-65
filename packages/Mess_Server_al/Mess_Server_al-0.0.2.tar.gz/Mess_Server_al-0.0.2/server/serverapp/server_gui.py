from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, \
    QPushButton, QDialog, QDialogButtonBox, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QLabel, QFileDialog, \
    QHBoxLayout
from PyQt5.QtCore import QSize, Qt

from config.settings import DEFAULT_HOST, DEFAULT_PORT, SERVER_DATABASE


class StartServer(QDialog):
    # NumGridRows = 3
    # NumButtons = 4

    def __init__(self):
        super(StartServer, self).__init__()
        self.create_form_group_box()

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        # button_box.accepted.connect(self.accept)
        button_box.accepted.connect(self.press_ok_event)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.form_group_box)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

        self.setWindowTitle("Server settings")

    def create_form_group_box(self):
        self.form_group_box = QGroupBox("Параметры запуска сервера: ")
        form = QFormLayout()

        hbox = QHBoxLayout()

        # Кнопка выбора пути.
        self.db_path_select = QPushButton('Обзор...', self)

        # Функция обработчик открытия окна выбора папки
        def open_file_dialog():
            path = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
            path = path.replace('/', '\\')
            self.line_path_to_db.setText(path)

        self.db_path_select.clicked.connect(open_file_dialog)

        self.line_path_to_db = QLineEdit()
        self.line_file_db = QLineEdit(text=SERVER_DATABASE)
        self.line_host = QLineEdit(text=DEFAULT_HOST)
        self.line_port = QLineEdit(text=str(DEFAULT_PORT))

        hbox.addStretch(1)
        hbox.addWidget(self.line_path_to_db)
        hbox.addWidget(self.db_path_select)

        form.addRow(QLabel("Путь до файла базы данных: "), hbox)
        form.addRow(QLabel("Файл базы данных: "), self.line_file_db)
        form.addRow(QLabel("Host:"), self.line_host)
        form.addRow(QLabel("Port:"), self.line_port)
        # layout.addRow(QLabel("Clients:"), QSpinBox(value=2))
        self.form_group_box.setLayout(form)

    def press_ok_event(self):
        with open('../server.ini', 'w') as the_file:
            the_file.write(
                f'[SETTINGS]\n'
                f'database_path = {self.line_path_to_db.text()}\n'
                f'database_file = {self.line_file_db.text()}\n'
                f'default_port = {self.line_port.text()}\n'
                f'listen_address = {self.line_host.text()}\n'
            )
        self.close()


# Наследуемся от QMainWindow
class UsersStatistic(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self, users_json):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)
        self.users_json = users_json

        self.setMinimumSize(QSize(480, 80))  # Устанавливаем размеры
        self.setWindowTitle("Список подключенных клиентов")  # Устанавливаем заголовок окна
        central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(central_widget)  # Устанавливаем центральный виджет

        grid_layout = QGridLayout()  # Создаём QGridLayout
        central_widget.setLayout(grid_layout)  # Устанавливаем данное размещение в центральный виджет

        self.table = QTableWidget(self)  # Создаём таблицу
        self.table.setColumnCount(4)  # Устанавливаем три колонки

        # Устанавливаем заголовки таблицы
        self.table.setHorizontalHeaderLabels(["Пользователь", "IP адрес", "Порт", "Последний логин"])

        # # Устанавливаем всплывающие подсказки на заголовки
        self.table.horizontalHeaderItem(0).setToolTip("Пользователь")
        self.table.horizontalHeaderItem(1).setToolTip("IP адрес")
        self.table.horizontalHeaderItem(2).setToolTip("Порт")
        self.table.horizontalHeaderItem(3).setToolTip("Последний логин")

        # Устанавливаем выравнивание на заголовки
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter)

        # заполняем таблицу данными
        self.fill_table()

        # делаем ресайз колонок по содержимому
        self.table.resizeColumnsToContents()

        # refresh button
        refresh_btn = QPushButton('Обновить', self)
        refresh_btn.setToolTip('Обновить')
        refresh_btn.clicked.connect(self.fill_table)

        grid_layout.addWidget(self.table, 0, 0)  # Добавляем таблицу в сетку
        grid_layout.addWidget(refresh_btn, 0, 1)  # Добавляем кнопку Обновить в сетку

        # refresh timer
        self.timer_status = QtCore.QTimer()
        self.timer_status.timeout.connect(self.fill_table)

        # check every half-second
        self.timer_status.start(1000)

    def clear_table(self):
        self.table.clear()

    def fill_table(self):
        if len(self.users_json) == 0:
            self.table.setRowCount(1)  # Устанавливаем количество строк в таблице
            # заполняем первую строку
            self.table.setItem(0, 0, QTableWidgetItem(""))
            self.table.setItem(0, 1, QTableWidgetItem(""))
            self.table.setItem(0, 2, QTableWidgetItem(""))
        else:
            users_list = list(self.users_json.keys())

            self.table.setRowCount(len(users_list))  # Устанавливаем количество строк в таблице

            for i in range(len(users_list)):
                self.table.setItem(i, 0, QTableWidgetItem(users_list[i]))
                self.table.setItem(i, 1, QTableWidgetItem(self.users_json[users_list[i]]['ip_addr']))
                self.table.setItem(i, 2, QTableWidgetItem(str(self.users_json[users_list[i]]['port'])))
                self.table.setItem(i, 3,
                                   QTableWidgetItem(
                                       self.users_json[users_list[i]]['login_time'].strftime("%Y-%m-%d-%H.%M.%S")))


if __name__ == "__main__":
    import sys
    import datetime

    app = QApplication(sys.argv)
    dialog = StartServer()
    dialog.show()
    # dialog.exec_()

    all_users = {
        "client1": {
            'socket': "<socket.socket fd=784, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, "
                      "laddr=('127.0.0.1', 7777), raddr=('127.0.0.1', 50165)>",
            'ip_addr': '127.0.0.1',
            'port': 50165,
            'login_time': datetime.datetime(2020, 2, 28, 19, 25, 34, 276014)
        }
    }
    # mw = UsersStatistic(all_users)
    # mw.show()
    sys.exit(app.exec())

