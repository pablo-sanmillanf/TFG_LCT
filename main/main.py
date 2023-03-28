import sys
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QWidget, QVBoxLayout,

)
from text_handler import TextHandler


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.handler = TextHandler(20, 20, 500, 500,
                                   "In this tutorial we'll learn how to use PyQt to create "
                                   "desktop applications with Python. First we'll create a "
                                   "series of simple windows on your desktop to ensure that"
                                   " PyQt is working and introduce some of the basic concepts. <br>"
                                   " Then we'll take a brief look at the event loop and how"
                                   " it relates to GUI programming in Python.", 13)

        self.buttonS = QPushButton("Split")
        self.buttonS.clicked.connect(self.split_action)

        self.buttonJ = QPushButton("Join")
        self.buttonJ.clicked.connect(self.join_action)

        self.buttonT = QPushButton("Get Text")
        self.buttonT.clicked.connect(self.text_action)
        hbox = QHBoxLayout(self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.buttonS)
        vbox.addWidget(self.buttonJ)
        vbox.addWidget(self.buttonT)

        hbox.addLayout(vbox)
        hbox.addWidget(self.handler)

        self.setLayout(hbox)

    def split_action(self):
        print("Split", self.handler.split(100, 100))

    def join_action(self):
        print("Join", self.handler.join(100, 100))

    def text_action(self):
        print(self.handler.get_text_classified())
        self.handler.change_text_size(10)


app = QApplication(sys.argv)

w = Window()
w.show()

app.exec()
