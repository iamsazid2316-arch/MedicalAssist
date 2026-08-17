from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class DoctorDashboard(QWidget):
    refresh_requested = Signal()
    case_requested = Signal(int)
    logout_requested = Signal()

    def __init__(self):
        super().__init__()
        self.cases: list[dict] = []
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(12)

        header = QHBoxLayout()
        self.title = QLabel("Doctor Dashboard")
        self.title.setObjectName("pageTitle")
        self.counter = QLabel("0 active cases")
        self.counter.setObjectName("statusBadge")
        self.refresh_button = QPushButton("Refresh")
        self.logout_button = QPushButton("Logout")
        self.refresh_button.clicked.connect(self.refresh_requested.emit)
        self.logout_button.clicked.connect(self.logout_requested.emit)
        header.addWidget(self.title)
        header.addStretch()
        header.addWidget(self.counter)
        header.addWidget(self.refresh_button)
        header.addWidget(self.logout_button)

        self.notification_label = QLabel("No new notifications")
        self.notification_label.setWordWrap(True)
        self.notification_label.setObjectName("infoBanner")

        self.case_list = QListWidget()
        self.case_list.itemDoubleClicked.connect(self._open_case)
        self.empty_label = QLabel("No cases are waiting for review.")
        self.empty_label.setObjectName("mutedText")
        self.review_button = QPushButton("Review selected case")
        self.review_button.clicked.connect(self._open_case)

        layout.addLayout(header)
        layout.addWidget(self.notification_label)
        layout.addWidget(self.case_list, 1)
        layout.addWidget(self.empty_label)
        layout.addWidget(self.review_button)

    def set_user(self, name: str):
        self.title.setText(f"Doctor Dashboard - {name}")

    def set_loading(self, loading: bool):
        self.refresh_button.setDisabled(loading)
        self.review_button.setDisabled(loading or not self.cases)
        self.refresh_button.setText("Loading..." if loading else "Refresh")

    def set_cases(self, cases: list[dict]):
        self.cases = cases
        self.case_list.clear()
        for case in cases:
            self.case_list.addItem(
                f"Case #{case['case_id']} - {case.get('cadet_name', 'Cadet')}\n"
                f"{(case.get('urgency') or 'routine').upper()} | {case['status'].title()} | "
                f"{case.get('symptoms', '')[:100]}"
            )
        self.counter.setText(f"{len(cases)} active case{'s' if len(cases) != 1 else ''}")
        self.case_list.setVisible(bool(cases))
        self.empty_label.setVisible(not cases)
        self.review_button.setEnabled(bool(cases))

    def set_notifications(self, notifications: list[dict]):
        self.notification_label.setText(
            notifications[0]["message"] if notifications else "No new notifications"
        )

    def _open_case(self):
        row = self.case_list.currentRow()
        if 0 <= row < len(self.cases):
            self.case_requested.emit(int(self.cases[row]["case_id"]))
