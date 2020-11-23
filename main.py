import sqlite3
import sys
import random

from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QLCDNumber, QMessageBox, QInputDialog, \
    QTableWidgetItem
from PyQt5 import QtGui, QtCore, QtWidgets


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class Show_results(QtWidgets.QDialog): # класс формы для отображения результатов из SQL-таблицы
    def __init__(self):
        super().__init__()
        self.btn_close = QPushButton("Закрыть результаты", self)
        self.btn_close.clicked.connect(self.btnClosed)
        self.btn_close.move(400, 700)
        self.btn_close.resize(200, 50)
        self.btn_close.setFont(QtGui.QFont('Arial', 11, QtGui.QFont.Bold))
        self.setGeometry(400, 150, 1000, 800)
        self.setWindowTitle("Общие результаты")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(90, 51, 830, 600))
        self.tableWidget.setObjectName("tableWidget")
        self.connection = sqlite3.connect("sea_battle_game.db")

        query = "SELECT * FROM all_games"
        res = self.connection.cursor().execute(query).fetchall()
        # Заполним размеры таблицы
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.setColumnWidth(0, 300)
        self.tableWidget.setColumnWidth(1, 170)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setColumnWidth(3, 220)

        self.tableWidget.setHorizontalHeaderLabels(["Имя", "Результат игры", "Время игры", "Местное время начала игры"])

    def closeEvent(self, event):
        # При закрытии формы закроем и наше соединение
        # с базой данных
        self.connection.close()

    def btnClosed(self):
        self.close()


