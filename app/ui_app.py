import sys

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


app = QApplication(sys.argv)

app.setFont(
    QFont("Arial", 14)
)

app.setStyleSheet("""
    QWidget {
        background-color: #f5f7fa;
        color: #1f2937;
    }

    QLabel {
        color: #1f2937;
    }

    QLineEdit,
    QComboBox {
        background-color: white;
        color: #1f2937;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 8px;
    }

    QPushButton {
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 9px 16px;
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


window = MainWindow()
window.resize(900, 600)
window.show()

sys.exit(app.exec())