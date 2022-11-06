import csv
import sys
from random import randint

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 580, 310))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(340, 330, 60, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(390, 330, 200, 20))
        self.lineEdit.setAcceptDrops(True)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 330, 110, 20))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(
            _translate("MainWindow", "Осторожно: дорого!")
        )
        self.label.setText(_translate("MainWindow", "Итого:"))
        self.pushButton.setText(_translate("MainWindow", "Обновить"))


class Program(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loadTable('price.csv')
        self.update_color()
        self.tableWidget.cellChanged.connect(self.set_total)
        self.pushButton.clicked.connect(self.start_update)

    def loadTable(self, table_name):
        with open(table_name, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            title = next(reader) + ['Количество']
            self.tableWidget.setColumnCount(len(title))
            self.tableWidget.setHorizontalHeaderLabels(title)
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(
                sorted(reader, key=lambda x: int(x[1]), reverse=True)
            ):
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row + ['0']):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(elem))

    def start_update(self):
        self.set_total()
        self.update_color()

    def update_color(self):
        for i in range(5):
            color = QColor(randint(0, 255), randint(0, 255), randint(0, 255))
            self.color_row(i, color)

    def color_row(self, row, color):
        for i in range(self.tableWidget.columnCount()):
            self.tableWidget.item(row, i).setBackground(color)

    def set_total(self):
        total = 0
        j = self.tableWidget.columnCount() - 1
        for i in range(self.tableWidget.rowCount()):
            total += int(self.tableWidget.item(i, j - 1).text()) * int(
                self.tableWidget.item(i, j).text()
            )
        self.lineEdit.setText(str(total))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Program()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
