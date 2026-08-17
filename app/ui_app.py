import sys
from pathlib import Path

# Keep the original `python app/ui_app.py` launch command working on Windows.
if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from app.ui.main_window import MainWindow


STYLE = """
QWidget { background: #f4f7fb; color: #172033; }
QLabel#pageTitle { font-size: 24px; font-weight: 700; color: #12335b; }
QLabel#sectionTitle { font-size: 17px; font-weight: 650; }
QLabel#mutedText { color: #64748b; }
QLabel#errorText { color: #b42318; }
QLabel#statusBadge { background: #e4efff; color: #174ea6; padding: 6px 10px; border-radius: 10px; }
QLabel#infoBanner { background: #e8f4fd; border: 1px solid #b6d8f2; padding: 10px; border-radius: 7px; }
QLabel#warningBanner { background: #fff5d6; border: 1px solid #f2cf66; padding: 10px; border-radius: 7px; }
QLineEdit, QComboBox, QTextEdit, QTextBrowser, QListWidget {
    background: white; border: 1px solid #cbd5e1; border-radius: 7px; padding: 8px;
}
QPushButton {
    background: #1769aa; color: white; border: 0; border-radius: 7px;
    padding: 9px 15px; font-weight: 600;
}
QPushButton:hover { background: #12568d; }
QPushButton:disabled { background: #a8b4c3; }
QPushButton#dangerButton { background: #b42318; }
QPushButton#dangerButton:hover { background: #8f1c13; }
"""


def main() -> int:
    application = QApplication(sys.argv)
    application.setApplicationName("MedicalAssist")
    application.setFont(QFont("Segoe UI", 11))
    application.setStyleSheet(STYLE)
    window = MainWindow()
    window.show()
    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
