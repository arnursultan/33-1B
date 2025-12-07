from pathlib import Path
from PyQt6.QtGui import QIcon
from config.user_settings import load_settings, save_settings


class IconLoader:

    ICON_DIR = Path(__file__).resolve().parent.parent / "icons"
    subscribers = []
    theme = None

    @staticmethod
    def load_theme():
        settings = load_settings()
        IconLoader.theme = settings.get("theme", "dark").lower()

    @staticmethod
    def set_theme(theme: str):
        theme = theme.lower()

        settings = load_settings()
        settings["theme"] = theme
        save_settings(settings)

        IconLoader.theme = theme

    @staticmethod
    def get(name: str) -> QIcon:

        if IconLoader.theme is None:
            IconLoader.load_theme()

        filename = name.lower() + ".png"
        path = IconLoader.ICON_DIR / IconLoader.theme / filename
        return QIcon(str(path))

    @staticmethod
    def subscribe(widget):
        IconLoader.subscribers.append(widget)

    @staticmethod
    def refresh_all():
        for widget in IconLoader.subscribers:
            if hasattr(widget, "refresh_icons"):
                widget.refresh_icons()