class Example(QWidget):
    def __init__(self):  # инициализация всех переменных для дальнейшей работы
        super().__init__()
        self.letters_coords = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К']
        self.left_buttons = []
        self.open_ships = []
        self.check_our = []
        self.all = []
        self.wrong = []
        self.IQ = [(1, 2), (1, 4), (1, 6), (1, 8), (1, 10), (2, 1), (2, 3), (2, 5), (2, 7), (2, 9), (3, 2), (3, 4),
                   (3, 6), (3, 8), (3, 10), (4, 1), (4, 3), (4, 5), (4, 7), (4, 9), (5, 2), (5, 4), (5, 6), (5, 8),
                   (5, 10), (6, 1), (6, 3), (6, 5), (6, 7), (6, 9), (7, 2), (7, 4), (7, 6), (7, 8), (7, 10), (8, 1),
                   (8, 3), (8, 5), (8, 7), (8, 9), (9, 2), (9, 4), (9, 6), (9, 8), (9, 10), (10, 1), (10, 3), (10, 5),
                   (10, 7), (10, 9)]
        self.open_our_ships = []
        self.computer_buttons = []
        self.color_buttons = []
        self.user_color_buttons = []
        self.dict_left = {}
        self.check_ship = []
        self.local = {}
        self.count = 0
        self.us_open = []
        self.local_comp = {}
        self.dict_right = {}
        self.all_btn_coords = []
        self.color_and_open_comp = []
        self.color_computer_buttons = []

        self.con = sqlite3.connect("sea_battle_game.db")

        self.check = False
        self.ships = {1: [], 2: [], 3: [], 4: []}
        self.k = [[False] * 10 for i in range(10)]
        self.copy_k = [[False] * 10 for i in range(10)]

        self.name, ok_pressed = QInputDialog.getText(self, "Введите имя",  # получение никнэйма игрока
                                                     "<p style='color: #2C5545;' style='font: italic bold 30px;'> "
                                                     "Введите своё "
                                                     "имя.")
        while not ok_pressed or self.name == '':
            self.name, ok_pressed = QInputDialog.getText(self, "Введите имя",
                                                         "<p style='color: #2C5545;' style='font: italic bold 30px;'> Введите "
                                                         "своё имя.")

        else:
            self.initUI()

    def initUI(self):  # Дизайн нашего приложения. Поля компьютера и игрока, другие виджеты
        self.setGeometry(400, 150, 1000, 800)
        self.setWindowTitle('Морской бой')
        for i in range(1, 11):  # генерирование полей
            for j in range(1, 11):
                self.btn = QPushButton('', self)
                self.btn.setStyleSheet("background-color: #5096AF")
                self.btn.resize(40, 40)
                self.btn.move(40 * i, 40 * j + 110)
                self.left_buttons.append(self.btn)
                self.dict_left[i, j] = self.btn
                self.local[self.btn] = (i, j)
                self.btn.clicked.connect(self.run)

                self.btn = QPushButton('', self)
                self.btn.setStyleSheet("background-color: #5096AF")
                self.btn.resize(40, 40)
                self.btn.move(40 * i + 510, 40 * j + 110)
                self.computer_buttons.append(self.btn)
                self.dict_right[i, j] = self.btn
                self.local_comp[self.btn] = (i, j)
                self.btn.clicked.connect(self.run)
                self.btn.setEnabled(False)

        self.btn = QPushButton('Выйти из игры', self)
        self.btn.setStyleSheet("background-color: #F0E891")
        self.btn.setFont(QtGui.QFont('Arial', 11, QtGui.QFont.Bold))
        self.btn.move(425, 700)
        self.btn.resize(150, 50)
        self.btn.clicked.connect(self.quit)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.displayTime)

        self.u = []
        for i in self.IQ:
            self.u.append(self.dict_left[i])

        self.copy_dict_right = self.dict_right.copy()
        self.copy_dict_left = self.dict_left.copy()
        for i in range(1, 11):
            self.label = QLabel(self)
            self.label.setText(str(i))
            self.label.move(13, 40 * i + 115)
            self.label.setFont(QtGui.QFont('Arial', 15, QtGui.QFont.Bold))

            self.label_computer = QLabel(self)
            self.label_computer.setText(str(i))
            self.label_computer.move(523, 40 * i + 115)
            self.label_computer.setFont(QtGui.QFont('Arial', 15, QtGui.QFont.Bold))

            self.label_letters = QLabel(self)
            self.label_letters.setStyleSheet("color: red")
            self.label_letters.setText(self.letters_coords[i - 1])
            self.label_letters.move(40 * i + 10, 122)
            self.label_letters.setFont(QtGui.QFont('Arial', 15, QtGui.QFont.Bold))

            self.label_computer_letters = QLabel(self)
            self.label_computer_letters.setStyleSheet("color: red")
            self.label_computer_letters.setText(self.letters_coords[i - 1])
            self.label_computer_letters.move(40 * i + 520, 122)
            self.label_computer_letters.setFont(QtGui.QFont('Arial', 15, QtGui.QFont.Bold))

        self.label = QLabel(self)
        self.label.setText("Ваше поле:")
        self.label.move(150, 70)
        self.label.setFont(QtGui.QFont('Arial', 15, QtGui.QFont.Bold))

        self.label_time = QLabel(self)
        self.label_time.setStyleSheet("color: #E59E1F;")
        self.label_time.setText("")
        self.label_time.move(315, 15)
        self.label_time.resize(500, 50)
        self.label_time.setFont(QtGui.QFont('Arial', 15, QtGui.QFont.Bold))

        self.label = QLabel(self)
        self.label.setText("Поле компьютера:")
        self.label.move(630, 70)
        self.label.setFont(QtGui.QFont('Arial', 15, QtGui.QFont.Bold))

        self.btn_start_game = QPushButton('Начинаем игру!', self)
        self.btn_start_game.setFont(QtGui.QFont('Arial', 10, QtGui.QFont.Bold))
        self.btn_start_game.resize(150, 50)
        self.btn_start_game.move(420, 50)
        self.btn_start_game.clicked.connect(self.start_game)
        self.btn_start_game.hide()

        self.btn_clear = QPushButton('Очистить поле', self)
        self.btn_clear.setFont(QtGui.QFont('Arial', 11, QtGui.QFont.Bold))
        self.btn_clear.resize(150, 50)
        self.btn_clear.move(200, 700)
        self.btn_clear.clicked.connect(self.clear_polygon)
        self.btn_clear.setStyleSheet('background-color: #FCB4D5;')

        self.remaining_cells = QLCDNumber(self)
        self.remaining_cells.resize(150, 50)
        self.remaining_cells.move(500, 600)
        self.remaining_cells.setStyleSheet('background-color: #F0AA00;')

        self.label = QLabel(self)
        self.label.setText("Закрашено клеток(из 20): ")
        self.label.move(180, 610)
        self.label.setFont(QtGui.QFont('Arial', 15, QtGui.QFont.Bold))

        self.btn_generation_ships = QPushButton('Сгенерировать корабли', self)
        self.btn_generation_ships.setFont(QtGui.QFont('Arial', 10, QtGui.QFont.Bold))
        self.btn_generation_ships.resize(230, 50)
        self.btn_generation_ships.move(120, 20)
        self.btn_generation_ships.clicked.connect(self.generate)

        self.btn_miss_motion = QPushButton('Пропустить ход', self)
        self.btn_miss_motion.setStyleSheet('background-color: #FCB4D5;')
        self.btn_miss_motion.setFont(QtGui.QFont('Arial', 11, QtGui.QFont.Bold))
        self.btn_miss_motion.move(200, 700)
        self.btn_miss_motion.resize(170, 50)
        self.btn_miss_motion.clicked.connect(self.miss_move)
        self.btn_miss_motion.hide()

        self.btn_show_sql = QPushButton('Показать все результаты', self)
        self.btn_show_sql.setFont(QtGui.QFont('Arial', 10, QtGui.QFont.Bold))
        self.btn_show_sql.setStyleSheet('background-color: #BEF574;')  # EEDC82
        self.btn_show_sql.resize(230, 50)
        self.btn_show_sql.move(650, 700)
        self.btn_show_sql.clicked.connect(self.show_sql_table)

    def show_sql_table(self): # функция вызова новой формы
        dialog = Show_results()
        dialog.exec()

    def quit(self):  # функция выхода из программы
        sys.exit(0)

    def generate(self):
        self.ships = {1: 4, 2: 3, 3: 2, 4: 1}
        self.dict_left = self.copy_dict_left.copy()
        self.dict_right = self.copy_dict_right.copy()
        self.color_buttons = []
        self.user_color_buttons = []
        self.remaining_cells.display(20)
        for i in self.left_buttons:
            i.setStyleSheet("background-color: #5096AF")
        generation_ships(self, self.dict_left)
        self.remaining_cells.setStyleSheet("background-color: #CEFF1D")
        self.btn_start_game.setStyleSheet("background-color: #CEFF1D")
        self.btn_start_game.show()

    def clear_polygon(self):  # Очистка поля игрока
        for i in self.user_color_buttons:
            self.copy_dict_left[i].setStyleSheet("background-color: #5096AF")
        self.user_color_buttons.clear()
        self.color_buttons.clear()
        self.remaining_cells.display(0)
        self.ships = {1: [], 2: [], 3: [], 4: []}
        self.k = [[False] * 10 for i in range(10)]
        self.copy_k = [[False] * 10 for i in range(10)]
        self.btn_start_game.hide()
        self.remaining_cells.setStyleSheet('background-color: #F0AA00;')

    def displayTime(self):  # Таймер, отображающий время партии
        now = QDateTime.currentDateTime().toString()
        time = now.split()[3].split(':')
        hour = int(time[0])
        minutes = int(time[1])
        seconds = int(time[2])
        self.now_seconds = hour * 3600 + minutes * 60 + seconds
        self.res_time = self.now_seconds - self.all_seconds
        if len(str(self.res_time)) == 1:
            self.label_time.setText('С начала игры прошло: 0:0' + str(self.res_time))
        else:
            if self.res_time <= 59:
                self.label_time.setText('С начала игры прошло: 0:' + str(self.res_time))
            else:
                if len(str(self.res_time % 60)) == 1:
                    self.label_time.setText(f'С начала игры прошло: {self.res_time // 60}:0{self.res_time % 60}')
                else:
                    self.label_time.setText(f'С начала игры прошло: {self.res_time // 60}:{self.res_time % 60}')

    def start_game(self):  # начало игры
        self.count_ship = []
        if len(self.user_color_buttons) == 20:
            count_ships(self, self.k)
            count_ships(self, self.copy_k)
            self.ships[1] = self.count_ship.count(1)
            self.ships[2] = self.count_ship.count(2)
            self.ships[3] = self.count_ship.count(3)
            self.ships[4] = self.count_ship.count(4)
            if self.ships == {1: 4, 2: 3, 3: 2, 4: 1} or not self.fl:
                self.btn_miss_motion.show()
                self.btn_show_sql.move(280, 620)
                self.now = QDateTime.currentDateTime().toString()
                time = self.now.split()[3].split(':')
                hour = int(time[0])
                minutes = int(time[1])
                seconds = int(time[2])
                self.all_seconds = hour * 3600 + minutes * 60 + seconds
                self.timer.start()
                self.label_time.show()
                self.btn_clear.hide()
                self.btn_start_game.hide()
                for i in range(len(self.left_buttons)):
                    self.left_buttons[i].setEnabled(False)
                self.remaining_cells.hide()
                self.label.move(550, 551)
                self.label.resize(400, 200)
                self.computer_ships = {1: 4, 2: 3, 3: 2, 4: 1}
                self.label.setAlignment(QtCore.Qt.AlignCenter)
                self.label.setText(
                    f"У компьютера осталось:\n{self.computer_ships[4]} линкор\n"
                    f"{self.computer_ships[3]} "
                    f"эсминца\n"
                    f"{self.computer_ships[2]} крейсера\n{self.computer_ships[1]} катера")

                generation_ships(self, self.dict_right)
                self.btn_generation_ships.hide()

                for i in self.computer_buttons:
                    i.setEnabled(True)
            else:
                QMessageBox.critical(self, "Error...", f"<p style='color: red;' style='font: italic bold 16px;'> "
                                                       f"Неправильное количество "
                                                       f"нужных кораблей! Должно быть: "
                                                       f"1 - 4-клеточный, 2 - 3-клеточных, 3 - 2-клеточных, "
                                                       f"4 - 1-клеточных",
                                     QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "Error...", f"<p style='color: red;' style='font: italic bold 16px;'> "
                                                   f"Невозможно "
                                                   f"начать игру! Количество "
                                                   f"закрашенных клеток не "
                                                   f"соответствует нужному — "
                                                   f"20. У Вас "
                                                   f"закрашено: {len(self.color_buttons)}",
                                 QMessageBox.Ok)

    def miss_move(self):  # функция пропустить ход
        comp_motion(self, True)

    def run(self):  # основная функция программы, отвечающая за выстрелы игрока и компьютера
        self.fl = True
        if self.sender() in self.left_buttons:
            n = self.left_buttons.index(self.sender())
            self.coord = self.local[self.sender()]
            self.flag = False
            if n in self.color_buttons:
                self.flag = True
                self.color_buttons.remove(n)
                self.user_color_buttons.remove(self.local[self.left_buttons[n]])
                self.left_buttons[n].setStyleSheet("background-color: #5096AF")
                self.k[self.coord[0] - 1][self.coord[1] - 1] = False
                self.copy_k[self.coord[1] - 1][self.coord[0] - 1] = False
                self.remaining_cells.display(len(self.color_buttons))
                if self.remaining_cells.value() == 20:
                    self.remaining_cells.setStyleSheet("background-color: #CEFF1D")
                    self.btn_start_game.setStyleSheet("background-color: #CEFF1D")
                    self.btn_start_game.show()
                else:
                    self.remaining_cells.setStyleSheet('background-color: #F0AA00;')
                    self.btn_start_game.hide()
            if len(self.color_buttons) == 0 and not self.flag:
                self.color_buttons.append(n)
                self.user_color_buttons.append(self.local[self.left_buttons[n]])
                self.k[self.coord[0] - 1][self.coord[1] - 1] = True
                self.copy_k[self.coord[1] - 1][self.coord[0] - 1] = True
                self.left_buttons[n].setStyleSheet("background-color: black")
                self.remaining_cells.display(len(self.color_buttons))
            elif len(self.color_buttons) >= 1 and not self.flag:
                self.color_buttons.sort()
                self.check = False
                if n % 10 != 0 and n % 10 != 9:
                    for i in self.color_buttons:
                        if n == i + 11 or n == i - 11 or n == i - 9 or n == i + 9:
                            self.check = True
                            break
                elif n % 10 == 0:
                    for i in self.color_buttons:
                        if n == i - 11 or n == i + 9:
                            self.check = True
                            break
                elif n % 10 == 9:
                    for i in self.color_buttons:
                        if n == i + 11 or n == i - 9:
                            self.check = True
                            break

                if not self.check:
                    if n not in self.color_buttons:
                        self.ch = False
                        self.k[self.coord[0] - 1][self.coord[1] - 1] = True
                        self.copy_k[self.coord[1] - 1][self.coord[0] - 1] = True
                        check_ships(self, self.k)
                        check_ships(self, self.copy_k)
                        if not self.ch:
                            self.all_btn_coords.append(self.coord)
                            self.color_buttons.append(n)
                            self.user_color_buttons.append(self.local[self.left_buttons[n]])
                            self.left_buttons[n].setStyleSheet("background-color: black")
                            self.remaining_cells.display(len(self.color_buttons))
                            if self.remaining_cells.value() == 20:
                                self.remaining_cells.setStyleSheet("background-color: #CEFF1D")
                                self.btn_start_game.setStyleSheet("background-color: #CEFF1D")
                                self.btn_start_game.show()
                            else:
                                self.remaining_cells.setStyleSheet('background-color: #F0AA00;')
                                self.btn_start_game.hide()
                            self.ch = False

        elif self.sender() in self.computer_buttons:
            buttonReply = ''
            cell = self.local_comp[self.sender()]
            if cell in self.color_computer_buttons:
                if cell in self.check_ship:
                    a = self.check_ship.index(cell)
                    del self.check_ship[a]
                self.sender().setStyleSheet('background-color: red')
                self.sender().setEnabled(False)
                self.open_ships.append(cell)
                self.color_and_open_comp.append(cell)
                if (cell[0] - 1, cell[1]) in self.color_computer_buttons and (
                        cell[0] - 1, cell[1]) not in self.open_ships:
                    self.check_ship.append((cell[0] - 1, cell[1]))
                if (cell[0] + 1, cell[1]) in self.color_computer_buttons and (
                        cell[0] + 1, cell[1]) not in self.open_ships:
                    self.check_ship.append((cell[0] + 1, cell[1]))
                if (cell[0], cell[1] - 1) in self.color_computer_buttons and (
                        cell[0], cell[1] - 1) not in self.open_ships:
                    self.check_ship.append((cell[0], cell[1] - 1))
                if (cell[0], cell[1] + 1) in self.color_computer_buttons and (
                        cell[0], cell[1] + 1) not in self.open_ships:
                    self.check_ship.append((cell[0], cell[1] + 1))
                if len(self.check_ship) == 0:
                    self.count = 0
                    for i in self.open_ships:
                        self.count += 1
                        check_neighbour(self, i, self.copy_dict_right, 'paint')
                    self.computer_ships[self.count] -= 1
                    if self.computer_ships[4] == 1:
                        link = f'{self.computer_ships[4]} линкор'
                    else:
                        link = f'{self.computer_ships[4]} линкоров ✅'

                    if self.computer_ships[3] == 2:
                        esm = f'{self.computer_ships[3]} эсминца'
                    elif self.computer_ships[3] == 1:
                        esm = f'{self.computer_ships[3]} эсминец'
                    else:
                        esm = f'{self.computer_ships[3]} эсминцев ✅'

                    if self.computer_ships[2] == 3 or self.computer_ships[2] == 2:
                        kreis = f'{self.computer_ships[2]} крейсера'
                    elif self.computer_ships[2] == 1:
                        kreis = f'{self.computer_ships[2]} крейсер'
                    else:
                        kreis = f'{self.computer_ships[2]} крейсеров ✅'

                    if self.computer_ships[1] == 4 or self.computer_ships[1] == 3 or self.computer_ships[1] == 2:
                        kater = f'{self.computer_ships[1]} катера'
                    elif self.computer_ships[1] == 1:
                        kater = f'{self.computer_ships[1]} катер'
                    else:
                        kater = f'{self.computer_ships[1]} катеров ✅'
                    self.label.setText(
                        f"У компьютера осталось:\n{link}\n"
                        f"{esm}"
                        f"\n"
                        f"{kreis}\n{kater}")
                    self.open_ships = []
                if len(self.color_and_open_comp) == 20:
                    self.timer.stop()
                    time = self.label_time.text().split()[4]
                    buttonReply = QMessageBox.question(self, 'Победа!!!', "<p style='color: green;' style='font: "
                                                                          "italic bold 25px;'> Вы "
                                                                          "выиграли!!!😎\nХотите начать игру заново?",
                                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if buttonReply == QMessageBox.Yes:
                        cur = self.con.cursor()
                        cur.execute(f"INSERT INTO all_games(nickname,result,time_game,world_time) VALUES('{self.name}',"
                                    f"'Победа игрока', '{time}', '{self.now}');")
                        self.con.commit()
                        clear_for_new_game(self)

                    if buttonReply == QMessageBox.No:
                        cur = self.con.cursor()
                        cur.execute(f"INSERT INTO all_games(nickname,result,time_game,world_time) VALUES('{self.name}',"
                                    f"'Победа игрока', '{time}', '{self.now}');")
                        self.con.commit()
                        clear_for_new_game(self)
                        self.con.close()
                        sys.exit(0)
            else:
                check = True
                self.sender().setStyleSheet('background-color: white')
                self.sender().setEnabled(False)
                comp_motion(self, check)


def comp_motion(self, check):  # реализация хода компьютера
    if len(self.possible) == 0:
        if len(self.u) > 0:
            x = random.choice(self.u)
            try:
                a = self.u.index(x)
                del self.u[a]
            except:
                pass
        else:
            y = []
            for i in self.left_buttons:
                if self.local[i] not in self.all and self.local[i] not in self.wrong:
                    y.append(i)
            x = random.choice(y)
    else:
        for i in self.possible:
            if i in self.wrong or i in self.open_our_ships:
                a = self.possible.index(i)
                del self.possible[a]
        del_waste(self)
        x = self.copy_dict_left[random.choice(self.possible)]
        a = self.possible.index(self.local[x])
        del self.possible[a]
    if self.local[x] in self.user_color_buttons:
        if self.local[x] in self.check_our:
            a = self.check_our.index(self.local[x])
            del self.check_our[a]
        x.setStyleSheet('background-color: red')
        try:
            a = self.u.index(x)
            del self.u[a]
        except:
            pass
        self.all.append(self.local[x])
        self.open_our_ships.append(self.local[x])
        if self.local[x] not in self.us_open:
            self.us_open.append(self.local[x])
        find_neighbour(self, self.local[x], self.copy_dict_left)
        del_waste(self)
        for i in self.possible:
            if i in self.user_color_buttons and i not in self.check_our and i not in self.all:
                self.check_our.append(i)
        for i in self.possible:
            if i in self.user_color_buttons and i not in self.all:
                check = True
                break
            else:
                check = False
        if not check:
            for i in self.open_our_ships:
                check_neighbour(self, i, self.copy_dict_left, 'our_paint')
            self.possible = []
            self.open_our_ships = []
        while check:
            del_waste(self)
            x = random.choice(self.possible)
            if x in self.user_color_buttons:
                self.copy_dict_left[x].setStyleSheet('background-color: red')
                if x not in self.us_open:
                    self.us_open.append(x)
                try:
                    a = self.u.index(self.copy_dict_left[x])
                    del self.u[a]
                except:
                    pass
                find_neighbour(self, x, self.copy_dict_left)
                del_waste(self)
                for i in self.possible:
                    if i in self.wrong or i in self.open_our_ships:
                        a = self.possible.index(i)
                        del self.possible[a]
                self.open_our_ships.append(x)
                self.all.append(x)
                for i in self.possible:
                    if i in self.user_color_buttons and i not in self.all:
                        check = True
                        break
                    else:
                        check = False
                if not check:
                    for i in self.open_our_ships:
                        check_neighbour(self, i, self.copy_dict_left, 'our_paint')
                    self.possible = []
                    self.open_our_ships = []
            else:
                self.copy_dict_left[x].setStyleSheet('background-color: white')
                try:
                    a = self.u.index(self.copy_dict_left[x])
                    del self.u[a]
                except:
                    pass
                check = False
                self.wrong.append(x)
                a = self.possible.index(x)
                del self.possible[a]
    else:
        self.wrong.append(self.local[x])
        x.setStyleSheet('background-color: white')
        try:
            a = self.u.index(self.copy_dict_left[x])
            del self.u[a]
        except:
            pass
    if len(self.us_open) == 20:
        self.timer.stop()
        time = self.label_time.text().split()[4]
        buttonReply = QMessageBox.question(self, 'Проигрыш:(',
                                           "<p style='color: red;' style='font: italic bold 25px;'> Увы, "
                                           "Вы проиграли:(😰\nХотите реванш?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute(f"INSERT INTO all_games(nickname,result,time_game,world_time) VALUES('{self.name}',"
                        f"'Победа компьютера',"
                        f"'{time}', '{self.now}');")
            self.con.commit()
            clear_for_new_game(self)

        if buttonReply == QMessageBox.No:
            cur = self.con.cursor()
            cur.execute(f"INSERT INTO all_games(nickname,result,time_game,world_time) VALUES('{self.name}',"
                        f"'Победа компьютера',"
                        f"'{time}', '{self.now}');")
            self.con.commit()
            clear_for_new_game(self)
            self.con.close()
            sys.exit(0)


def del_waste(self):  # логика игры компьютера(стрельба по ненужным клеткам невозможна)
    same = 0
    flag = -1
    if len(self.open_our_ships) >= 2:
        if self.open_our_ships[0][0] == self.open_our_ships[1][0]:
            same = self.open_our_ships[0][0]
            flag = 0
        elif self.open_our_ships[0][1] == self.open_our_ships[1][1]:
            same = self.open_our_ships[0][1]
            flag = 1
    if flag == 1:
        for i in self.possible:
            if i[1] != same:
                a = self.possible.index(i)
                del self.possible[a]
    if flag == 0:
        for i in self.possible:
            if i[0] != same:
                a = self.possible.index(i)
                del self.possible[a]


def clear_for_new_game(self):  # функция для очистки поля, приводящая все переменные в изначальный вид
    for i in self.left_buttons:
        i.setStyleSheet("background-color: #5096AF")
        i.setEnabled(True)
    for j in self.computer_buttons:
        j.setStyleSheet("background-color: #5096AF")
    self.user_color_buttons.clear()
    self.color_buttons.clear()
    self.remaining_cells.display(0)
    self.ships = {1: [], 2: [], 3: [], 4: []}
    self.k = [[False] * 10 for i in range(10)]
    self.copy_k = [[False] * 10 for i in range(10)]
    self.btn_start_game.hide()
    self.remaining_cells.setStyleSheet('background-color: #F0AA00;')
    self.btn_miss_motion.hide()

    self.label.setText("Закрашено клеток(из 20): ")
    self.label.move(140, 525)
    self.label.setFont(QtGui.QFont('Arial', 15, QtGui.QFont.Bold))
    self.btn_generation_ships.show()
    self.remaining_cells.show()
    self.btn_clear.show()
    self.label_time.hide()
    self.wrong.clear()
    self.all.clear()
    self.color_computer_buttons.clear()
    self.us_open.clear()
    self.color_and_open_comp.clear()
    self.open_ships.clear()


def generation_ships(self, dictionary):  # функция, отвечающая за генерацию кораблей
    self.fl = False
    self.possible = []
    self.possible_second = []
    while len(self.possible) == 0 or len(self.possible_second) == 0 or len(self.possible_third) == 0:  # генерация
        # четырехпалуюного корабля
        self.possible = []
        self.possible_second = []
        self.possible_third = []
        self.first_cell = random.choice([i for i in dictionary.keys()])
        find_neighbour(self, self.first_cell, dictionary)
        if len(self.possible) > 0:
            self.second_cell = random.choice(self.possible)
            find_neighboor_for_third(self, self.first_cell, self.second_cell, dictionary)
            if len(self.possible_second) > 0:
                self.third_cell = random.choice(self.possible_second)
                find_neighboor_for_fourth(self, self.second_cell, self.third_cell, dictionary)
                if len(self.possible_third) > 0:
                    self.fourth_cell = random.choice(self.possible_third)
                    if dictionary != self.dict_right:
                        dictionary[self.first_cell].setStyleSheet("background-color: black")
                        dictionary[self.second_cell].setStyleSheet("background-color: black")
                        dictionary[self.third_cell].setStyleSheet("background-color: black")
                        dictionary[self.fourth_cell].setStyleSheet("background-color: black")
                        self.user_color_buttons.append(self.first_cell)
                        self.user_color_buttons.append(self.second_cell)
                        self.user_color_buttons.append(self.third_cell)
                        self.user_color_buttons.append(self.fourth_cell)
                    else:
                        self.color_computer_buttons.append(self.first_cell)
                        self.color_computer_buttons.append(self.second_cell)
                        self.color_computer_buttons.append(self.third_cell)
                        self.color_computer_buttons.append(self.fourth_cell)
                    check_neighbour(self, self.first_cell, dictionary, 'del')
                    check_neighbour(self, self.second_cell, dictionary, 'del')
                    check_neighbour(self, self.third_cell, dictionary, 'del')
                    check_neighbour(self, self.fourth_cell, dictionary, 'del')
    for i in range(2):  # генерация трехпалубных кораблей
        self.possible = []
        self.possible_second = []
        while len(self.possible) == 0 or len(self.possible_second) == 0:
            self.possible = []
            self.possible_second = []
            self.first_cell = random.choice([i for i in dictionary.keys()])
            find_neighbour(self, self.first_cell, dictionary)
            if len(self.possible) > 0:
                self.second_cell = random.choice(self.possible)
                find_neighboor_for_third(self, self.first_cell, self.second_cell, dictionary)
                if len(self.possible_second) > 0:
                    self.third_cell = random.choice(self.possible_second)
                    if dictionary != self.dict_right:
                        dictionary[self.first_cell].setStyleSheet("background-color: black")
                        dictionary[self.second_cell].setStyleSheet("background-color: black")
                        dictionary[self.third_cell].setStyleSheet("background-color: black")
                        self.user_color_buttons.append(self.first_cell)
                        self.user_color_buttons.append(self.second_cell)
                        self.user_color_buttons.append(self.third_cell)
                    else:
                        self.color_computer_buttons.append(self.first_cell)
                        self.color_computer_buttons.append(self.second_cell)
                        self.color_computer_buttons.append(self.third_cell)
                    check_neighbour(self, self.first_cell, dictionary, 'del')
                    check_neighbour(self, self.second_cell, dictionary, 'del')
                    check_neighbour(self, self.third_cell, dictionary, 'del')
    for i in range(3):  # генерация двухпалубных кораблей
        self.possible = []
        while len(self.possible) == 0:
            self.first_cell = random.choice([i for i in dictionary.keys()])
            find_neighbour(self, self.first_cell, dictionary)
            if len(self.possible) > 0:
                self.second_cell = random.choice(self.possible)
                if dictionary != self.dict_right:
                    dictionary[self.first_cell].setStyleSheet("background-color: black")
                    dictionary[self.second_cell].setStyleSheet("background-color: black")
                    self.user_color_buttons.append(self.first_cell)
                    self.user_color_buttons.append(self.second_cell)
                else:
                    self.color_computer_buttons.append(self.first_cell)
                    self.color_computer_buttons.append(self.second_cell)
                check_neighbour(self, self.first_cell, dictionary, 'del')
                check_neighbour(self, self.second_cell, dictionary, 'del')
    for i in range(4):  # генерация однопалубных кораблей
        self.one_cell = random.choice([i for i in dictionary.keys()])
        check_neighbour(self, self.one_cell, dictionary, 'del')
        if dictionary != self.dict_right:
            dictionary[self.one_cell].setStyleSheet("background-color: black")
            self.user_color_buttons.append(self.one_cell)
        else:
            self.color_computer_buttons.append(self.one_cell)
        del dictionary[self.one_cell]
    self.possible = []


def find_neighboor_for_fourth(self, cell_second, cell_third, dictionary):  # функция, нахождения соседних клеток с
    # четырехпалубным кораблем
    if cell_third[0] == cell_second[0]:
        if cell_third[1] == cell_second[1] + 1:
            if (cell_third[0], cell_third[1] + 1) in dictionary:
                self.possible_third.append((cell_third[0], cell_third[1] + 1))
            if (cell_third[0], cell_third[1] - 3) in dictionary:
                self.possible_third.append((cell_third[0], cell_third[1] - 3))
        elif cell_third[1] == cell_second[1] - 1:
            if (cell_third[0], cell_third[1] - 1) in dictionary:
                self.possible_third.append((cell_third[0], cell_third[1] - 1))
            if (cell_third[0], cell_third[1] + 3) in dictionary:
                self.possible_third.append((cell_third[0], cell_third[1] + 3))
    if cell_third[1] == cell_second[1]:
        if cell_third[0] == cell_second[0] + 1:
            if (cell_third[0] + 1, cell_third[1]) in dictionary:
                self.possible_third.append((cell_third[0] + 1, cell_third[1]))
            if (cell_third[0] - 3, cell_third[1]) in dictionary:
                self.possible_third.append((cell_third[0] - 3, cell_third[1]))
        elif cell_third[0] == cell_second[0] - 1:
            if (cell_third[0] - 1, cell_third[1]) in dictionary:
                self.possible_third.append((cell_third[0] - 1, cell_third[1]))
            if (cell_third[0] + 3, cell_third[1]) in dictionary:
                self.possible_third.append((cell_third[0] + 3, cell_third[1]))


def find_neighboor_for_third(self, cell_first, cell_second, dictionary):  # функция, нахождения соседних клеток с
    # трехпалубным кораблем
    if cell_first[0] == cell_second[0]:
        if cell_second[1] == cell_first[1] + 1:
            if (cell_second[0], cell_second[1] + 1) in dictionary:
                self.possible_second.append((cell_second[0], cell_second[1] + 1))
            if (cell_second[0], cell_second[1] - 2) in dictionary:
                self.possible_second.append((cell_second[0], cell_second[1] - 2))
        else:
            if (cell_second[0], cell_second[1] - 1) in dictionary:
                self.possible_second.append((cell_second[0], cell_second[1] - 1))
            if (cell_second[0], cell_second[1] + 2) in dictionary:
                self.possible_second.append((cell_second[0], cell_second[1] + 2))
    if cell_first[1] == cell_second[1]:
        if cell_second[0] == cell_first[0] + 1:
            if (cell_second[0] + 1, cell_second[1]) in dictionary:
                self.possible_second.append((cell_second[0] + 1, cell_second[1]))
            if (cell_second[0] - 2, cell_second[1]) in dictionary:
                self.possible_second.append((cell_second[0] - 2, cell_second[1]))
        else:
            if (cell_second[0] - 1, cell_second[1]) in dictionary:
                self.possible_second.append((cell_second[0] - 1, cell_second[1]))
            if (cell_second[0] + 2, cell_second[1]) in dictionary:
                self.possible_second.append((cell_second[0] + 2, cell_second[1]))


def find_neighbour(self, cell, dictionary):  # нахождение соседей с клеткой, граничащие по стороне
    if (cell[0] - 1, cell[1]) in dictionary:
        self.possible.append((cell[0] - 1, cell[1]))
    if (cell[0] + 1, cell[1]) in dictionary:
        self.possible.append((cell[0] + 1, cell[1]))
    if (cell[0], cell[1] - 1) in dictionary:
        self.possible.append((cell[0], cell[1] - 1))
    if (cell[0], cell[1] + 1) in dictionary:
        self.possible.append((cell[0], cell[1] + 1))


def try_del(self, cell, dictionary, action):  # закрашивание соседних клеток при затоплении корабля
    try:
        if action == 'del':
            del dictionary[cell]
        elif action == 'paint':
            if cell not in self.open_ships:
                dictionary[cell].setStyleSheet("background-color: white")
                dictionary[cell].setEnabled(False)
        elif action == 'our_paint':
            if cell not in self.open_our_ships:
                dictionary[cell].setStyleSheet("background-color: white")
                self.wrong.append(cell)
                if self.copy_dict_left[cell] in self.u:
                    a = self.u.index(self.copy_dict_left[cell])
                    del self.u[a]
    except KeyError:
        pass


def check_neighbour(self, x, dictionary, action):  # функция, нахождения 'соседей' для данной клетки
    try_del(self, (x[0], x[1] - 1), dictionary, action)
    try_del(self, (x[0], x[1] + 1), dictionary, action)
    try_del(self, (x[0] - 1, x[1]), dictionary, action)
    try_del(self, (x[0] + 1, x[1]), dictionary, action)
    try_del(self, (x[0] + 1, x[1] - 1), dictionary, action)
    try_del(self, (x[0] + 1, x[1] + 1), dictionary, action)
    try_del(self, (x[0] - 1, x[1] - 1), dictionary, action)
    try_del(self, (x[0] - 1, x[1] + 1), dictionary, action)


def count_ships(self, bottoms):  # функция подсчета кораблей
    for i in range(len(bottoms)):
        count = 0
        for j in range(len(bottoms[i])):
            if (i != 0 and i != len(bottoms) - 1 and bottoms[i][j] and
                not bottoms[i + 1][j] and
                not bottoms[i - 1][j]) or (i == 0 and bottoms[i][j] and
                                           not bottoms[i + 1][j]) or (
                    i == len(bottoms) - 1 and bottoms[i][j] and not bottoms[i - 1][j]):
                count += 1
            elif count != 0:
                if count == 1 and bottoms == self.k:
                    count = 0
                elif count == 1 and bottoms == self.copy_k:
                    self.count_ship.append(count)
                    count = 0
                else:
                    self.count_ship.append(count)
                    count = 0
            if j == len(bottoms[i]) - 1 and count != 0:
                if count == 1 and bottoms == self.copy_k:
                    self.count_ship.append(count)
                    count = 0
                elif count == 1 and bottoms == self.k:
                    count = 0
                elif count > 1:
                    self.count_ship.append(count)


def check_ships(self, mass):  # второстепенная функция для подсчета кораблей
    for i in mass:
        self.count_tr = 0
        for j in i:
            if j:
                if self.count_tr == 4:
                    self.ch = True
                    if mass == self.k:
                        mass[self.coord[0] - 1][self.coord[1] - 1] = False
                    else:
                        mass[self.coord[1] - 1][self.coord[0] - 1] = False
                    break
                else:
                    self.count_tr += 1
            if not j:
                self.count_tr = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())