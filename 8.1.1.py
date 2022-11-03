import sys

from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow

SCREEN_SIZE = [400, 400]


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(*SCREEN_SIZE)

        self.fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[
            0
        ]

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 100, 300))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_1 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_1.setObjectName("pushButton_1")
        self.buttonGroup_1 = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup_1.setObjectName("buttonGroup_1")
        self.buttonGroup_1.addButton(self.pushButton_1)
        self.verticalLayout.addWidget(self.pushButton_1)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.buttonGroup_1.addButton(self.pushButton_2)
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.buttonGroup_1.addButton(self.pushButton_3)
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.buttonGroup_1.addButton(self.pushButton_4)
        self.verticalLayout.addWidget(self.pushButton_4)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 0, 300, 300))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(self.fname))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 300, 400, 60))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget
        )
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_5 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.buttonGroup_2 = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup_2.setObjectName("buttonGroup_2")
        self.buttonGroup_2.addButton(self.pushButton_5)
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.pushButton_6 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.buttonGroup_2.addButton(self.pushButton_6)
        self.horizontalLayout.addWidget(self.pushButton_6)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_1.setText(_translate("MainWindow", "R"))
        self.pushButton_2.setText(_translate("MainWindow", "G"))
        self.pushButton_3.setText(_translate("MainWindow", "B"))
        self.pushButton_4.setText(_translate("MainWindow", "ALL"))
        self.pushButton_5.setText(
            _translate("MainWindow", "Против часовой стрелки")
        )
        self.pushButton_6.setText(
            _translate("MainWindow", "По часовой стрелке")
        )


class Program(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.oim = Image.open(self.fname)
        self.filter = 'ALL'
        self.trans = 0
        self.buttonGroup_1.buttonClicked.connect(self.recolor)
        self.buttonGroup_2.buttonClicked.connect(self.povernut)

    def povernut(self, btn):
        if btn == self.pushButton_5:
            self.trans += 1
        else:
            self.trans += 3
        self.change_im()

    def recolor(self, btn):
        self.filter = btn.text()
        self.change_im()

    def change_im(self):
        im = self.oim.copy()
        for _ in range(self.trans % 4):
            im = im.transpose(Image.Transpose.ROTATE_90)
        pixels = im.load()
        x, y = im.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = rgb_choice(r, g, b, self.filter)
        im.save(self.fname)
        im.close()
        self.label.setPixmap(QtGui.QPixmap(self.fname))
        self.oim.save(self.fname)


def rgb_choice(r, g, b, text):
    if text == 'R':
        return r, 0, 0
    elif text == 'G':
        return 0, g, 0
    elif text == 'B':
        return 0, 0, b
    return r, g, b


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Program()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
