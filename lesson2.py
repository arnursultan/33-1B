# import sys
# from PyQt6.QtWidgets import QApplication, QWidget
#
# def main():
#     app = QApplication(sys.argv)
#
#     window = QWidget()
#     window.setWindowTitle("Наше первое окно на PyQt6!")
#     window.resize(400, 300)
#
#     window.show()
#
#     sys.exit(app.exec())
#
# if __name__ == '__main__':
#     main()

import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QMessageBox,
)

def calculate_sum(data: list[int]) -> int:
    return sum(data)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Код с декомпозицией на PyQt6")
        self.resize(400, 300)

        self.button = QPushButton("Посчитать сумму", parent=self)
        self.button.move(120,120)

        self.button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        s = calculate_sum(numbers)
        self.show_result(s)

    def show_result(self, result: int):
        msg = QMessageBox(self)
        msg.setWindowTitle("Результат")
        msg.setText(f"Сумма чисел: {result}")
        msg.exec()

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()