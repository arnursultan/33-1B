from PyQt6.QtCore import QObject, pyqtSignal

class Events(QObject):
    theme_changed = pyqtSignal()

events = Events()
