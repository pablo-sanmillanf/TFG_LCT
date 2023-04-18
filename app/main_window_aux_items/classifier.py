from .rects_handler import RectsHandler
from PyQt5.QtCore import QEvent, Qt, QPointF
from PyQt5.QtGui import QPen, QFont
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsItem

from .descriptor_handler import DescriptorHandler, ALLOWED_STRINGS, TEXT_SEPARATOR
from .separator_handler import SeparatorHandler


def obtain_limit_points(points):
    return [(line[0], (line[1][0], line[1][-1])) for line in points]


class TextClassifier(QGraphicsLineItem):
    """
    This class controls all the behaviour of the QGraphicsItems associated with the graphical text
    classification. That is, the rectangles and its descriptors_handler and the separators between them.
    """

    def __init__(self, max_width: float, line_height: float, fixed_points: list[tuple[float, list[float]]],
                 parent: QGraphicsItem) -> None:
        """
        Create TextClassifier object. Only one object form this class should be created
        :param max_width: The maximum width of this element. Is determined by the max text width.
        :param line_height: The height that the rectangles and the separators will have. Should be
                            greater than text height.
        :param fixed_points: Available points for the separators. The structure must
                             be [(y_0, [x_0, x_1, ...]), (y_1, [x_0, x_1, ...]), ...]
        :param parent: The QGraphicsItem parent of this element. Can't be None
        """
        super().__init__(parent)
        self.setOpacity(0)
        self.max_width = max_width
        self.height = line_height
        self.fixed_points = fixed_points
        self.radius = line_height / 4
        self.offset = 0
        self.pen = None

        # Set separators
        self.sep_handler = SeparatorHandler(line_height, fixed_points, parent)
        self.sep_handler.add_separator(fixed_points[0][1][0], fixed_points[0][0], True)
        self.sep_handler.add_separator(fixed_points[-1][1][-1], fixed_points[-1][0], True)

        self.rects_handler = RectsHandler(self.height, self.radius, obtain_limit_points(fixed_points), parent)
        self.rects_handler.add_separator_listeners(
            self.sep_handler.emitter.pos_changed,
            self.sep_handler.emitter.clicked_on_the_border
        )

        self.descriptors_handler = DescriptorHandler(0, "SG~;SD~", 10, obtain_limit_points(fixed_points), parent)
        self.descriptors_handler.add_separator_listeners(
            self.sep_handler.emitter.pos_changed,
            self.sep_handler.emitter.clicked_on_the_border
        )

    def set_separator_pen(self, pen: QPen) -> None:
        """
        Apply the given pen to all the separators
        :param pen: the pen to be applied
        """
        self.pen = pen
        self.sep_handler.set_separator_pen(pen)

    def split(self, x: float, y: float) -> bool:
        """
        Splits the nearest rectangle to the given coordinates in two, placing a separator where
        the split has been made.
        :param x: The x coordinate
        :param y: The y coordinate
        :return: True if success, False if error. There can be a mistake if the coordinates
                 are out of bounds or if there is no more space to place a separator
        """
        new_separator = self.sep_handler.add_separator(x, y, False)

        if new_separator is None:
            return False

        return True

