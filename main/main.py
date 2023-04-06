import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow, QInputDialog

)
from mainWindow import Ui_MainWindow

COLORS = [
    "lavender",
    "gold",
    "goldenrod",
    "yellow",
    "orange",
    "red",
    "sienna",
    "firebrick",
    "deeppink",
    "magenta",
    "orangered",
    "brown",
    "yellowgreen",
    "chocolate",
    "coral",
    "papayawhip",
    "bisque",
]


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.textHandler.setup(10, 10, 500, 500, open("text.txt", "r").read(), 13, COLORS)

        self.actionText_size.triggered.connect(self.text_size_dialog)

    def text_size_dialog(self, s: bool) -> None:
        value, ok = QInputDialog().getInt(
            self, "Change text size", "Text size:",
            self.textHandler.get_text_size(),
            4,  # Min value
            30,  # Max value
            1  # Step
        )

        if ok:
            self.textHandler.set_text_size(value)


app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec()
