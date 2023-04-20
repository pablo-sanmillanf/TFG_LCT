import typing

from PyQt5 import QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QGraphicsItem, QGraphicsRectItem, QStyleOptionGraphicsItem


class RoundedRect(QGraphicsRectItem):
    """
    This class represents a multiple QGraphicsRectItem with rounded corners. It adjusts his text_size and
    the number of QGraphicsRectItem to fill the gap between the associated Separators.
    Assuming the "|" are the separators and the "=" are the rectangles, this is more or less what it will look like:
    |=====================================================================
    ======================================================================
    ====================================|
    """

    def __init__(self, x: float | int, y: float | int, width: float | int, height: float | int, radius: float | int,
                 parent: QGraphicsItem) -> None:
        """
        Create RoundedRect object.
        :param x: The x-position of the rectangle
        :param y: The y-position of the rectangle
        :param width: The width of this element. Is determined by the max text width.
        :param height: The height of the rectangles.
        :param radius: The radius of the rounded corners.
        :param parent: The QGraphicsItem parent of this Separator. Can't be None
        """
        super().__init__(0, 0, width, height, parent)
        self.setPos(x, y)
        self.radius = radius
        self.setFlag(QGraphicsItem.ItemIgnoresParentOpacity)

    def set_background_color(self, color: str) -> None:
        """
        Set the rectangle background color
        :param color: The color as string. Should be a valid HTML color.
        """
        self.setBrush(QColor(color))
        self.update()

    def set_radius(self, radius: float) -> None:
        """
        Set the radius of the rounded rect.
        :param radius: The radius in pixels
        """
        self.radius = radius

    def set_pos_and_size(self, x: float | int, y: float | int, width: float | int, height: float | int):
        """
        Set the position and the size of the rounded_rect.
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
        :param painter: The object to paint the rectangles in the canvas
        :param option: This parameter will be ignored
        :param widget: This parameter will be ignored
        """
        if self.rect().width() != 0:
            painter.setBrush(self.brush())
            painter.drawRoundedRect(self.boundingRect(), self.radius, self.radius)
