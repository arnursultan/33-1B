import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QDialog, QWidget, QLabel, QVBoxLayout, QProgressBar
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer

from core.db import init_pool, close_pool
from core.models import init_all_tables

from app.auth_dialog import LoginDialog
from app.main_window import MainWindow

from config.user_settings import load_settings
from app.widgets.theme import apply_theme


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(500, 330)

        self.setWindowOpacity(0.0)

        pix = QPixmap("splash.png").scaled(
            200, 200,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.logo = QLabel()
        self.logo.setPixmap(pix)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo)

        self.text = QLabel("Loading system…")
        self.text.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 5px;")
        self.text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.text)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setFixedWidth(300)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #555;
                border-radius: 6px;
                height: 10px;
            }
            QProgressBar::chunk {
                background-color: #0078FF;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.progress)

    def fade_in(self, duration=600):
        self.anim_in = QPropertyAnimation(self, b"windowOpacity")
        self.anim_in.setDuration(duration)
        self.anim_in.setStartValue(0)
        self.anim_in.setEndValue(1)
        self.anim_in.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anim_in.start()

    def fade_out(self, duration=600, finished_callback=None):
        self.anim_out = QPropertyAnimation(self, b"windowOpacity")
        self.anim_out.setDuration(duration)
        self.anim_out.setStartValue(1)
        self.anim_out.setEndValue(0)
        self.anim_out.setEasingCurve(QEasingCurve.Type.InOutCubic)

        if finished_callback:
            self.anim_out.finished.connect(finished_callback)

        self.anim_out.start()


def main():
    app = QApplication(sys.argv)

    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("academy.pro")
    except Exception:
        pass

    BASE = Path(__file__).resolve().parent
    ICON_PATH = BASE / "app" / "icon.ico"
    print("APP ICON:", ICON_PATH, ICON_PATH.exists())
    app.setWindowIcon(QIcon(str(ICON_PATH)))

    settings = load_settings()
    apply_theme(settings.get("theme", "dark"))

    splash = SplashScreen()
    splash.show()
    splash.fade_in()

    def load_backend():
        init_pool()
        init_all_tables()

        def after_fade_out():
            splash.close()

            login = LoginDialog()

            if login.exec() == QDialog.DialogCode.Accepted:
                window = MainWindow(current_user=login.user)
                window.show()
            else:
                close_pool()
                sys.exit()

        splash.fade_out(finished_callback=after_fade_out)

    QTimer.singleShot(800, load_backend)

    exit_code = app.exec()
    close_pool()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
