from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        title = QLabel("MedicalAssist")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Medical Assistance System")
        subtitle.setAlignment(Qt.AlignCenter)

        username_label = QLabel("Username / ID")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username or ID")

        password_label = QLabel("Password")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)

        role_label = QLabel("Role")

        self.role_input = QComboBox()
        self.role_input.addItems(["Cadet", "Doctor"])

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.show_loading)

        self.error_label = QLabel()
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet("color: red;")
        self.error_label.hide()

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addSpacing(20)

        main_layout.addWidget(username_label)
        main_layout.addWidget(self.username_input)

        main_layout.addWidget(password_label)
        main_layout.addWidget(self.password_input)

        main_layout.addWidget(role_label)
        main_layout.addWidget(self.role_input)

        main_layout.addWidget(self.error_label)

        main_layout.addSpacing(10)
        main_layout.addWidget(self.login_button)

        self.setLayout(main_layout)

    def show_loading(self):
        self.login_button.setText("Logging in...")
        self.login_button.setEnabled(False)

        self.username_input.setEnabled(False)
        self.password_input.setEnabled(False)
        self.role_input.setEnabled(False)