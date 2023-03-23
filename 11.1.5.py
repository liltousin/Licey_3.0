import sqlite3
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(220, 30, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(330, 30, 113, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 90, 570, 250))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 10, 200, 70))
        self.textEdit.setObjectName("textEdit")
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
            _translate("MainWindow", "Генерация фильмов")
        )
        self.pushButton.setText(_translate("MainWindow", "Запуск"))
        self.pushButton_2.setText(_translate("MainWindow", "Изменить"))
        self.textEdit.setHtml(
            _translate(
                "MainWindow",
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" "
                "\"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" />"
                "<style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'."
                "AppleSystemUIFont\'; font-size:13pt; font-weight:400; "
                "font-style:normal;\">\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; "
                "margin-left:0px; margin-right:0px; -qt-block-indent:0; "
                "text-indent:0px;\">id = 11</p></body></html>",
            )
        )


class Program(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("films_db.sqlite")
        self.pushButton.clicked.connect(self.load_data)
        self.pushButton_2.clicked.connect(self.change_data)

    def load_data(self):
        cur = self.con.cursor()
        query = 'SELECT * FROM Films WHERE ' + self.textEdit.toPlainText()
        try:
            result = cur.execute(query).fetchall()
        except sqlite3.OperationalError:
            self.statusBar().showMessage('Неверный запрос')
            self.tableWidget.setRowCount(0)
            return
        self.tableWidget.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        self.statusBar().showMessage('')
        self.tableWidget.setColumnCount(len(result[0]))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def change_data(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        if not rows:
            return
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        valid = QMessageBox.question(
            self,
            '',
            "Действительно заменить элементы с id " + ",".join(ids),
            QMessageBox.Yes,
            QMessageBox.No,
        )
        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            data = cur.execute(
                "SELECT * FROM films WHERE id IN ("
                + ", ".join('?' * len(ids))
                + ")",
                ids,
            ).fetchall()
            cur.execute(
                "DELETE FROM films WHERE id IN ("
                + ", ".join('?' * len(ids))
                + ")",
                ids,
            )
            for row in data:
                cur.execute(
                    "INSERT INTO Films VALUES("
                    + ", ".join('?' * len(row))
                    + ")",
                    [row[0], row[1][::-1], row[2] + 1000, row[3], row[4] * 2],
                )
            self.con.commit()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Program()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
