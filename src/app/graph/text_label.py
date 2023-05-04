from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QWidget

HIGHLIGHT_STYLE = "color:white;background-color:red;"


class TextLabel(QLabel):
    """
    This class manages the text associated to the points represented in the graph. This text is split in parts that
    represents the text associated to each point of the graph. The class permit to highlight one of this text parts.
    Also, this class manages two split versions of the text: clauses and super clauses, that can be swapped.
    """
    scroll_updated = pyqtSignal(int)

    def __init__(self, parent: QWidget):
        """
        TextLabel object creator.
        :param parent: The widget parent of the QLabel.
        """
        super().__init__(parent)
        self._clause_texts = None
        self._super_clause_texts = None
        self._clauses_type_selected = True  # True if clauses selected, False if super clauses selected

    def set_texts(self, super_clause_texts: list[str], clause_texts: list[str]) -> None:
        """
        Change the lists of strings of clauses and super clauses and represents in the QLabel, the text corresponding to
        the clauses.
        :param super_clause_texts: The super clauses string list.
        :param clause_texts: The clauses string list.
        """
        self._clause_texts = clause_texts
        self._super_clause_texts = super_clause_texts
        self.setText("<p style=\"line-height:200%\">" + " ".join(clause_texts).replace("\n", "<br>") + "<p>")

    def set_clauses_type(self, is_normal_clauses: bool) -> None:
        """
        Set the clauses type between clauses and super clauses depending on is_normal_clauses parameter.
        :param is_normal_clauses: True if is clauses, False if is super clauses.
        """
        if self._clauses_type_selected != is_normal_clauses:
            self._clauses_type_selected = is_normal_clauses
            if self._clauses_type_selected:
                self.setText(
                    "<p style=\"line-height:200%\">" + " ".join(self._clause_texts).replace("\n", "<br>") + "<p>"
                )
            else:
                self.setText(
                    "<p style=\"line-height:200%\">" + " ".join(self._super_clause_texts).replace("\n", "<br>") + "<p>"
                )

    def text_selected(self, text_index: int) -> None:
        """
        Change the text in the QLabel to highlight the part of the text that correspond to the index passed as
        parameter.
        :param text_index: The index of the selected string.
        """
        text = "<p style=\"line-height:200%\"> "
        if self._clauses_type_selected:
            text_list = self._clause_texts
        else:
            text_list = self._super_clause_texts

        for i in range(len(text_list)):
            if i == text_index:
                aux_label = QLabel()
                aux_label.setFont(self.font())
                aux_label.setText(text + "</p>")
                if aux_label.width() >= aux_label.fontMetrics().boundingRect(aux_label.text()).width():
                    self.scroll_updated.emit(0)
                else:
                    self.scroll_updated.emit(aux_label.height())

                text += ("<span style = \"" + HIGHLIGHT_STYLE + "\">" + text_list[i].replace("\n", "<br>")
                         + "</span> ")
            else:
                text += (text_list[i].replace("\n", "<br>") + " ")
        text += "</p>"
        self.setText(text)

    def get_data(self) -> list[str]:
        """
        Obtain the list of strings that is currently represented in the QLabel, depending on if the clause type selected
        is clauses or super clauses.
        :return: The list of strings.
        """
        if self._clauses_type_selected:
            return self._clause_texts
        else:
            return self._super_clause_texts
