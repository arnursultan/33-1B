from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from core.repository import UsersRepo


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setFixedSize(320, 200)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Username"))
        self.username = QLineEdit()
        layout.addWidget(self.username)

        layout.addWidget(QLabel("Password"))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password)

        login_btn = QPushButton("Sign In")
        login_btn.clicked.connect(self.try_login)
        layout.addWidget(login_btn)

        self.user = None

    def try_login(self):
        username = self.username.text()
        password = self.password.text()

        repo = UsersRepo()
        user = repo.auth(username, password)

        if not user:
            QMessageBox.warning(self, "Error", "Invalid login or password.")
            return

        self.user = user
        self.accept()
