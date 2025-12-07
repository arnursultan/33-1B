from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QFile
from app.widgets.icon_loader import IconLoader
from app.events import events

def apply_theme(theme="dark"):
    IconLoader.set_theme(theme)

    file = QFile(f"app/theme/{theme}.qss")
    file.open(QFile.OpenModeFlag.ReadOnly)
    qss = file.readAll().data().decode()
    QApplication.instance().setStyleSheet(qss)

    events.theme_changed.emit()
    IconLoader.refresh_all()
