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
        self.verticalSlider = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider.setGeometry(QtCore.QRect(20, 20, 20, 300))
        self.verticalSlider.setMaximum(100)
        self.verticalSlider.setProperty("value", 100)
        self.verticalSlider.setTracking(True)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 50, 250, 250))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(self.fname))
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
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
            _translate("MainWindow", "Изменение прозрачности")
        )


class Program(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.oim = Image.open(self.fname)
        self.verticalSlider.valueChanged.connect(self.change_trans)

    def change_trans(self):
        value = int(self.sender().value())
        im = self.oim.copy()
        im.putalpha(255 * value // 100)
        im.save(self.fname)
        im.close()
        self.label.setPixmap(QtGui.QPixmap(self.fname))
        self.oim.save(self.fname)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Program()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
