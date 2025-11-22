import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget,
    QLabel, QPushButton, QLineEdit, QTextEdit,
    QCheckBox, QRadioButton, QComboBox, QSlider,
    QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox
)
from PyQt6.QtGui import QFont, QPalette, QColor


class WidgetsDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Урок 3 — базовые виджеты PyQt6")
        self.resize(650, 480)

        layout = QVBoxLayout()
        layout.addWidget(self.block_text())
        layout.addWidget(self.block_clicks())
        layout.addWidget(self.block_checkbox_text())
        layout.addWidget(self.block_style())
        layout.addWidget(self.block_mood())
        self.setLayout(layout)

    def block_text(self):
        box = QGroupBox("1. Поле ввода и надпись")
        self.label = QLabel("Здесь будет ваш текст", font=QFont("Arial", 14))
        line = QLineEdit(placeholderText="Введите текст...")
        line.textChanged.connect(self.label.setText)
        lay = QVBoxLayout(); lay.addWidget(self.label); lay.addWidget(line)
        box.setLayout(lay); return box

    def block_clicks(self):
        box = QGroupBox("2. Кнопка и счётчик")
        self.count = 0
        self.counter_label = QLabel("Кнопка ещё не нажималась")
        btn = QPushButton("Нажми меня")
        btn.clicked.connect(self.on_click)
        h = QHBoxLayout(); h.addWidget(btn); h.addWidget(self.counter_label)
        box.setLayout(h); return box

    def on_click(self):
        self.count += 1
        self.counter_label.setText(f"Кнопку нажали {self.count} раз(а)")

    def block_checkbox_text(self):
        box = QGroupBox("3. Чекбокс и текст")
        text = QTextEdit("Здесь можно писать длинный текст...")
        check = QCheckBox("Разрешить редактирование", checked=True)
        check.stateChanged.connect(
            lambda s: text.setReadOnly(s != Qt.CheckState.Checked)
        )
        v = QVBoxLayout(); v.addWidget(check); v.addWidget(text)
        box.setLayout(v); return box

    def block_style(self):
        box = QGroupBox("4. Цвет и размер шрифта")
        colors = {"Чёрный": "black", "Красный": "red", "Синий": "blue"}

        grid = QGridLayout()
        for r, (title, c) in enumerate(colors.items()):
            radio = QRadioButton(title, checked=(r == 0))
            radio.toggled.connect(lambda ch, col=c: ch and self.set_color(col))
            grid.addWidget(radio, r, 0)

        self.font_size_label = QLabel("Размер шрифта: 14")
        slider = QSlider(Qt.Orientation.Horizontal, minimum=8, maximum=40, value=14)
        slider.valueChanged.connect(self.set_font_size)

        grid.addWidget(self.font_size_label, 0, 1)
        grid.addWidget(slider, 1, 1, 2, 1)
        box.setLayout(grid)
        return box

    def set_color(self, color):
        pal = self.label.palette()
        pal.setColor(QPalette.ColorRole.WindowText, QColor(color))
        self.label.setPalette(pal)

    def set_font_size(self, size):
        f = self.label.font(); f.setPointSize(size)
        self.label.setFont(f)
        self.font_size_label.setText(f"Размер шрифта: {size}")

    def block_mood(self):
        box = QGroupBox("5. Настроение")
        mood_label = QLabel("Ваше настроение: неизвестно")
        combo = QComboBox()
        combo.addItems(["Нормально", "Отлично", "Хочу спать", "Зол", "Учусь PyQt6", "Сигма"])
        combo.currentTextChanged.connect(
            lambda t:mood_label.setText(f"Ваше настроение: {t}")
        )
        h = QHBoxLayout(); h.addWidget(combo); h.addWidget(mood_label)
        box.setLayout(h); return box

def main():
    app = QApplication(sys.argv)
    w = WidgetsDemo()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()