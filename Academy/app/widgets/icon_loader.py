from PyQt6.QtGui import QIcon


class IconLoader:
    current_theme = "dark"
    subscribers = []

    @staticmethod
    def set_theme(theme: str):
        IconLoader.current_theme = theme

    @staticmethod
    def load(name: str) -> QIcon:
        return QIcon(f"app/icons/{IconLoader.current_theme}/{name}.png")

    @staticmethod
    def subscribe(widget):
        IconLoader.subscribers.append(widget)

    @staticmethod
    def refresh_all():
        for w in IconLoader.subscribers:
            if hasattr(w, "refresh_icons"):
                w.refresh_icons()
