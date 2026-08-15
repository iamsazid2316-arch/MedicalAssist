import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


app = QApplication(sys.argv)

window = MainWindow()
window.resize(900, 600)
window.show()

sys.exit(app.exec())