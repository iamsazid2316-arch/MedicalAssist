from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class LoginPage(QWidget):
    login_requested = Signal(str, str, str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(260, 80, 260, 80)
        layout.setSpacing(12)

        title = QLabel("MedicalAssist")
        title.setObjectName("pageTitle")
        title.setAlignment(Qt.AlignCenter)
        subtitle = QLabel("Safe medical assistance with doctor oversight")
        subtitle.setAlignment(Qt.AlignCenter)

        self.connection_label = QLabel("Checking server connection...")
        self.connection_label.setAlignment(Qt.AlignCenter)
        self.connection_label.setObjectName("mutedText")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username or ID")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self._submit)

        self.role_input = QComboBox()
        self.role_input.addItems(["Cadet", "Doctor"])

        self.error_label = QLabel()
        self.error_label.setWordWrap(True)
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setObjectName("errorText")
        self.error_label.hide()

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self._submit)

        demo_hint = QLabel(
            "Demo: TestCadet / test123   |   TestDoctor / doctor123"
        )
        demo_hint.setAlignment(Qt.AlignCenter)
        demo_hint.setObjectName("mutedText")

        for widget in (
            title,
            subtitle,
            self.connection_label,
            self.username_input,
            self.password_input,
            self.role_input,
            self.error_label,
            self.login_button,
            demo_hint,
        ):
            layout.addWidget(widget)

    def _submit(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        if not username or not password:
            self.show_error("Enter both your username and password.")
            return
        self.show_error("")
        self.login_requested.emit(username, password, self.role_input.currentText().lower())

    def set_loading(self, loading: bool):
        self.login_button.setDisabled(loading)
        self.username_input.setDisabled(loading)
        self.password_input.setDisabled(loading)
        self.role_input.setDisabled(loading)
        self.login_button.setText("Signing in..." if loading else "Login")

    def show_error(self, message: str):
        self.error_label.setText(message)
        self.error_label.setVisible(bool(message))

    def set_connection(self, connected: bool):
        self.connection_label.setText(
            "Server connected" if connected else "Server unavailable - start the backend"
        )
        self.connection_label.setProperty("connected", connected)
        self.connection_label.style().unpolish(self.connection_label)
        self.connection_label.style().polish(self.connection_label)

    def reset(self):
        self.set_loading(False)
        self.password_input.clear()
        self.show_error("")
