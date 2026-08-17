from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class CadetDashboard(QWidget):
    consultation_requested = Signal()
    refresh_requested = Signal()
    response_requested = Signal(int)
    logout_requested = Signal()

    def __init__(self):
        super().__init__()
        self.cases: list[dict] = []
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(12)

        header = QHBoxLayout()
        self.welcome_label = QLabel("Cadet Dashboard")
        self.welcome_label.setObjectName("pageTitle")
        self.connection_label = QLabel("Connected")
        self.connection_label.setObjectName("statusBadge")
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout_requested.emit)
        header.addWidget(self.welcome_label)
        header.addStretch()
        header.addWidget(self.connection_label)
        header.addWidget(self.logout_button)

        self.notification_label = QLabel("No new notifications")
        self.notification_label.setWordWrap(True)
        self.notification_label.setObjectName("infoBanner")

        self.consultation_button = QPushButton("Start Medical Consultation")
        self.consultation_button.clicked.connect(self.consultation_requested.emit)

        row = QHBoxLayout()
        title = QLabel("Previous cases")
        title.setObjectName("sectionTitle")
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_requested.emit)
        row.addWidget(title)
        row.addStretch()
        row.addWidget(self.refresh_button)

        self.case_list = QListWidget()
        self.case_list.itemDoubleClicked.connect(self._request_response)
        self.empty_label = QLabel("No cases yet. Start a consultation when you need help.")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setObjectName("mutedText")
        self.response_button = QPushButton("View approved doctor response")
        self.response_button.clicked.connect(self._request_response)

        layout.addLayout(header)
        layout.addWidget(self.notification_label)
        layout.addWidget(self.consultation_button)
        layout.addLayout(row)
        layout.addWidget(self.case_list, 1)
        layout.addWidget(self.empty_label)
        layout.addWidget(self.response_button)

    def set_user(self, name: str):
        self.welcome_label.setText(f"Welcome, {name}")

    def set_loading(self, loading: bool):
        self.refresh_button.setDisabled(loading)
        self.response_button.setDisabled(loading)
        self.refresh_button.setText("Loading..." if loading else "Refresh")

    def set_cases(self, cases: list[dict]):
        self.cases = cases
        self.case_list.clear()
        for case in cases:
            urgency = (case.get("urgency") or "routine").upper()
            self.case_list.addItem(
                f"Case #{case['case_id']}  |  {case['status'].title()}  |  {urgency}\n"
                f"{case.get('symptoms', '')[:120]}"
            )
        self.case_list.setVisible(bool(cases))
        self.empty_label.setVisible(not cases)
        self.response_button.setEnabled(bool(cases))

    def set_notifications(self, notifications: list[dict]):
        if notifications:
            self.notification_label.setText(notifications[0]["message"])
        else:
            self.notification_label.setText("No new notifications")

    def _request_response(self):
        row = self.case_list.currentRow()
        if 0 <= row < len(self.cases):
            self.response_requested.emit(int(self.cases[row]["case_id"]))
