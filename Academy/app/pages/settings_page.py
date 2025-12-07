from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox
from PyQt6.QtGui import QFont
from app.widgets.theme import apply_theme
from config.user_settings import load_settings, save_settings


class SettingsPage(QWidget):
    def __init__(self, user, main_window=None):
        super().__init__()

        self.user = user
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        title = QLabel("Settings")
        title.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        layout.addWidget(title)

        theme_label = QLabel("Theme:")
        theme_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Medium))
        layout.addWidget(theme_label)

        btn_light = QPushButton("Light Theme")
        btn_dark = QPushButton("Dark Theme")

        btn_light.setFixedHeight(40)
        btn_dark.setFixedHeight(40)

        btn_light.clicked.connect(lambda: self._change_theme("light"))
        btn_dark.clicked.connect(lambda: self._change_theme("dark"))

        layout.addWidget(btn_light)
        layout.addWidget(btn_dark)

        anim_label = QLabel("Animation Mode:")
        anim_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Medium))
        layout.addWidget(anim_label)

        self.anim_select = QComboBox()
        self.anim_select.setFixedHeight(35)
        self.anim_select.addItems(["fade", "slide", "slide_fade", "flip"])

        settings = load_settings()
        self.anim_select.setCurrentText(settings.get("animation", "slide_fade"))
        self.anim_select.currentTextChanged.connect(self._change_animation)

        layout.addWidget(self.anim_select)

        layout.addStretch()

    def _change_theme(self, theme):
        settings = load_settings()
        settings["theme"] = theme
        save_settings(settings)
        apply_theme(theme)

    def _change_animation(self, mode):
        settings = load_settings()
        settings["animation"] = mode
        save_settings(settings)

        if self.main_window:
            self.main_window.animation_mode = mode
