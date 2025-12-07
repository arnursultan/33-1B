from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal, QPropertyAnimation, QEasingCurve
from app.events import events
from app.widgets.icon_loader import IconLoader


class Sidebar(QWidget):
    page_changed = pyqtSignal(int)

    def __init__(self, user):
        super().__init__()

        self.expanded = True
        self._anim = None

        self.setFixedWidth(200)
        events.theme_changed.connect(self.refresh_icons)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        self.toggle_btn = QPushButton("☰")
        self.toggle_btn.setObjectName("SidebarToggle")
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        layout.addWidget(self.toggle_btn)

        self.title = QLabel("Academy")
        self.title.setStyleSheet("font-size: 18px; font-weight: bold; margin-left: 4px;")
        layout.addWidget(self.title)

        self.menu = QListWidget()

        menu_items = [
            ("Students", "students"),
            ("Teachers", "teachers"),
            ("Settings", "settings"),
        ]

        for text, icon_name in menu_items:
            item = QListWidgetItem(text)
            item.setIcon(IconLoader.get(icon_name))
            self.menu.addItem(item)

        if user.role != "admin":
            self.menu.takeItem(2)

        self.menu.currentRowChanged.connect(self.page_changed)
        layout.addWidget(self.menu)

        self.menu.setCurrentRow(0)

    def refresh_icons(self):
        for i in range(self.menu.count()):
            item = self.menu.item(i)
            text = item.text()
            icon_name = text.lower()
            item.setIcon(IconLoader.get(icon_name))

        self.menu.repaint()

    def toggle_sidebar(self):
        start = self.width()
        end = 60 if self.expanded else 200
        self.expanded = not self.expanded

        if self._anim:
            self._anim.stop()

        anim = QPropertyAnimation(self, b"minimumWidth")
        anim.setDuration(220)
        anim.setStartValue(start)
        anim.setEndValue(end)
        anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        anim.start()

        self._anim = anim

        if not self.expanded:
            self.title.setText("")
            for i in range(self.menu.count()):
                self.menu.item(i).setText("")
        else:
            self.title.setText("Academy")
            menu_texts = ["Students", "Teachers", "Settings"]
            for i in range(self.menu.count()):
                self.menu.item(i).setText(menu_texts[i])
