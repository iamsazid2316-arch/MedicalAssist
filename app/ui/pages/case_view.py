from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class CaseView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Case View")
        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)

        self.setLayout(layout)