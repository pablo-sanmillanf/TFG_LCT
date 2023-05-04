from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QPushButton, QWidget
from PySide2.QtGui import QIcon
import sys, os

basedir = os.path.dirname(__file__)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hello World")
        layout = QVBoxLayout()
        label = QLabel("My simple app.")
        label.setMargin(10)
        layout.addWidget(label)

        button = QPushButton("Push")
        button.setIcon(QIcon(os.path.join(basedir, "icons", "lightning.svg")))
        button.pressed.connect(self.close)
        layout.addWidget(button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(basedir, "icons", "penguin.svg")))
    w = MainWindow()
    app.exec_()