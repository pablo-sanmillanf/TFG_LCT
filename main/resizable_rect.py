import typing

import numpy as np

from PyQt5.QtCore import QPointF, QEvent
from PyQt5.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsSceneMouseEvent,
    QWidget,
    QStyleOptionGraphicsItem,
)
from PyQt5 import QtGui


def find_nearest_point(candidate_points, point_reference):
    min_dist = 50000
    final_point = None
    for point in candidate_points:
        distance = np.abs(point_reference.x() - point.x())
        if min_dist > distance:
            min_dist = distance
            final_point = point
    return final_point


class RoundedRect(QGraphicsRectItem):
    """
    This class has the same behavior as QGraphicsRectItem except that
    it paints the rectangle with rounded corners, with a rounding radius,
    passed as a parameter in the constructor.
    """
    def __init__(self, x, y, width, height, radius, *args, **kwargs):
        super().__init__(x, y, width, height, *args, **kwargs)
        self.radius = radius

    def paint(self,
              painter: QtGui.QPainter,
              option: 'QStyleOptionGraphicsItem',
              widget: typing.Optional[QWidget] = ...) -> None:
        painter.drawRoundedRect(self.rect(), self.radius, self.radius)


class ResizableRect(QGraphicsRectItem):
    def __init__(self, x, y, width, height, fixed_points, *args, **kwargs):
        super().__init__(0, 0, width, height, *args, **kwargs)

        self.setPos(x, y)

        self.left_separator = CustomSeparator(0, 0, height, None, parent=self)
        self.right_separator = CustomSeparator(0, 0, height, None, parent=self)
        self.left_separator.setPos(0, 0)
        self.right_separator.setPos(width, 0)

        self.fixed_points = None
        self.set_fixed_points(fixed_points)

    def set_fixed_points(self, fixed_points):
        if not isinstance(fixed_points, (np.ndarray, np.generic, list)):
            raise TypeError('set_points must be a list')
        elif not all(isinstance(x, QPointF) for x in fixed_points):
            raise TypeError('All the elements of set_points must be of type QPointF')

        for i in range(len(fixed_points)):
            fixed_points[i].setX(fixed_points[i].x() - self.pos().x())
            fixed_points[i].setY(fixed_points[i].y() - self.pos().y())

        self.fixed_points = fixed_points
        self.left_separator.fixed_points = self.fixed_points
        self.right_separator.fixed_points = self.fixed_points

    def init_separators(self, pen):
        self.left_separator.installSceneEventFilter(self)
        self.right_separator.installSceneEventFilter(self)
        self.left_separator.setPen(pen)
        self.right_separator.setPen(pen)

    def sceneEventFilter(self, watched, event):
        if isinstance(event, QGraphicsSceneMouseEvent):
            if self.right_separator is watched:
                self.setRect(self.left_separator.pos().x(),
                             self.left_separator.pos().y(),
                             watched.pos().x() - self.left_separator.pos().x(),
                             self.rect().height())
            elif self.left_separator is watched:
                self.setRect(watched.pos().x(),
                             watched.pos().y(),
                             self.right_separator.pos().x() - watched.pos().x(),
                             self.rect().height())

        elif isinstance(event, QEvent) and event.type() == QEvent.UngrabMouse:
            if self.right_separator is watched:
                self.setRect(self.left_separator.pos().x(),
                             self.left_separator.pos().y(),
                             find_nearest_point(
                                 self.fixed_points,
                                 self.right_separator.pos()
                             ).x() - self.left_separator.pos().x(),
                             self.rect().height())
            elif self.left_separator is watched:
                self.setRect(watched.pos().x(),
                             watched.pos().y(),
                             self.right_separator.pos().x() -
                             find_nearest_point(
                                 self.fixed_points,
                                 self.left_separator.pos()
                             ).x(),
                             self.rect().height())
        return False


"""
class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Defining a scene rect of 400x200, with it's origin at 0,0.
        # If we don't set this on creation, we can set it later with .setSceneRect
        self.scene = QGraphicsScene(0, 0, 400, 400)
        self.rect = ResizableRect(100, 100, 20, 20,
                                  np.array(
                                      [QPointF(0, 0),
                                       QPointF(100, 0),
                                       QPointF(200, 0),
                                       QPointF(300, 0),
                                       QPointF(400, 0),
                                       QPointF(500, 0)
                                       ], dtype=object))

        self.scene.addItem(self.rect)

        custom_pen = QPen(Qt.black)
        custom_pen.setWidth(10)

        self.rect.init_separators(custom_pen)
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)

        view = QGraphicsView(self.scene)
        view.setRenderHint(QPainter.Antialiasing)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.button)
        hbox.addWidget(view)

        self.setLayout(hbox)
        self.setMinimumSize(QSize(800, 500))

    def show_new_window(self):
        self.rect.setPos(200, 200)


app = QApplication(sys.argv)

w = Window()
w.show()

app.exec()
"""
