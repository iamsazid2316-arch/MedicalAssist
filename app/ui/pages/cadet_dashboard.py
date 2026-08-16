from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class CadetDashboard(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Cadet Dashboard")
        title.setAlignment(Qt.AlignCenter)

        welcome = QLabel("Welcome to MedicalAssist")
        welcome.setAlignment(Qt.AlignCenter)

        consultation_button = QPushButton(
            "Start Medical Consultation"
        )

        previous_cases_title = QLabel("Previous Cases")
        previous_cases_title.setAlignment(Qt.AlignCenter)

        previous_cases = QLabel(
            "No previous cases available."
        )
        previous_cases.setAlignment(Qt.AlignCenter)

        case_status_title = QLabel("Current Case Status")
        case_status_title.setAlignment(Qt.AlignCenter)

        case_status = QLabel("No active medical case.")
        case_status.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(title)
        main_layout.addWidget(welcome)
        main_layout.addSpacing(20)

        main_layout.addWidget(consultation_button)

        main_layout.addSpacing(30)

        main_layout.addWidget(previous_cases_title)
        main_layout.addWidget(previous_cases)

        main_layout.addSpacing(20)

        main_layout.addWidget(case_status_title)
        main_layout.addWidget(case_status)

        self.setLayout(main_layout)