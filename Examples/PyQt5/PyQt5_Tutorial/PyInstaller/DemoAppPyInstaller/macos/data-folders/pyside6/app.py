from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QPushButton, QWidget
from PySide6.QtGui import QIcon

import sys
import os

basedir = os.path.dirname(__file__)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hello World")
        layout = QVBoxLayout()
        label = QLabel("Hello World")
        label.setMargin(10)
        layout.addWidget(label)

        button1 = QPushButton("Hide")
        button1.setIcon(QIcon(os.path.join(basedir, "icons", "hand.png")))
        button1.pressed.connect(self.lower)
        layout.addWidget(button1)

        button2 = QPushButton("Close")
        button2.setIcon(QIcon(os.path.join(basedir, "icons", "lightning.png")))
        button2.pressed.connect(self.close)
        layout.addWidget(button2)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
