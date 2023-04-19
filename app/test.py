import sys
from main_window_aux_items.main_text import MainText

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QFont, QBrush
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QPushButton,
    QWidget,

)

from main_window_aux_items.classifier import Classifier

COLORS = [
    "#ff0000",
    "blue",
    "blue",
    "blue",
    "blue",
    "green",
    "green",
    "green",
    "green",
    "white",
    "white",
    "white",
    "white",
    "yellow",
    "yellow",
    "yellow",
    "yellow"
]


def get_points(tuple_list):
    return [(i[0], [e[0] for e in i[1]]) for i in tuple_list]


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Defining a scene rounded_rect of 400x200, with it's origin at 0,0.
        # If we don't set this on creation, we can set it later with .setSceneRect
        self.scene = QGraphicsScene(0, 0, 500, 500)

        view = QGraphicsView(self.scene)
        view.setRenderHint(QPainter.Antialiasing)
        view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        view.setMinimumSize(502, 502)

        rect = QGraphicsRectItem(0, 0, 500, 500)
        pen = QPen(Qt.green)
        pen.setWidth(5)
        rect.setPen(pen)
        self.scene.addItem(rect)

        font = QFont()
        font.setFamily('Times')
        font.setBold(True)
        font.setPointSize(10)

        self.classifier = Classifier("In this tutorial we'll learn how to use PyQt to create "
                                     "desktop applications with Python. First we'll create a "
                                     "series of simple windows on your desktop to ensure that"
                                     " PyQt is working and introduce some of the basic concepts. <br>"
                                     " Then we'll take a brief look at the event loop and how"
                                     " it relates to GUI programming in Python.", 500, 13, "SD~;SG~", COLORS, rect)

        self.buttonS = QPushButton("Split")
        self.buttonS.clicked.connect(self.split_action)

        self.buttonJ = QPushButton("Join")
        self.buttonJ.clicked.connect(self.join_action)

        self.buttonA = QPushButton("Action")
        self.buttonA.clicked.connect(self.action)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.buttonS)
        hbox.addWidget(self.buttonJ)
        hbox.addWidget(self.buttonA)
        hbox.addWidget(view)

        self.setLayout(hbox)

    def split_action(self):
        self.classifier.split(100, 300)

    def join_action(self):
        print("Join", self.classifier.join(100, 300))

    def action(self):
        print(self.classifier.get_text_analyzed())


app = QApplication(sys.argv)

w = Window()
w.show()

app.exec()
