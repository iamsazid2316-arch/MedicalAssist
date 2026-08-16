from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class DoctorDashboard(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Doctor Dashboard")
        title.setAlignment(Qt.AlignCenter)

        welcome = QLabel("Welcome to MedicalAssist")
        welcome.setAlignment(Qt.AlignCenter)

        pending_cases_title = QLabel("Pending Cases")
        pending_cases_title.setAlignment(Qt.AlignCenter)

        self.case_selector = QComboBox()
        self.case_selector.addItems([
            "No pending cases available."
        ])

        case_summary_title = QLabel("Selected Case Summary")
        case_summary_title.setAlignment(Qt.AlignCenter)

        self.case_summary = QLabel("No case selected.")
        self.case_summary.setAlignment(Qt.AlignCenter)
        self.case_summary.setWordWrap(True)

        case_details_title = QLabel("Case Details")
        case_details_title.setAlignment(Qt.AlignCenter)

        self.case_details = QLabel(
            "Select a case to view its details."
        )
        self.case_details.setAlignment(Qt.AlignCenter)
        self.case_details.setWordWrap(True)

        medical_history_title = QLabel("Medical History")
        medical_history_title.setAlignment(Qt.AlignCenter)

        self.medical_history = QLabel(
            "No medical history available."
        )
        self.medical_history.setAlignment(Qt.AlignCenter)
        self.medical_history.setWordWrap(True)

        consultation_history_title = QLabel(
            "Consultation History"
        )
        consultation_history_title.setAlignment(Qt.AlignCenter)

        self.consultation_history = QLabel(
            "No consultation history available."
        )
        self.consultation_history.setAlignment(Qt.AlignCenter)
        self.consultation_history.setWordWrap(True)

        actions_title = QLabel("Doctor Actions")
        actions_title.setAlignment(Qt.AlignCenter)

        self.review_button = QPushButton("Review Case")
        self.approve_button = QPushButton("Approve Case")
        self.reject_button = QPushButton("Reject Case")

        status_title = QLabel("Case Status")
        status_title.setAlignment(Qt.AlignCenter)

        self.status_selector = QComboBox()
        self.status_selector.addItems([
            "Pending",
            "Under Review",
            "Approved",
            "Rejected",
        ])

        self.update_status_button = QPushButton(
            "Update Case Status"
        )

        main_layout.addWidget(title)
        main_layout.addWidget(welcome)
        main_layout.addSpacing(25)

        main_layout.addWidget(pending_cases_title)
        main_layout.addWidget(self.case_selector)

        main_layout.addSpacing(20)

        main_layout.addWidget(case_summary_title)
        main_layout.addWidget(self.case_summary)

        main_layout.addSpacing(20)

        main_layout.addWidget(case_details_title)
        main_layout.addWidget(self.case_details)

        main_layout.addSpacing(20)

        main_layout.addWidget(medical_history_title)
        main_layout.addWidget(self.medical_history)

        main_layout.addSpacing(20)

        main_layout.addWidget(consultation_history_title)
        main_layout.addWidget(self.consultation_history)

        main_layout.addSpacing(20)

        main_layout.addWidget(actions_title)
        main_layout.addWidget(self.review_button)
        main_layout.addWidget(self.approve_button)
        main_layout.addWidget(self.reject_button)

        main_layout.addSpacing(20)

        main_layout.addWidget(status_title)
        main_layout.addWidget(self.status_selector)
        main_layout.addWidget(self.update_status_button)

        self.setLayout(main_layout)