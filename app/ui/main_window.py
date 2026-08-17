from __future__ import annotations

from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot
from PySide6.QtWidgets import QMainWindow, QMessageBox, QStackedWidget

from app.api_client import ApiClient, ApiError
from app.ui.pages.cadet_dashboard import CadetDashboard
from app.ui.pages.case_view import CaseView
from app.ui.pages.consultation import Consultation
from app.ui.pages.doctor_dashboard import DoctorDashboard
from app.ui.pages.login_page import LoginPage


class WorkerSignals(QObject):
    success = Signal(object)
    error = Signal(str)
    finished = Signal()


class ApiWorker(QRunnable):
    def __init__(self, operation: Callable[[], Any]):
        super().__init__()
        self.operation = operation
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            self.signals.success.emit(self.operation())
        except ApiError as exc:
            self.signals.error.emit(str(exc))
        except Exception:
            self.signals.error.emit("An unexpected error occurred. Please try again.")
        finally:
            self.signals.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self, api_client: ApiClient | None = None):
        super().__init__()
        self.api = api_client or ApiClient()
        self.thread_pool = QThreadPool.globalInstance()
        self._workers: set[ApiWorker] = set()

        self.setWindowTitle("MedicalAssist")
        self.resize(1100, 760)
        self.setMinimumSize(820, 600)

        self.pages = QStackedWidget()
        self.login_page = LoginPage()
        self.cadet_dashboard = CadetDashboard()
        self.doctor_dashboard = DoctorDashboard()
        self.case_view = CaseView()
        self.consultation = Consultation()
        for page in (
            self.login_page,
            self.cadet_dashboard,
            self.doctor_dashboard,
            self.case_view,
            self.consultation,
        ):
            self.pages.addWidget(page)
        self.setCentralWidget(self.pages)
        self.pages.setCurrentWidget(self.login_page)

        self.login_page.login_requested.connect(self.login)
        self.cadet_dashboard.consultation_requested.connect(self.open_consultation)
        self.cadet_dashboard.refresh_requested.connect(self.refresh_cadet_dashboard)
        self.cadet_dashboard.response_requested.connect(self.show_doctor_response)
        self.cadet_dashboard.logout_requested.connect(self.logout)
        self.consultation.message_requested.connect(self.send_consultation_message)
        self.consultation.back_requested.connect(self.go_to_cadet_dashboard)
        self.doctor_dashboard.refresh_requested.connect(self.refresh_doctor_dashboard)
        self.doctor_dashboard.case_requested.connect(self.open_doctor_case)
        self.doctor_dashboard.logout_requested.connect(self.logout)
        self.case_view.back_requested.connect(self.go_to_doctor_dashboard)
        self.case_view.decision_requested.connect(self.submit_doctor_decision)

        self.statusBar().showMessage(f"API: {self.api.base_url}")
        self._check_connection()

    def _run(
        self,
        operation: Callable[[], Any],
        success: Callable[[Any], None],
        error: Callable[[str], None],
        finished: Callable[[], None] | None = None,
    ):
        worker = ApiWorker(operation)
        self._workers.add(worker)
        worker.signals.success.connect(success)
        worker.signals.error.connect(error)
        if finished:
            worker.signals.finished.connect(finished)
        worker.signals.finished.connect(lambda: self._workers.discard(worker))
        self.thread_pool.start(worker)

    def _check_connection(self):
        self._run(
            self.api.health,
            lambda _data: self._set_connected(True),
            lambda _message: self._set_connected(False),
        )

    def _set_connected(self, connected: bool):
        self.login_page.set_connection(connected)
        self.statusBar().showMessage(
            f"{'Connected to' if connected else 'Cannot reach'} {self.api.base_url}"
        )

    @Slot(str, str, str)
    def login(self, username: str, password: str, expected_role: str):
        self.login_page.set_loading(True)

        def success(data: dict):
            if data.get("role") != expected_role:
                self.api.logout()
                self.login_page.show_error(
                    f"This account is registered as {data.get('role', 'another role')}."
                )
                return
            name = data.get("name", username)
            if data["role"] == "cadet":
                self.cadet_dashboard.set_user(name)
                self.pages.setCurrentWidget(self.cadet_dashboard)
                self.refresh_cadet_dashboard()
            else:
                self.doctor_dashboard.set_user(name)
                self.pages.setCurrentWidget(self.doctor_dashboard)
                self.refresh_doctor_dashboard()

        self._run(
            lambda: self.api.login(username, password),
            success,
            self.login_page.show_error,
            lambda: self.login_page.set_loading(False),
        )

    def logout(self):
        self.api.logout()
        self.login_page.reset()
        self.pages.setCurrentWidget(self.login_page)
        self._check_connection()

    def refresh_cadet_dashboard(self):
        self.cadet_dashboard.set_loading(True)

        def load():
            return self.api.get_cases(), self.api.get_notifications()

        def success(data: tuple[list[dict], list[dict]]):
            cases, notifications = data
            self.cadet_dashboard.set_cases(cases)
            self.cadet_dashboard.set_notifications(notifications)

        self._run(
            load,
            success,
            self._show_dashboard_error,
            lambda: self.cadet_dashboard.set_loading(False),
        )

    def _show_dashboard_error(self, message: str):
        self.statusBar().showMessage(message)
        QMessageBox.warning(self, "MedicalAssist", message)

    def open_consultation(self):
        self.consultation.reset()
        self.pages.setCurrentWidget(self.consultation)

    def send_consultation_message(self, message: str):
        self.consultation.set_loading(True)

        if self.consultation.case_id is None:
            def operation():
                created = self.api.create_case(message)
                response = self.api.ask_assistant(created["case_id"], message)
                return created, response

            def success(result: tuple[dict, dict]):
                created, response = result
                self.consultation.set_case(
                    created["case_id"], response["status"], response["urgency"]
                )
                self.consultation.add_message("MedicalAssist", response["message"])
        else:
            case_id = self.consultation.case_id

            def operation():
                return self.api.ask_assistant(case_id, message)

            def success(response: dict):
                self.consultation.set_case(
                    response["case_id"], response["status"], response["urgency"]
                )
                self.consultation.add_message("MedicalAssist", response["message"])

        self._run(
            operation,
            success,
            self.consultation.show_error,
            lambda: self.consultation.set_loading(False),
        )

    def go_to_cadet_dashboard(self):
        self.pages.setCurrentWidget(self.cadet_dashboard)
        self.refresh_cadet_dashboard()

    def show_doctor_response(self, case_id: int):
        def success(data: dict):
            title = "Emergency response" if data["decision"] == "emergency" else "Doctor response"
            QMessageBox.information(self, title, data["response"])

        self._run(
            lambda: self.api.get_case_response(case_id),
            success,
            self._show_dashboard_error,
        )

    def refresh_doctor_dashboard(self):
        self.doctor_dashboard.set_loading(True)

        def load():
            return self.api.get_doctor_cases(), self.api.get_notifications()

        def success(data: tuple[list[dict], list[dict]]):
            cases, notifications = data
            self.doctor_dashboard.set_cases(cases)
            self.doctor_dashboard.set_notifications(notifications)

        self._run(
            load,
            success,
            self._show_dashboard_error,
            lambda: self.doctor_dashboard.set_loading(False),
        )

    def open_doctor_case(self, case_id: int):
        self.doctor_dashboard.set_loading(True)

        def success(data: dict):
            self.case_view.load_case(data)
            self.pages.setCurrentWidget(self.case_view)

        self._run(
            lambda: self.api.get_doctor_case(case_id),
            success,
            self._show_dashboard_error,
            lambda: self.doctor_dashboard.set_loading(False),
        )

    def submit_doctor_decision(self, case_id: int, decision: str, response: str):
        self.case_view.set_loading(True)

        def success(data: dict):
            QMessageBox.information(
                self,
                "Decision saved",
                f"Case #{data['case_id']} is now {data['status']}.",
            )
            self.go_to_doctor_dashboard()

        self._run(
            lambda: self.api.submit_doctor_decision(case_id, decision, response),
            success,
            self.case_view.show_error,
            lambda: self.case_view.set_loading(False),
        )

    def go_to_doctor_dashboard(self):
        self.pages.setCurrentWidget(self.doctor_dashboard)
        self.refresh_doctor_dashboard()

    def closeEvent(self, event):
        self.api.close()
        super().closeEvent(event)
