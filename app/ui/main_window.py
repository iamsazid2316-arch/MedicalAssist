from PySide6.QtWidgets import QMainWindow, QLabel
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Medical Assistance System")

        label = QLabel("Medical Assistance System")
        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)