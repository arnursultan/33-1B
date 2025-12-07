from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLineEdit, QPushButton, QHBoxLayout, QLabel, QComboBox,
    QMessageBox, QFileDialog
)
from app.controllers.teachers_controller import TeachersController
from app.widgets.icon_loader import IconLoader
from app.events import events
import csv


class TeachersPage(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.controller = TeachersController()

        IconLoader.subscribe(self)
        events.theme_changed.connect(self.refresh_icons)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Teachers"))

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Full Name", "Subject", "Email",
            "Phone", "Experience", "Status"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        form = QHBoxLayout()
        self.fn = QLineEdit();   self.fn.setPlaceholderText("Full Name")
        self.subj = QLineEdit(); self.subj.setPlaceholderText("Subject")
        self.email = QLineEdit();self.email.setPlaceholderText("Email")
        self.phone = QLineEdit();self.phone.setPlaceholderText("Phone")
        self.exp = QLineEdit();  self.exp.setPlaceholderText("Experience (years)")

        self.status = QComboBox()
        self.status.addItems(["active", "inactive", "vacation"])

        form.addWidget(self.fn)
        form.addWidget(self.subj)
        form.addWidget(self.email)
        form.addWidget(self.phone)
        form.addWidget(self.exp)
        form.addWidget(self.status)
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
        self.btn_export.setIcon(IconLoader.get("export") or IconLoader.get("teachers"))

    def load(self):
        rows = self.controller.get_all()
        self.table.setRowCount(len(rows))
        for i, r in enumerate(rows):
            for j, v in enumerate(r):
                self.table.setItem(i, j, QTableWidgetItem(str(v)))

    def select_row(self, row, col):
        self.selected_id = int(self.table.item(row, 0).text())
        self.fn.setText(self.table.item(row, 1).text())
        self.subj.setText(self.table.item(row, 2).text())
        self.email.setText(self.table.item(row, 3).text())
        self.phone.setText(self.table.item(row, 4).text())
        self.exp.setText(self.table.item(row, 5).text())
        self.status.setCurrentText(self.table.item(row, 6).text())

    def add(self):
        msg = self.controller.add(
            self.fn.text(), self.subj.text(), self.email.text(),
            self.phone.text(), self.exp.text(), self.status.currentText()
        )
        if msg != "ok":
            QMessageBox.warning(self, "Error", msg)
            return
        self.load()

    def update(self):
        msg = self.controller.update(
            self.selected_id,
            self.fn.text(), self.subj.text(), self.email.text(),
            self.phone.text(), self.exp.text(), self.status.currentText()
        )
        if msg != "ok":
            QMessageBox.warning(self, "Error", msg)
            return
        self.load()

    def delete(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Error", "Select a teacher first")
            return

        reply = QMessageBox.question(
            self,
            "Confirm delete",
            "Are you sure you want to delete this teacher?",
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
            "Export teachers to CSV",
            "teachers.csv",
            "CSV Files (*.csv)"
        )
        if not path:
            return

        rows = self.controller.get_all()
        headers = ["ID", "Full Name", "Subject", "Email", "Phone", "Experience", "Status"]

        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                for row in rows:
                    writer.writerow(row)
            QMessageBox.information(self, "Done", "Teachers exported successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export: {e}")
