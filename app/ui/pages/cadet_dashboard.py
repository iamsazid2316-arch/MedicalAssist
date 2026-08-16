from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)

from ..components.buttons import PrimaryButton


class CadetDashboard(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        main_layout.setContentsMargins(
            40, 30, 40, 30
        )

        main_layout.setSpacing(12)

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        title = QLabel(
            "Cadet Dashboard"
        )
        title.setAlignment(
            Qt.AlignCenter
        )

        # -------------------------------------------------
        # Welcome Message
        # -------------------------------------------------

        welcome = QLabel(
            "Welcome to MedicalAssist"
        )
        welcome.setAlignment(
            Qt.AlignCenter
        )

        # -------------------------------------------------
        # Consultation Button
        # -------------------------------------------------

        self.consultation_button = PrimaryButton(
            "➜ Start Medical Consultation"
        )

        # -------------------------------------------------
        # Previous Cases
        # -------------------------------------------------

        previous_cases_title = QLabel(
            "Previous Cases"
        )
        previous_cases_title.setAlignment(
            Qt.AlignCenter
        )

        previous_cases = QLabel(
            "No previous cases available yet."
        )
        previous_cases.setAlignment(
            Qt.AlignCenter
        )
        previous_cases.setWordWrap(
            True
        )

        # -------------------------------------------------
        # Current Case Status
        # -------------------------------------------------

        case_status_title = QLabel(
            "Current Case Status"
        )
        case_status_title.setAlignment(
            Qt.AlignCenter
        )

        case_status = QLabel(
            "No active medical case at the moment."
        )
        case_status.setAlignment(
            Qt.AlignCenter
        )
        case_status.setWordWrap(
            True
        )

        # -------------------------------------------------
        # Logout Button
        # -------------------------------------------------

        self.logout_button = PrimaryButton(
            "↩ Logout"
        )

        # -------------------------------------------------
        # Add Widgets
        # -------------------------------------------------

        main_layout.addWidget(
            title
        )

        main_layout.addWidget(
            welcome
        )

        main_layout.addSpacing(
            10
        )

        main_layout.addWidget(
            self.consultation_button
        )

        main_layout.addSpacing(
            20
        )

        main_layout.addWidget(
            previous_cases_title
        )

        main_layout.addWidget(
            previous_cases
        )

        main_layout.addSpacing(
            10
        )

        main_layout.addWidget(
            case_status_title
        )

        main_layout.addWidget(
            case_status
        )

        main_layout.addSpacing(
            20
        )

        main_layout.addWidget(
            self.logout_button
        )

        # -------------------------------------------------
        # Set Layout
        # -------------------------------------------------

        self.setLayout(
            main_layout
        )