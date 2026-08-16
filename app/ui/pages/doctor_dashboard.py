from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
    QComboBox,
    QPushButton,
)


class DoctorDashboard(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        main_layout.setAlignment(
            Qt.AlignCenter
        )

        main_layout.setContentsMargins(
            40, 30, 40, 30
        )

        main_layout.setSpacing(12)

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        title = QLabel(
            "Doctor Dashboard"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        main_layout.addWidget(
            title
        )

        main_layout.addSpacing(
            10
        )

        # -------------------------------------------------
        # Pending Cases
        # -------------------------------------------------

        pending_title = QLabel(
            "Pending Cases"
        )

        pending_title.setAlignment(
            Qt.AlignCenter
        )

        self.pending_cases = QComboBox()

        self.pending_cases.addItems(
            [
                "Case #1001",
                "Case #1002",
                "Case #1003",
            ]
        )

        main_layout.addWidget(
            pending_title
        )

        main_layout.addWidget(
            self.pending_cases
        )

        main_layout.addSpacing(
            15
        )

        # -------------------------------------------------
        # Selected Case Summary
        # -------------------------------------------------

        summary_title = QLabel(
            "Selected Case Summary"
        )

        summary_title.setAlignment(
            Qt.AlignCenter
        )

        self.case_summary = QLabel(
            "No case selected."
        )

        self.case_summary.setAlignment(
            Qt.AlignCenter
        )

        self.case_summary.setWordWrap(
            True
        )

        main_layout.addWidget(
            summary_title
        )

        main_layout.addWidget(
            self.case_summary
        )

        main_layout.addSpacing(
            15
        )

        # -------------------------------------------------
        # Case Details
        # -------------------------------------------------

        details_title = QLabel(
            "Case Details"
        )

        details_title.setAlignment(
            Qt.AlignCenter
        )

        self.case_details = QLabel(
            "Select a case to view its details."
        )

        self.case_details.setAlignment(
            Qt.AlignCenter
        )

        self.case_details.setWordWrap(
            True
        )

        main_layout.addWidget(
            details_title
        )

        main_layout.addWidget(
            self.case_details
        )

        main_layout.addSpacing(
            15
        )

        # -------------------------------------------------
        # Medical History
        # -------------------------------------------------

        medical_history_title = QLabel(
            "Medical History"
        )

        medical_history_title.setAlignment(
            Qt.AlignCenter
        )

        self.medical_history = QLabel(
            "No medical history available."
        )

        self.medical_history.setAlignment(
            Qt.AlignCenter
        )

        self.medical_history.setWordWrap(
            True
        )

        main_layout.addWidget(
            medical_history_title
        )

        main_layout.addWidget(
            self.medical_history
        )

        main_layout.addSpacing(
            15
        )

        # -------------------------------------------------
        # Consultation History
        # -------------------------------------------------

        consultation_history_title = QLabel(
            "Consultation History"
        )

        consultation_history_title.setAlignment(
            Qt.AlignCenter
        )

        self.consultation_history = QLabel(
            "No consultation history available."
        )

        self.consultation_history.setAlignment(
            Qt.AlignCenter
        )

        self.consultation_history.setWordWrap(
            True
        )

        main_layout.addWidget(
            consultation_history_title
        )

        main_layout.addWidget(
            self.consultation_history
        )

        main_layout.addSpacing(
            15
        )

        # -------------------------------------------------
        # Doctor Actions
        # -------------------------------------------------

        actions_title = QLabel(
            "Doctor Actions"
        )

        actions_title.setAlignment(
            Qt.AlignCenter
        )

        self.review_button = QPushButton(
            "Review Case"
        )

        self.approve_button = QPushButton(
            "Approve Case"
        )

        self.reject_button = QPushButton(
            "Reject Case"
        )

        main_layout.addWidget(
            actions_title
        )

        main_layout.addWidget(
            self.review_button
        )

        main_layout.addWidget(
            self.approve_button
        )

        main_layout.addWidget(
            self.reject_button
        )

        main_layout.addSpacing(
            15
        )

        # -------------------------------------------------
        # Case Status
        # -------------------------------------------------

        status_title = QLabel(
            "Case Status"
        )

        status_title.setAlignment(
            Qt.AlignCenter
        )

        self.status_selector = QComboBox()

        self.status_selector.addItems(
            [
                "Pending",
                "Under Review",
                "Approved",
                "Rejected",
            ]
        )

        self.update_status_button = QPushButton(
            "Update Case Status"
        )

        main_layout.addWidget(
            status_title
        )

        main_layout.addWidget(
            self.status_selector
        )

        main_layout.addWidget(
            self.update_status_button
        )

        main_layout.addSpacing(
            15
        )

        # -------------------------------------------------
        # Logout
        # -------------------------------------------------

        self.logout_button = QPushButton(
            "↩ Logout"
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

        # -------------------------------------------------
        # Temporary Case Data
        # -------------------------------------------------

        self.case_data = {
            "Case #1001": {
                "summary": (
                    "Patient reports fever, headache, "
                    "and general weakness."
                ),
                "details": (
                    "Patient: Ahmed Rahman\n"
                    "Age: 24\n"
                    "Gender: Male\n"
                    "Priority: Medium"
                ),
                "medical_history": (
                    "No significant medical history available."
                ),
                "consultation_history": (
                    "No previous consultation recorded."
                ),
            },

            "Case #1002": {
                "summary": (
                    "Patient reports chest discomfort "
                    "and shortness of breath."
                ),
                "details": (
                    "Patient: Fatima Akter\n"
                    "Age: 31\n"
                    "Gender: Female\n"
                    "Priority: High"
                ),
                "medical_history": (
                    "Previous respiratory issues reported."
                ),
                "consultation_history": (
                    "Previous consultation recorded."
                ),
            },

            "Case #1003": {
                "summary": (
                    "Patient reports abdominal pain "
                    "and nausea."
                ),
                "details": (
                    "Patient: Karim Hasan\n"
                    "Age: 42\n"
                    "Gender: Male\n"
                    "Priority: Medium"
                ),
                "medical_history": (
                    "No significant medical history available."
                ),
                "consultation_history": (
                    "No previous consultation recorded."
                ),
            },
        }

        # -------------------------------------------------
        # Signals
        # -------------------------------------------------

        self.pending_cases.currentTextChanged.connect(
            self.load_selected_case
        )

        self.approve_button.clicked.connect(
            self.approve_selected_case
        )

        self.reject_button.clicked.connect(
            self.reject_selected_case
        )

        self.update_status_button.clicked.connect(
            self.update_case_status
        )

        # -------------------------------------------------
        # Load First Case
        # -------------------------------------------------

        self.load_selected_case(
            self.pending_cases.currentText()
        )

    # -----------------------------------------------------
    # Load Selected Case
    # -----------------------------------------------------

    def load_selected_case(
        self,
        case_id
    ):
        if not case_id:
            return

        case = self.case_data.get(
            case_id
        )

        if case is None:
            return

        self.case_summary.setText(
            case["summary"]
        )

        self.case_details.setText(
            case["details"]
        )

        self.medical_history.setText(
            case["medical_history"]
        )

        self.consultation_history.setText(
            case["consultation_history"]
        )

        self.status_selector.setCurrentText(
            "Pending"
        )

    # -----------------------------------------------------
    # Get Current Case
    # -----------------------------------------------------

    def get_current_case(self):

        case_id = (
            self.pending_cases.currentText()
        )

        case = self.case_data.get(
            case_id
        )

        return case_id, case

    # -----------------------------------------------------
    # Approve Case
    # -----------------------------------------------------

    def approve_selected_case(self):

        self.status_selector.setCurrentText(
            "Approved"
        )

    # -----------------------------------------------------
    # Reject Case
    # -----------------------------------------------------

    def reject_selected_case(self):

        self.status_selector.setCurrentText(
            "Rejected"
        )

    # -----------------------------------------------------
    # Update Status
    # -----------------------------------------------------

    def update_case_status(self):

        current_status = (
            self.status_selector.currentText()
        )

        self.case_summary.setText(
            self.case_summary.text()
            + f"\n\nCurrent Status: {current_status}"
        )