import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow

SCREEN_SIZE = [400, 500]


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(*SCREEN_SIZE)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 10, 60, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(160, 40, 60, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(160, 70, 60, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_1.setGeometry(QtCore.QRect(220, 10, 113, 21))
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(220, 40, 113, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(220, 70, 113, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 24))
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
            _translate("MainWindow", "Квадрат объектив 1")
        )
        self.pushButton.setText(_translate("MainWindow", "Показать"))
        self.label.setText(_translate("MainWindow", "side"))
        self.label_2.setText(_translate("MainWindow", "coeff"))
        self.label_3.setText(_translate("MainWindow", "n"))


class Program(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.do_paint = False
        self.pushButton.clicked.connect(self.paint)

    def paintEvent(self, event):
        if self.do_paint:
            qp = QPainter()
            qp.begin(self)
            self.draw_boxes(qp)
            qp.end()
            self.do_paint = False

    def paint(self):
        self.do_paint = True
        self.repaint()

    def xs(self, x):
        return x + SCREEN_SIZE[0] // 2

    def ys(self, y):
        return SCREEN_SIZE[1] // 2 - y + 50

    def draw_boxes(self, qp: QPainter):
        side = int(self.lineEdit_1.text())
        coeff = float(self.lineEdit_2.text())
        n = int(self.lineEdit_3.text())
        list_of_nodes = [
            (
                (side / 2, side / 2),
                (side / 2, -side / 2),
                (-side / 2, -side / 2),
                (-side / 2, side / 2),
            )
        ]
        for _ in range(n - 1):
            list_of_nodes.append(
                (
                    (
                        list_of_nodes[-1][0][0] * coeff,
                        list_of_nodes[-1][0][1] * coeff,
                    ),
                    (
                        list_of_nodes[-1][1][0] * coeff,
                        list_of_nodes[-1][1][1] * coeff,
                    ),
                    (
                        list_of_nodes[-1][2][0] * coeff,
                        list_of_nodes[-1][2][1] * coeff,
                    ),
                    (
                        list_of_nodes[-1][3][0] * coeff,
                        list_of_nodes[-1][3][1] * coeff,
                    ),
                )
            )
        list_of_nodes2 = [
            (
                (int(self.xs(nodes[0][0])), int(self.ys(nodes[0][1]))),
                (int(self.xs(nodes[1][0])), int(self.ys(nodes[1][1]))),
                (int(self.xs(nodes[2][0])), int(self.ys(nodes[2][1]))),
                (int(self.xs(nodes[3][0])), int(self.ys(nodes[3][1]))),
            )
            for nodes in list_of_nodes
        ]
        pen = QPen(Qt.red, 2)
        qp.setPen(pen)
        for nodes2 in list_of_nodes2:
            for i in range(-1, len(nodes2) - 1):
                qp.drawLine(*nodes2[i], *nodes2[i + 1])


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Program()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
