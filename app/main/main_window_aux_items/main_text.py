from PyQt5 import QtGui
from PyQt5.QtCore import QTextBoundaryFinder

from PyQt5.QtWidgets import QGraphicsTextItem, QGraphicsItem


def _apply_text_format(text: str) -> str:
    """
    This function format the text to adapt it to the required format by class MainText.
    More specifically, replace the "\n" with "<br>", remove duplicate spaces and change special HTML characters with
    valid HTML ones.
    :param text: The text to be formatted.
    :return: The formatted text.
    """
    text = text.replace("&", "&amp;")
    text = text.replace("\"", "&quot;")
    text = text.replace(">", "&gt;")
    text = text.replace("<", "&lt;")
    return " ".join(text.replace("\n", " <br> ").split())


def _remove_text_format(text: str) -> str:
    """
    This function remove the HTML format from the text to obtain plain text.
    :param text: The text to be formatted.
    :return: The formatted text.
    """
    text = text.replace("&amp;", "&")
    text = text.replace("&quot;", "\"")
    text = text.replace("&gt;", ">")
    text = text.replace("&lt;", "<")
    return text


def _find_boundaries_word(word: str):
    finder = QTextBoundaryFinder(QTextBoundaryFinder.Line, word)
    result = []
    index = finder.toNextBoundary()
    while index != -1:
        result.append(index)
        index = finder.toNextBoundary()
    result.pop()
    return result


