from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel


HIGHLIGHT_STYLE = "color:white;background-color:red;"


class TextLabel(QLabel):

    scroll_updated = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.clause_texts = None
        self.super_clause_texts = None
        self.clauses_type_selected = True  # True if clauses selected, False if super clauses selected

    def set_texts(self, super_clause_texts: list[str], clause_texts: list[str]):
        self.clause_texts = clause_texts
        self.super_clause_texts = super_clause_texts
        self.setText("<p style=\"line-height:200%\">" + " ".join(clause_texts).replace("\n", "<br>") + "<p>")

    def set_clauses_type(self, is_normal_clauses: bool):
        if self.clauses_type_selected != is_normal_clauses:
            self.clauses_type_selected = is_normal_clauses
            if self.clauses_type_selected:
                self.setText(
                    "<p style=\"line-height:200%\">" + " ".join(self.clause_texts).replace("\n", "<br>") + "<p>"
                )
            else:
                self.setText(
                    "<p style=\"line-height:200%\">" + " ".join(self.super_clause_texts).replace("\n", "<br>") + "<p>"
                )

    def text_selected(self, text_index):
        text = "<p style=\"line-height:200%\"> "
        if self.clauses_type_selected:
            text_list = self.clause_texts
        else:
            text_list = self.super_clause_texts

        for i in range(len(text_list)):
            if i == text_index:
                if i == 0:
                    self.scroll_updated.emit(0)
                else:
                    aux_label = QLabel()
                    aux_label.setFont(self.font())
                    aux_label.setText(text + "</p>")
                    self.scroll_updated.emit(aux_label.height())

                text += ("<span style = \"" + HIGHLIGHT_STYLE + "\">" + text_list[i].replace("\n", "<br>")
                         + "</span> ")
            else:
                text += (text_list[i].replace("\n", "<br>") + " ")
        text += "</p>"
        self.setText(text)
