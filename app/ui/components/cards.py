from PySide6.QtWidgets import QFrame, QVBoxLayout


class Card(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFrameShape(QFrame.StyledPanel)

        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 12px;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 12, 12, 12)

    def add_widget(self, widget):
        self.layout.addWidget(widget)