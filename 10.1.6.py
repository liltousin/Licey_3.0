import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(730, 370)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 10, 201, 26))
        self.comboBox.setObjectName("comboBox")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(60, 50, 100, 50))
        self.pushButton.setObjectName("pushButton")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(220, 10, 500, 300))
        self.tableView.setObjectName("tableView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 730, 24))
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
            _translate("MainWindow", "Фильтрация по жанрам")
        )
        self.pushButton.setText(_translate("MainWindow", "Пуск"))


class Program(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loadTable()
        self.pushButton.clicked.connect(self.select_data)

    def loadTable(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        # Укажем имя базы данных
        db.setDatabaseName('films_db.sqlite')
        # И откроем подключение
        db.open()

        combo_model = QSqlTableModel(self, db)
        combo_model.setTable('genres')
        combo_model.select()

        self.comboBox.setModel(combo_model)
        self.comboBox.setModelColumn(combo_model.fieldIndex("title"))

        self.model = QSqlTableModel(self, db)
        self.model.setTable('films')
        self.model.select()
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Название")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Год")
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Жанр")

        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().moveSection(2, 3)
        self.tableView.setColumnHidden(0, True)
        self.tableView.setColumnHidden(4, True)

    def select_data(self):
        self.model.setFilter(f'genre = {self.comboBox.currentIndex() + 1}')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Program()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
