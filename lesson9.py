import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import QPropertyAnimation, QRect, Qt


class LastApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Last Dance")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setFixedSize(400, 300)

        self.label = QLabel(" PyQt6 работает.", self)
        self.label.setFont(QFont("Arial", 16))
        self.label.setStyleSheet("color: #ffffff;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button = QPushButton("Кликни", self)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #ff4757;
                color: white;
                padding: 10px;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ff6b81;
            }
            """)
        self.button.clicked.connect(self.animate)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setStyleSheet("background-color: #1e272e")

    def animate(self):
        self.anim = QPropertyAnimation(self.button, b"geometry")
        self.anim.setDuration(300)
        self.anim.setStartValue(QRect(120, 160, 160, 40))
        self.anim.setEndValue(QRect(110, 155, 180, 50))
        self.anim.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LastApp()
    window.show()
    sys.exit(app.exec())