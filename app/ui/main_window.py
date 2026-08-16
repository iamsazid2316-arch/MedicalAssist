from PySide6.QtWidgets import QMainWindow, QStackedWidget

from .pages.login_page import LoginPage
from .pages.cadet_dashboard import CadetDashboard
from .pages.doctor_dashboard import DoctorDashboard
from .pages.case_view import CaseView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Medical Assistance System")

        self.pages = QStackedWidget()

        self.login_page = LoginPage()
        self.cadet_dashboard = CadetDashboard()
        self.doctor_dashboard = DoctorDashboard()
        self.case_view = CaseView()

        self.pages.addWidget(self.login_page)
        self.pages.addWidget(self.cadet_dashboard)
        self.pages.addWidget(self.doctor_dashboard)
        self.pages.addWidget(self.case_view)

        self.setCentralWidget(self.pages)