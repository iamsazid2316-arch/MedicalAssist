from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextBrowser,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class CaseView(QWidget):
    back_requested = Signal()
    decision_requested = Signal(int, str, str)

    def __init__(self):
        super().__init__()
        self.case_id: int | None = None
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)

        header = QHBoxLayout()
        self.title = QLabel("Case Review")
        self.title.setObjectName("pageTitle")
        self.status = QLabel("No case selected")
        self.status.setObjectName("statusBadge")
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back_requested.emit)
        header.addWidget(self.title)
        header.addStretch()
        header.addWidget(self.status)
        header.addWidget(self.back_button)

        details = QGridLayout()
        self.patient_info = QLabel("Cadet: -")
        self.urgency = QLabel("Urgency: -")
        self.symptoms = QLabel("Symptoms: -")
        self.symptoms.setWordWrap(True)
        details.addWidget(self.patient_info, 0, 0)
        details.addWidget(self.urgency, 0, 1)
        details.addWidget(self.symptoms, 1, 0, 1, 2)

        conversation_title = QLabel("Consultation history")
        conversation_title.setObjectName("sectionTitle")
        self.conversation = QTextBrowser()

        response_title = QLabel("Doctor response")
        response_title.setObjectName("sectionTitle")
        self.response_input = QTextEdit()
        self.response_input.setPlaceholderText(
            "Enter the safe, final response that may be shown to the cadet"
        )
        self.response_input.setMaximumHeight(150)
        self.feedback = QLabel()
        self.feedback.setObjectName("errorText")

        buttons = QHBoxLayout()
        for label, decision in (
            ("Approve", "approve"),
            ("Modify & approve", "modify"),
            ("Reject", "reject"),
            ("Emergency", "emergency"),
        ):
            button = QPushButton(label)
            if decision == "emergency":
                button.setObjectName("dangerButton")
            button.clicked.connect(
                lambda _checked=False, selected=decision: self._submit(selected)
            )
            buttons.addWidget(button)
        self.decision_buttons = [buttons.itemAt(i).widget() for i in range(buttons.count())]

        layout.addLayout(header)
        layout.addLayout(details)
        layout.addWidget(conversation_title)
        layout.addWidget(self.conversation, 1)
        layout.addWidget(response_title)
        layout.addWidget(self.response_input)
        layout.addWidget(self.feedback)
        layout.addLayout(buttons)

    def load_case(self, case: dict):
        self.case_id = int(case["case_id"])
        self.title.setText(f"Case #{self.case_id}")
        self.status.setText(case.get("status", "pending").title())
        self.patient_info.setText(
            f"Cadet: {case.get('cadet_name', 'Unknown')} (ID {case.get('cadet_id', '-')})"
        )
        self.urgency.setText(f"Urgency: {(case.get('urgency') or 'routine').title()}")
        self.symptoms.setText(f"Symptoms: {case.get('symptoms', '')}")
        self.conversation.clear()
        for message in case.get("messages", []):
            sender = message.get("sender", "unknown").title()
            text = str(message.get("message", ""))
            safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            self.conversation.append(f"<p><b>{sender}:</b> {safe}</p>")
        if not case.get("messages"):
            self.conversation.setPlainText("No consultation messages were recorded.")
        self.response_input.clear()
        self.feedback.clear()
        self.set_loading(False)

    def set_loading(self, loading: bool):
        self.back_button.setDisabled(loading)
        self.response_input.setDisabled(loading)
        for button in self.decision_buttons:
            button.setDisabled(loading)

    def show_error(self, message: str):
        self.feedback.setText(message)

    def _submit(self, decision: str):
        response = self.response_input.toPlainText().strip()
        if self.case_id is None:
            return
        if not response:
            self.show_error("Enter a doctor response before making a decision.")
            return
        self.show_error("")
        self.decision_requested.emit(self.case_id, decision, response)
