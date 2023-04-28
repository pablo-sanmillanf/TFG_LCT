from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel


HIGHLIGHT_STYLE = "color:white;background-color:red;"


class TextLabel(QLabel):

    scroll_updated = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.clause_texts = None
        self.super_clause_texts = None

    def set_texts(self, super_clause_texts: list[str], clause_texts: list[str]):
        self.clause_texts = clause_texts
        self.super_clause_texts = super_clause_texts
        self.setText("<p style=\"line-height:200%\">" + " ".join(clause_texts).replace("\n", "<br>") + "<p>")

    def text_selected(self, text_index):
        text = "<p style=\"line-height:200%\"> "

        for i in range(len(self.clause_texts)):
            if i == text_index:
                if i == 0:
                    self.scroll_updated.emit(0)
                else:
                    aux_label = QLabel()
                    aux_label.setFont(self.font())
                    aux_label.setText(text + "</p>")
                    self.scroll_updated.emit(aux_label.height())

                text += ("<span style = \"" + HIGHLIGHT_STYLE + "\">" + self.clause_texts[i].replace("\n", "<br>")
                         + "</span> ")
            else:
                text += (self.clause_texts[i].replace("\n", "<br>") + " ")
        text += "</p>"
        self.setText(text)
