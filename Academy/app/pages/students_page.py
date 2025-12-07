from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLineEdit, QPushButton, QHBoxLayout, QLabel, QMessageBox, QFileDialog
)
from app.controllers.students_controller import StudentsController
from app.widgets.icon_loader import IconLoader
from app.events import events
import csv


class StudentsPage(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.controller = StudentsController()

        IconLoader.subscribe(self)
        events.theme_changed.connect(self.refresh_icons)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Students"))

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Age", "Email"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        form = QHBoxLayout()
        self.name = QLineEdit()
        self.age = QLineEdit()
        self.email = QLineEdit()

        self.name.setPlaceholderText("Name")
        self.age.setPlaceholderText("Age")
        self.email.setPlaceholderText("Email")

        form.addWidget(self.name)
        form.addWidget(self.age)
        form.addWidget(self.email)
        layout.addLayout(form)

        buttons = QHBoxLayout()
        self.btn_add = QPushButton(" Add")
        self.btn_update = QPushButton(" Update")
        self.btn_delete = QPushButton(" Delete")
        self.btn_export = QPushButton(" Export CSV")

        buttons.addWidget(self.btn_add)
        buttons.addWidget(self.btn_update)
        buttons.addWidget(self.btn_delete)
        buttons.addWidget(self.btn_export)

        layout.addLayout(buttons)

        self.table.cellClicked.connect(self.select_row)
        self.btn_add.clicked.connect(self.add)
        self.btn_update.clicked.connect(self.update)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_export.clicked.connect(self.export_csv)

        self.selected_id = None

        if user.role != "admin":
            self.btn_add.hide()
            self.btn_update.hide()
            self.btn_delete.hide()

        self.refresh_icons()
        self.load()

    def refresh_icons(self):
        self.btn_add.setIcon(IconLoader.get("add"))
        self.btn_update.setIcon(IconLoader.get("edit"))
        self.btn_delete.setIcon(IconLoader.get("delete"))
        self.btn_export.setIcon(IconLoader.get("export") or IconLoader.get("students"))

    def load(self):
        rows = self.controller.get_all()
        self.table.setRowCount(len(rows))
        for i, r in enumerate(rows):
            for j, v in enumerate(r):
                self.table.setItem(i, j, QTableWidgetItem(str(v)))

    def select_row(self, row, col):
        self.selected_id = int(self.table.item(row, 0).text())
        self.name.setText(self.table.item(row, 1).text())
        self.age.setText(self.table.item(row, 2).text())
        self.email.setText(self.table.item(row, 3).text())

    def add(self):
        msg = self.controller.add(
            self.name.text(),
            self.age.text(),
            self.email.text()
        )
        if msg != "ok":
            QMessageBox.warning(self, "Error", msg)
            return
        self.load()

    def update(self):
        msg = self.controller.update(
            self.selected_id,
            self.name.text(),
            self.age.text(),
            self.email.text()
        )
        if msg != "ok":
            QMessageBox.warning(self, "Error", msg)
            return
        self.load()

    def delete(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Error", "Select a student first")
            return

        reply = QMessageBox.question(
            self,
            "Confirm delete",
            "Are you sure you want to delete this student?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        msg = self.controller.delete(self.selected_id)
        if msg != "ok":
            QMessageBox.warning(self, "Error", msg)
            return

        self.selected_id = None
        self.load()

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export students to CSV",
            "students.csv",
            "CSV Files (*.csv)"
        )
        if not path:
            return

        rows = self.controller.get_all()
        headers = ["ID", "Name", "Age", "Email"]

        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                for row in rows:
                    writer.writerow(row)
            QMessageBox.information(self, "Done", "Students exported successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export: {e}")
