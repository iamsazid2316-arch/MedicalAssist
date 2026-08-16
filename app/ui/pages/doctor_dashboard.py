from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class DoctorDashboard(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Doctor Dashboard")
        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)

        self.setLayout(layout)