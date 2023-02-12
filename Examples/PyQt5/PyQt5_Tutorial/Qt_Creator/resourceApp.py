import sys

from PyQt5 import QtGui, QtWidgets

import resources

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hello World")
        self.button = QtWidgets.QPushButton("My button")

        icon = QtGui.QIcon(":/icons/penguin.png")
        self.button.setIcon(icon)
        self.button.clicked.connect(self.change_icon)

        self.setCentralWidget(self.button)

        self.show()

    def change_icon(self):
        icon = QtGui.QIcon(":/icons/monkey.png")
        self.button.setIcon(icon)


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()