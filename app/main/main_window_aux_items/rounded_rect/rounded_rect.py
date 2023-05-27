import typing

from PyQt5 import QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QGraphicsItem, QGraphicsRectItem, QStyleOptionGraphicsItem


class RoundedRect(QGraphicsRectItem):
    """
    This class represents a QGraphicsRectItem with rounded corners. This class also has methods to set and obtain the
    background color. When the width is 0, the class paints nothing.
    """

    def __init__(self, x: float | int, y: float | int, width: float | int, height: float | int, radius: float | int,
                 parent: QGraphicsItem) -> None:
        """
        Create RoundedRect object.
        :param x: The x-position of the rectangle
        :param y: The y-position of the rectangle
        :param width: The width of this element.
        :param height: The height of the rectangle.
        :param radius: The radius of the rounded corners.
        :param parent: The QGraphicsItem parent of this Separator. Can't be None
        """
        super().__init__(0, 0, width, height, parent)
        self.setPos(x, y)
        self._radius = radius
        self.setFlag(QGraphicsItem.ItemIgnoresParentOpacity)

    def set_background_color(self, color: str) -> None:
        """
        Set the rectangle background color.
        :param color: The color as string. Should be a valid HTML color.
        """
        self.setBrush(QColor(color))
        self.update()

    def get_background_color(self) -> str:
        """
        Return the rectangle background color.
        :return: The color as string. Is a valid HTML color.
        """
        return self.brush().color()

    def set_radius(self, radius: float) -> None:
        """
        Set the radius of the rounded rect.
        :param radius: The radius in pixels
        """
        self._radius = radius

    def set_pos_and_size(self, x: float | int, y: float | int, width: float | int, height: float | int):
        """
        Set the position and the size of the rounded rect.
        :param x: The x-position of the rectangle.
        :param y: The y-position of the rectangle.
        :param width: The width of this element.
        :param height: The height of the rectangle.
        """
        self.setRect(0, 0, width, height)
        self.setPos(x, y)

    def paint(self,
              painter: QtGui.QPainter,
              option: QStyleOptionGraphicsItem,
              widget: typing.Optional[QWidget] = ...) -> None:
        """
        Paints the rectangle with a given radius.
        :param painter: The object to paint the rectangles in the _canvas
        :param option: This parameter will be ignored
        :param widget: This parameter will be ignored
        """
        if self.rect().width() != 0:
            painter.setBrush(self.brush())
            painter.drawRoundedRect(self.boundingRect(), self._radius, self._radius)
