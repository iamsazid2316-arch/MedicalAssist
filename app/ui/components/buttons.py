from PySide6.QtWidgets import QPushButton


class PrimaryButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)

        self.setMinimumHeight(40)

        self.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1d4ed8;
            }

            QPushButton:pressed {
                background-color: #1e40af;
            }

            QPushButton:disabled {
                background-color: #9ca3af;
                color: #e5e7eb;
            }
        """)


class ActionButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)

        self.setMinimumHeight(40)

        self.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1f2937;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #f1f5f9;
            }

            QPushButton:pressed {
                background-color: #e2e8f0;
            }

            QPushButton:disabled {
                background-color: #e5e7eb;
                color: #9ca3af;
            }
        """)