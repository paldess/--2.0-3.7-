from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys

Form, _ = uic.loadUiType("window_main_2.ui")


def error():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Неверные данные!")
    msg.setInformativeText('Проверьте введенные параметры')
    msg.setWindowTitle("Ошибка")
    msg.exec_()


class Ui(QtWidgets.QMainWindow, Form):
    def __init__(self):
        super(Ui, self).__init__()
        self.total = 0
        self.x = 0
        self.time_ust_zam = 0
        self.time_obr = 0
        self.setupUi(self)
        self.exit.clicked.connect(self.ex)  # выход
        self.add.clicked.connect(self.viewe)  # добавить
        self.clear_list.clicked.connect(self.clear)  # очистить
        self.raschet_2.clicked.connect(self.ras_nar)  # предварительный расчетнаружней обработки
        self.new_2.clicked.connect(self.viewe_new)  # обновление данных установки и замера
        self.raschet.clicked.connect(self.ras_nar_n)  # предварительный расчет внутренней обработки

    def clear(self):  # очистить
        self.list_result.clear()
        self.x = 0
        self.total = 0
        self.predvar.setText('0')

    def viewe_new(self):  # обновление данных установки и замера
        try:
            if float(self.ustanovka.text()) <= 0 or float(self.zamer.text()) <= 0:
                raise ValueError
            result = self.total + float(self.ustanovka.text()) + float(self.zamer.text())
            self.total_time.setText(str(round(result, 2)))
        except ValueError:
            error()

    def viewe(self):  # добавить в расчеты
        try:
            if float(self.ustanovka.text()) <= 0 or float(self.zamer.text()) <= 0:
                raise ValueError
            self.x += 1
            self.list_result.addItem(str(self.x) + '-' + str(self.time_obr) + 'мин'
                                     + ' --- ф' + str(self.max_n.text())
                                     + 'xф' + str(self.min_n.text())
                                     + 'x' + str(self.light_n.text()))
            self.total += self.time_obr
            result = self.total + float(self.ustanovka.text()) + float(self.zamer.text())
            self.total_time.setText(str(round(result, 2)))
        except ValueError:
            error()

    def ex(self):
        exit(0)

    def ras_nar(self):  # расчет по данным(предварительный) наружняя обработка
        try:
            if int(self.max_n.text()) <= 0 or int(self.light_n.text()) <= 0 or int(self.polnota_n.text()) <= 0 or int(
                    self.min_n.text()) <= 0:
                raise ValueError
            x = 180000 if self.steel_2.isChecked() else 380000
            n = round(x / 3.14 / int(self.max_n.text()), 2)                      # обороты шпинделя
            n = 1200 if n > 1200 else n                                         # ограничение максимальных
            n = 200 if n < 200 else n                                            # ограничение минимальных
            n = n * 0.2                                                         # подача в мм/мин
            torec = int(self.max_n.text()) / n * int(self.spinBox.value()) if self.torec.isChecked() else 0

            self.time_obr = round((int(self.light_n.text()) / n) \
                                  * ((int(self.max_n.text()) - int(self.min_n.text()))  # вычисление времени обработки
                                     / 4) / 100 * int(self.polnota_n.text()) + torec, 2)

            self.predvar.setText(str(self.time_obr))
        except ValueError:
            error()

    def ras_nar_n(self):  # расчет по данным(предварительный) внутренняя обработка
        try:
            if int(self.max_n.text()) <= 0 or int(self.light_n.text()) <= 0 or int(self.polnota_n.text()) <= 0 or int(
                    self.min_n.text()) <= 0:
                raise ValueError
            x = 180000 if self.steel.isChecked() else 380000
            n = round(x / 3.14 / int(self.max.text()), 2)        # обороты шпинделя
            n = 1200 if n > 1200 else n                         # ограничение максимальных
            n = 200 if n < 200 else n                            # ограничение минимальных
            n = n * 0.2                                         # подача в мм/мин
            sverlo = int(self.sverl_gl.text()) / 30 if self.sverl.isChecked() else 0
            if int(self.sverl_gl.text()) < 0:
                raise ValueError
            self.time_obr = round((int(self.light.text()) / n) \
                                  * ((int(self.max.text()) - int(self.min.text()))  # вычисление времени обработки
                                     / 4) / 100 * int(self.polnota_n.text()) + sverlo, 2)

            self.predvar.setText(str(self.time_obr))
        except ValueError:
            error()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    w.show()
    sys.exit(app.exec_())