class MainText(QGraphicsTextItem):
    """
    This class represents a multiline text with an interline spacing introduced in the constructor. Can also calculate
    the points that represents the spaces in the text.
    """

    def __init__(self, text: str, size: float | int, width: float | int, line_height: float | int,
                 parent: QGraphicsItem) -> None:
        """
        Create MainText object.
        :param text: The text to represent by the element.
        :param size: The point size of the text.
        :param width: The maximum width for a line.
        :param line_height: Represents the space between strips in the text. Is a number as a percentage so should be
                            greater than 100
        :param parent: The QGraphicsItem parent.
        """
        super().__init__(parent)
        self._words_width = None
        self.setTextWidth(width - 10)
        self.setFlag(QGraphicsItem.ItemIgnoresParentOpacity)
        self.setPos(5, 5)
        self.setZValue(1)
        self._line_height = line_height
        self._text = text

        # Add specific format
        font = self.font()
        font.setFamily('Times')
        font.setBold(True)
        self.setFont(font)

        self.set_text_size(size)
        self.set_text(text)

    def get_text(self) -> str:
        """
        Return the plain text of the element.
        :return: The plain text.
        """
        text = _remove_text_format(self._text).replace(" <br> ", " \n ").replace(" <br> ", " \n ")
        if text[-4:] == "<br>":
            return text[:-4] + "\n"
        return text

    def set_text(self, text: str) -> None:
        """
        Set the text of the element justified and with the element's line height. Also apply the format accepted by the
        HTML engine.
        :param text: The text
        """
        self._text = _apply_text_format(text)
        self._set_text(self._text)

    def _set_text(self, text: str) -> None:
        """
        Set the text of the element justified and with the element's line height.
        :param text: The text
        """
        self.setHtml('<p align="justify" style="line-height: ' + str(self._line_height) + '%">' + text + '</p>')

        self._words_width = self._get_words_width(self._text.split(" "))

    def set_width(self, width: float | int) -> None:
        """
        Set the text width for the item and recalculates the separator points
        :param width: Maximum width in pixels
        """
        self.setTextWidth(width - 10)

    def set_text_size(self, size: float | int) -> None:
        """
        Set the point size of the text. Call this function won't update automatically the positions of the points
        between the words.
        :param size: The point size as a number
        """
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)

    def _get_words_width(self, text_list: list[str]) -> list[tuple[int | float, str, bool]]:
        """
        This function calculates the width of all the words passed as parameter.
        :param text_list: A list of words.
        :return: A list. For each element, the first sub-element is the word width, the second, the word and the last, a
                 boolean that indicates if the word is part of a word with one or more BREAK_LINE_CHARACTERS.
        """
        # Obtain the offsets to correctly place the separators
        half_space, padding = self._get_separator_offsets_width()

        # Create an auxiliary QGraphicsTextItem to calculate the points
        aux_text = QGraphicsTextItem()
        aux_text.setFont(self.font())

        result = []
        for word in text_list:
            if word == "<br>":
                result.append((-1, "\n", False))  # Break line
            else:
                aux_text.setHtml(word)
                positions = _find_boundaries_word(word)
                if len(positions) == 0:
                    result.append((aux_text.boundingRect().width() - 2 * padding, word, False))
                else:
                    start_pos = 0

                    for i in range(len(positions)):
                        sub_word = word[start_pos:positions[i]]
                        start_pos = positions[i]

                        aux_text.setHtml(sub_word)
                        result.append((aux_text.boundingRect().width() - 2 * padding, sub_word, True))

                    sub_word = word[start_pos:]
                    aux_text.setHtml(sub_word)
                    result.append((aux_text.boundingRect().width() - 2 * padding, sub_word, False))

        return result

    def get_complete_points(self) -> list[tuple[float, list[list[float | str | bool]]]]:
        """
        Calculates the points of separation between the different words of the text. It returns a complex structure that
        is composed by a list of tuples. The first element of the tuple is the y-value for a specific line and the
        second element is a three-element list. Each of these three-element lists represents an x-value in the specific
        line, the word that is immediately after the x-point and a boolean that indicates if this word is part of a word
        with one or more BREAK_LINE_CHARACTERS. In the case of an end of line, and empty string will be stored.
        :return: The complex structure described above.
        """

        half_space, horizontal_padding = self._get_separator_offsets_width()
        vertical_padding, line_vertical_offset = self._get_separator_offsets_height()

        space = 2 * half_space
        points = []
        line_index = 0
        words_start_index = 0
        words_width = 2 * horizontal_padding
        skip = False
        i = 0

        for i in range(len(self._words_width) - 1):
            if skip:
                if self._words_width[i][0] == -1:  # Another break line
                    line_index += 1
                    points[-1][1][-1][1] += "\n "
                else:
                    skip = False
                    words_width += self._words_width[i][0] + space
                    words_start_index = i
                    points[-1][1][-1][1] += "\n"

                continue
            elif self._words_width[i][0] == -1:  # Break line

                # Add line
                points.append((
                    vertical_padding + line_vertical_offset * line_index + self.pos().y(),
                    self._get_x_values(
                        words_start_index,
                        i - 1,
                        True, horizontal_padding,
                        half_space
                    )
                ))
                line_index += 1
                words_width = 2 * horizontal_padding
                skip = True
            else:
                if self._words_width[i - 1][2]:  # If current string is part of a string with BREAK_LINE_CHARACTERS
                    words_width += self._words_width[i][0]
                else:
                    words_width += (self._words_width[i][0] + space)

                if words_width - space > self.textWidth():  # This line is full

                    # Add line
                    points.append((
                        vertical_padding + line_vertical_offset * line_index + self.pos().y(),
                        self._get_x_values(
                            words_start_index,
                            i - 1,
                            False,
                            horizontal_padding,
                            half_space
                        )
                    ))
                    line_index += 1
                    words_width = 2 * horizontal_padding + self._words_width[i][0] + space
                    words_start_index = i
        if skip:
            words_start_index = i + 1
            points[-1][1][-1][1] += "\n"

        if self._words_width[len(self._words_width) - 2][2]:
            words_width += self._words_width[len(self._words_width) - 1][0]
        else:
            words_width += (self._words_width[len(self._words_width) - 1][0] + 2 * half_space)

        if words_width - space > self.textWidth():  # This line is full
            # Add line
            points.append((
                vertical_padding + line_vertical_offset * line_index + self.pos().y(),
                self._get_x_values(
                    words_start_index,
                    len(self._words_width) - 2,
                    False,
                    horizontal_padding,
                    half_space
                )
            ))
            line_index += 1
            words_start_index = len(self._words_width) - 1

        points.append((
            vertical_padding + line_vertical_offset * line_index + self.pos().y(),
            self._get_x_values(
                words_start_index,
                len(self._words_width) - 1,
                True,
                horizontal_padding,
                half_space
            )
        ))
        return points

    def _get_x_values(self, start_index: int, end_index: int, break_line: bool,
                      padding: int | float, half_space: int | float) -> list[list[float | str | bool]]:
        """
        Calculates the x-points of separation between the different words of a line indicated by start_index and
        end_index. It returns a complex structure. Is composed by a list of three-element lists. Each of these
        three-element lists represents an x-value in the line, the word that is immediately after the x-point and a
        boolean that indicates if this word is part of a word with one or more BREAK_LINE_CHARACTERS. In the case of the
        end of line, and empty string will be stored.
        :param start_index: Index of the first word in the line in self.words_width structure.
        :param end_index: Index of the last word in the line in self.words_width structure plus one.
        :param break_line: True if the line is not justified (because of a "\n" character or because of the end of the
                           document).
        :param padding: The padding introduced by QGraphicsTextItem.
        :param half_space: Half of what the character space occupies with the given font
        :return: The complex structure described above.
        """
        line_width = padding / 2 + self.pos().x()
        x_values_with_words = [
            [
                line_width,
                _remove_text_format(self._words_width[start_index][1]),
                (self._words_width[start_index - 1][2] if (start_index > 1) else False)
            ]
        ]
        line_width += padding / 2 - half_space

        sub_str_pos = []

        for i in range(start_index, end_index):
            # If current string is part of a string with BREAK_LINE_CHARACTERS and is not at the start of the line
            if self._words_width[i - 1][2] and start_index != i:
                line_width += self._words_width[i][0]

                x_values_with_words[-1][0] += half_space

                sub_str_pos.append(i - start_index)
            else:
                line_width += (self._words_width[i][0] + 2 * half_space)

            x_values_with_words.append(
                [line_width, _remove_text_format(self._words_width[i + 1][1]), self._words_width[i][2]]
            )

        if self._words_width[end_index - 1][2]:
            line_width += (self._words_width[end_index][0] - half_space + padding)
            sub_str_pos.append(end_index)
        else:
            line_width += (self._words_width[end_index][0] + half_space + padding)

        # Adjust offsets to the justify line
        if not break_line and end_index > start_index + len(sub_str_pos):

            # We obtain the remaining pixels that will be distributed among all the spaces to justify text, and we
            # divide it by the number of spaces to know how much is left for each one
            space_adjust = ((self.textWidth() - line_width + self.pos().x()) /
                            (end_index - start_index - len(sub_str_pos)))

            sub_str_offset = 1
            # Add space_adjust to the x-points
            for e in range(1, len(x_values_with_words)):
                if e in sub_str_pos:
                    sub_str_offset += 1
                x_values_with_words[e][0] += (space_adjust / 2 + space_adjust * (e - sub_str_offset))

            x_values_with_words.append(
                [self.textWidth() - padding / 2 + self.pos().x(), "", self._words_width[end_index][2]]
            )
        else:
            x_values_with_words.append([line_width, "", False])

        return x_values_with_words

    def _get_separator_offsets_width(self) -> tuple[float, float]:
        """
        This function gets the width in pixels of what would occupy half of what the space character occupies with the
        given font. In addition, it also gets the width in pixels of the padding introduced by the QGraphicsTextItem
        element. To do this, the following system of equations must be solved:
            - padding + space + padding = len_text1
            - padding + space + space + padding = len_text2
        Those values will be used to place the text separators

        :return: Half of what the character space occupies with the given font and the padding introduced by
                 QGraphicsTextItem.
        """
        text1 = QGraphicsTextItem(" ")
        text2 = QGraphicsTextItem("  ")
        text1.setFont(self.font())
        text2.setFont(self.font())

        # Resolve the system of equations
        space = text2.boundingRect().width() - text1.boundingRect().width()
        padding = text1.boundingRect().width() - text2.boundingRect().width() / 2

        return space / 2, padding

    def _get_separator_offsets_height(self) -> tuple[float, float]:
        """
        This function gets the height in pixels of the height of the strip used to represent the text with the given
        font plus the line spacing. In addition, it also gets the height in pixels of the padding introduced by the
        QGraphicsTextItem element. To do so, the following system of equations must be solved:
            - padding + strip + line_spacing + padding = height_1
            - padding + strip + line_spacing + strip + line_spacing + padding = height_2
        Those values will be used to place the text separators

        :return: The padding height introduced by QGraphicsTextItem and the height that occupies the text plus the
                 padding height between line texts.
        """
        aux = QGraphicsTextItem()
        aux.setFont(self.font())

        aux.setHtml('<p align="justify" style="line-height:' + str(self._line_height) + '%">Test</p>')
        height_1 = aux.boundingRect().height()

        aux.setHtml('<p align="justify" style="line-height:' + str(self._line_height) + '%">Test<br>Test</p>')
        height_2 = aux.boundingRect().height()

        # Resolve the system of equations
        strip_plus_line_spacing = height_2 - height_1
        padding = height_1 - (height_2 / 2)

        return padding, strip_plus_line_spacing

    def setFont(self, font: QtGui.QFont) -> None:
        """
        Set text with a given font.
        :param font: The font object
        """
        super().setFont(font)
        self._set_text(self._text)
