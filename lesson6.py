import psycopg2
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
)
import sys

def get_connection():
    return psycopg2.connect(
        host='localhost',
        port='5433',
        database='academy',
        user='postgres',
        password='1234',
    )

def fetch_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, age, email FROM students ORDER BY id;")
    rows = cur.fetchall()
    conn.close()
    return rows

def search_students(text):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, age, email FROM students WHERE name ILIKE %s;", (f'%{text}%',))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_student(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id = %s;", (student_id,))

def update_students(student_id, name, age, email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE students SET name = %s, age = %s, email = %s WHERE id = %s;",
                (name, age, email, student_id)
                )
    conn.commit()
    conn.close()

class AcademyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Academy CRUD / PyQt6 / PostgreSQL")

        layout = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.search)
        layout.addWidget(self.search_input)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Age", "Email"])
        layout.addWidget(self.table)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя")
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Возраст")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        layout.addWidget(self.name_input)
        layout.addWidget(self.age_input)
        layout.addWidget(self.email_input)

        btns = QHBoxLayout()

        self.btn_update = QPushButton("Изменить")
        self.btn_delete = QPushButton("Удалить")

        btns.addWidget(self.btn_update)
        btns.addWidget(self.btn_delete)

        self.btn_update.clicked.connect(self.update_row)
        self.btn_delete.clicked.connect(self.delete_row)

        layout.addLayout(btns)

        self.setLayout(layout)

    def create_table(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                age INTEGER,
                email VARCHAR(100),
            );
        """)

        conn.commit()
        conn.close()

        self.load_data()

        self.table.cellClicked.connect(self.select_row)

        self.selected_id = None

    def load_data(self):
        rows = fetch_all()
        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

    def search(self, text):
        rows = search_students(text)
        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

    def select_row(self, row, column):
        self.selected_id = int(self.table.item(row, 0).text())
        self.name_input.setText(row(self.table.item(row, 1).text()))
        self.age_input.setText(self.table.item(row, 2).text())
        self.email_input.setText(self.table.item(row, 3).text())

    def delete_row(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите строку.")
            return

        delete_student(self.selected_id)
        QMessageBox.information(self, "Успех", "Запись удалена")

        self.load_data()
        self.selected_id = None

    def update_row(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Ошибка", "Выберите строку для изменения.")
            return

        name = self.name_input.text()
        age = self.age_input.text()
        email = self.email_input.text()

        if not name or not age or not email:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля.")
            return

        update_students(self.selected_id, name, age, email)
        QMessageBox.information(self, "Успех", "Запись успешно изменена.")

        self.load_data()

app = QApplication(sys.argv)
window = AcademyApp()
window.show()
sys.exit(app.exec())