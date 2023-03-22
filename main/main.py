import sys

from PyQt5 import QtGui

from custom_text import CustomText

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

from text_classifier import TextClassifier


def get_points(tuple_list):
    return [(i[0], [e[0] for e in i[1]]) for i in tuple_list]


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Defining a scene rect of 400x200, with it's origin at 0,0.
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

        text = CustomText("In this tutorial we'll learn how to use PyQt to create "
                          "desktop applications with Python. First we'll create a "
                          "series of simple windows on your desktop to ensure that"
                          " PyQt is working and introduce some of the basic concepts. <br>"
                          " Then we'll take a brief look at the event loop and how"
                          " it relates to GUI programming in Python.", 300, rect, font)
        self.scene.addItem(text)

        self.classifier = TextClassifier(500, 20, get_points(text.point_list), "SD~;SG~", rect)
        custom_pen = QPen(Qt.black)
        custom_pen.setWidth(5)
        self.classifier.set_separator_pen(custom_pen)

        self.buttonS = QPushButton("Split")
        self.buttonS.clicked.connect(self.split_action)

        self.buttonJ = QPushButton("Join")
        self.buttonJ.clicked.connect(self.join_action)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.buttonS)
        hbox.addWidget(self.buttonJ)
        hbox.addWidget(view)

        self.setLayout(hbox)

    def split_action(self):
        print("Split", self.classifier.split(100, 100))

    def join_action(self):
        brush = QBrush(Qt.red)
        print("Join", self.classifier.join(100, 100))
        self.classifier.set_rects_brush(brush)


app = QApplication(sys.argv)

w = Window()
w.show()

app.exec()
