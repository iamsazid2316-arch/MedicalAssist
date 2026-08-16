from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class CadetDashboard(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Cadet Dashboard")
        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)

        self.setLayout(layout)