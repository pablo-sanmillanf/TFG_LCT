import sys

from resizable_rect import MultilineRoundedRect
from custom_text import CustomText
from separator import Separator

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QFont
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

        self.classifier = TextClassifier(20, get_points(text.point_list), rect)
        custom_pen = QPen(Qt.black)
        custom_pen.setWidth(5)
        self.classifier.set_separator_pen(custom_pen)

        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.button)
        hbox.addWidget(view)

        self.setLayout(hbox)

    def show_new_window(self):
        print(self.classifier.split(100, 100))


app = QApplication(sys.argv)

w = Window()
w.show()

app.exec()
