import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt
import db_5

class DBWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contacts CRUD + DB + PyQt6 — Lesson 5")
        self.setup_ui()
        db_5.init_db()
        self.load_contacts()

    def setup_ui(self):
        lbl_name = QLabel("Name:")
        self.input_name = QLineEdit()
        lbl_email = QLabel("Email:")
        self.input_email = QLineEdit()
        lbl_phone = QLabel("Phone:")
        self.input_phone = QLineEdit()

        btn_add = QPushButton("Добавить")
        btn_add.clicked.connect(self.on_add)

        btn_refresh = QPushButton("Обновить")
        btn_refresh.clicked.connect(self.load_contacts)

        form_layout = QHBoxLayout()
        form_layout.addWidget(lbl_name)
        form_layout.addWidget(self.input_name)
        form_layout.addWidget(lbl_email)
        form_layout.addWidget(self.input_email)
        form_layout.addWidget(lbl_phone)
        form_layout.addWidget(self.input_phone)
        form_layout.addWidget(btn_add)
        form_layout.addWidget(btn_refresh)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Email", "Phone", "Created at"])
        self.table.setColumnHidden(0, False)
        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)
        self.resize(900, 400)

    def on_add(self):
        name = self.input_name.text().strip()
        email = self.input_email.text().strip()
        phone = self.input_phone.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation", "Имя не может быть пустым.")
            return

        try:
            new_id = db_5.create_contact(name, email, phone)
        except Exception as e:
            QMessageBox.critical(self, "DB Error", f"Ошибка при создании контакта: {e}")
            return

        self.input_name.clear()
        self.input_email.clear()
        self.input_phone.clear()
        self.load_contacts()
        QMessageBox.information(self, "Success", f"Контакт добавлен (id={new_id}).")

    def load_contacts(self):
        try:
            rows = db_5.get_all_contacts()
        except Exception as e:
            QMessageBox.critical(self, "DB Error", f"Ошибка при загрузке данных: {e}")
            return

        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                item = QTableWidgetItem(str(value) if value is not None else "")
                if c == 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(r, c, item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = DBWindow()
    w.show()
    sys.exit(app.exec())