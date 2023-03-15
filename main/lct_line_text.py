import sys

from resizable_rect import ResizableRect
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
        left_separator = Separator(0, 0, 20, rect, get_points(text.point_list))
        right_separator = Separator(0, 0, 20, rect, get_points(text.point_list))

        custom_pen = QPen(Qt.black)
        custom_pen.setWidth(5)
        left_separator.setPen(custom_pen)
        right_separator.setPen(custom_pen)
        left_separator.setPos(200, 100)
        right_separator.setPos(400, 300)

        # rou = ResizableRect(20, 5, rect)
        #self.scene.addItem(rou)
        #rou.init_separators((left_separator, right_separator))
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.button)
        hbox.addWidget(view)

        self.setLayout(hbox)

    def show_new_window(self):
        pass


app = QApplication(sys.argv)

w = Window()
w.show()

app.exec()
