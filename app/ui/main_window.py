from PySide6.QtWidgets import QMainWindow, QStackedWidget

from .pages.login_page import LoginPage
from .pages.cadet_dashboard import CadetDashboard
from .pages.doctor_dashboard import DoctorDashboard
from .pages.case_view import CaseView
from .pages.consultation import Consultation


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # -------------------------------------------------
        # Main Window
        # -------------------------------------------------

        self.setWindowTitle(
            "Medical Assistance System"
        )

        self.resize(
            1100,
            800
        )

        # -------------------------------------------------
        # Pages
        # -------------------------------------------------

        self.pages = QStackedWidget()

        self.login_page = LoginPage()
        self.cadet_dashboard = CadetDashboard()
        self.doctor_dashboard = DoctorDashboard()
        self.case_view = CaseView()
        self.consultation = Consultation()

        # -------------------------------------------------
        # Add Pages
        # -------------------------------------------------

        self.pages.addWidget(
            self.login_page
        )

        self.pages.addWidget(
            self.cadet_dashboard
        )

        self.pages.addWidget(
            self.doctor_dashboard
        )

        self.pages.addWidget(
            self.case_view
        )

        self.pages.addWidget(
            self.consultation
        )

        self.setCentralWidget(
            self.pages
        )

        # -------------------------------------------------
        # Start With Login
        # -------------------------------------------------

        self.pages.setCurrentWidget(
            self.login_page
        )

        # =================================================
        # LOGIN
        # =================================================

        self.login_page.login_button.clicked.connect(
            self.handle_login
        )

        # =================================================
        # CADET DASHBOARD
        # =================================================

        self.cadet_dashboard.consultation_button.clicked.connect(
            self.open_consultation
        )

        self.cadet_dashboard.logout_button.clicked.connect(
            self.logout
        )

        # =================================================
        # CONSULTATION
        # =================================================

        self.consultation.back_button.clicked.connect(
            self.go_to_cadet_dashboard
        )

        # =================================================
        # DOCTOR DASHBOARD
        # =================================================

        self.doctor_dashboard.review_button.clicked.connect(
            self.open_selected_case
        )

        self.doctor_dashboard.logout_button.clicked.connect(
            self.logout
        )

        # =================================================
        # CASE VIEW
        # =================================================

        self.case_view.back_button.clicked.connect(
            self.go_to_doctor_dashboard
        )

        self.case_view.approve_button.clicked.connect(
            self.approve_case
        )

        self.case_view.reject_button.clicked.connect(
            self.reject_case
        )

    # =====================================================
    # LOGIN
    # =====================================================

    def handle_login(self):

        role = (
            self.login_page
            .role_input
            .currentText()
        )

        if role == "Cadet":

            self.pages.setCurrentWidget(
                self.cadet_dashboard
            )

        elif role == "Doctor":

            self.pages.setCurrentWidget(
                self.doctor_dashboard
            )

        # Reset Login Button

        self.login_page.login_button.setText(
            "Login"
        )

        self.login_page.login_button.setEnabled(
            True
        )

        self.login_page.username_input.setEnabled(
            True
        )

        self.login_page.password_input.setEnabled(
            True
        )

        self.login_page.role_input.setEnabled(
            True
        )

    # =====================================================
    # LOGOUT
    # =====================================================

    def logout(self):

        self.pages.setCurrentWidget(
            self.login_page
        )

        # Clear login fields

        self.login_page.username_input.clear()

        self.login_page.password_input.clear()

        # Reset role

        self.login_page.role_input.setCurrentIndex(
            0
        )

        # Reset login button

        self.login_page.login_button.setText(
            "Login"
        )

        self.login_page.login_button.setEnabled(
            True
        )

        self.login_page.username_input.setEnabled(
            True
        )

        self.login_page.password_input.setEnabled(
            True
        )

        self.login_page.role_input.setEnabled(
            True
        )

    # =====================================================
    # CADET → CONSULTATION
    # =====================================================

    def open_consultation(self):

        self.pages.setCurrentWidget(
            self.consultation
        )

    # =====================================================
    # CONSULTATION → CADET
    # =====================================================

    def go_to_cadet_dashboard(self):

        self.pages.setCurrentWidget(
            self.cadet_dashboard
        )

    # =====================================================
    # DOCTOR → CASE VIEW
    # =====================================================

    def open_selected_case(self):

        case_id = (
            self.doctor_dashboard
            .pending_cases
            .currentText()
        )

        if not case_id:
            return

        case_data = (
            self.doctor_dashboard
            .case_data
            .get(case_id)
        )

        if case_data is None:
            return

        self.case_view.load_case(
            case_id,
            case_data
        )

        self.pages.setCurrentWidget(
            self.case_view
        )

    # =====================================================
    # APPROVE CASE
    # =====================================================

    def approve_case(self):

        if not hasattr(
            self.case_view,
            "current_case_id"
        ):
            return

        if not self.case_view.current_case_id:
            return

        self.case_view.status.setText(
            "Case Status: Approved"
        )

    # =====================================================
    # REJECT CASE
    # =====================================================

    def reject_case(self):

        if not hasattr(
            self.case_view,
            "current_case_id"
        ):
            return

        if not self.case_view.current_case_id:
            return

        self.case_view.status.setText(
            "Case Status: Rejected"
        )

    # =====================================================
    # CASE VIEW → DOCTOR DASHBOARD
    # =====================================================

    def go_to_doctor_dashboard(self):

        self.pages.setCurrentWidget(
            self.doctor_dashboard
        )
