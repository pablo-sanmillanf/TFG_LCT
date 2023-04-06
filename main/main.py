import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow

)
from mainWindow import Ui_MainWindow

COLORS = [
    "lavender",
    "gold",
    "goldenrod",
    "yellow",
    "orange",
    "red",
    "sienna",
    "firebrick",
    "deeppink",
    "magenta",
    "orangered",
    "brown",
    "yellowgreen",
    "chocolate",
    "coral",
    "papayawhip",
    "bisque",
]


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.textHandler.setup(10, 10, 500, 500, open("text.txt", "r").read(), 13, COLORS)

    """
        self.buttonT = QPushButton("Get Text")
        self.buttonT.clicked.connect(self.text_action)
        hbox = QHBoxLayout(self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.buttonT)

        hbox.addLayout(vbox)
        hbox.addWidget(self.handler)

        self.setLayout(hbox)

    def text_action(self):
        print(self.handler.get_text_classified())
        self.handler.set_text_size(20)
    """


app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec()
