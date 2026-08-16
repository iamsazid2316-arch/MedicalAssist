from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)


class ConsultationScreen(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        title = QLabel("Medical Consultation")
        title.setAlignment(Qt.AlignCenter)

        chatbot_title = QLabel("MedicalAssist AI")
        chatbot_title.setAlignment(Qt.AlignCenter)

        status_label = QLabel("Consultation Status: Active")
        status_label.setAlignment(Qt.AlignCenter)

        ai_message = QLabel(
            "AI: Hello! Please describe your medical problem."
        )
        ai_message.setWordWrap(True)

        cadet_message = QLabel(
            "Cadet: I have a headache."
        )
        cadet_message.setWordWrap(True)

        self.typing_indicator = QLabel(
            "MedicalAssist is typing..."
        )
        self.typing_indicator.setAlignment(Qt.AlignCenter)
        self.typing_indicator.hide()

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText(
            "Type your medical message..."
        )

        self.send_button = QPushButton("Send")

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)

        main_layout.addWidget(title)
        main_layout.addWidget(chatbot_title)
        main_layout.addWidget(status_label)
        main_layout.addSpacing(20)

        main_layout.addWidget(ai_message)
        main_layout.addWidget(cadet_message)
        main_layout.addWidget(self.typing_indicator)

        main_layout.addStretch()

        main_layout.addLayout(input_layout)

        self.setLayout(main_layout)