from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)


class Consultation(QWidget):
    message_requested = Signal(str)
    back_requested = Signal()

    def __init__(self):
        super().__init__()
        self.case_id: int | None = None
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)

        header = QHBoxLayout()
        title = QLabel("Medical Consultation")
        title.setObjectName("pageTitle")
        self.status_label = QLabel("New consultation")
        self.status_label.setObjectName("statusBadge")
        self.back_button = QPushButton("Back to dashboard")
        self.back_button.clicked.connect(self.back_requested.emit)
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.status_label)
        header.addWidget(self.back_button)

        safety = QLabel(
            "This assistant does not diagnose or prescribe. A doctor reviews submitted cases. "
            "For severe or life-threatening symptoms, contact emergency services immediately."
        )
        safety.setWordWrap(True)
        safety.setObjectName("warningBanner")

        self.transcript = QTextBrowser()
        self.transcript.setOpenExternalLinks(False)
        self.typing_indicator = QLabel("MedicalAssist is preparing a response...")
        self.typing_indicator.setObjectName("mutedText")
        self.typing_indicator.hide()

        input_row = QHBoxLayout()
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Describe your symptoms and how long you have had them")
        self.message_input.returnPressed.connect(self._send)
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self._send)
        input_row.addWidget(self.message_input, 1)
        input_row.addWidget(self.send_button)

        layout.addLayout(header)
        layout.addWidget(safety)
        layout.addWidget(self.transcript, 1)
        layout.addWidget(self.typing_indicator)
        layout.addLayout(input_row)
        self.reset()

    def reset(self):
        self.case_id = None
        self.status_label.setText("New consultation")
        self.transcript.clear()
        self.add_message(
            "MedicalAssist",
            "Hello. Describe your main symptoms, duration, and severity.",
        )
        self.set_loading(False)

    def set_case(self, case_id: int, status: str, urgency: str):
        self.case_id = case_id
        self.status_label.setText(
            f"Case #{case_id} - {status.title()} - {urgency.title()}"
        )

    def add_message(self, sender: str, message: str):
        safe = (
            message.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br>")
        )
        self.transcript.append(f"<p><b>{sender}:</b> {safe}</p>")

    def set_loading(self, loading: bool):
        self.message_input.setDisabled(loading)
        self.send_button.setDisabled(loading)
        self.back_button.setDisabled(loading)
        self.send_button.setText("Sending..." if loading else "Send")
        self.typing_indicator.setVisible(loading)

    def show_error(self, message: str):
        self.add_message("System", message)

    def _send(self):
        message = self.message_input.text().strip()
        if not message or self.send_button.isEnabled() is False:
            return
        self.message_input.clear()
        self.add_message("You", message)
        self.message_requested.emit(message)
