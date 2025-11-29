import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget,QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt
import db_5

class DBWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contacts CRUD + DB + PyQt6 — Lesson 5")
        self.setup_ui()
        db.init_db()
        self.load_contacts()
