from PyQt6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget, QGraphicsOpacityEffect
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QRect

from app.widgets.sidebar import Sidebar
from app.widgets.theme import apply_theme
from app.pages.students_page import StudentsPage
from app.pages.teachers_page import TeachersPage
from app.pages.settings_page import SettingsPage

from config.user_settings import load_settings


class MainWindow(QWidget):
    def __init__(self, current_user):
        super().__init__()

        self.current_user = current_user
        self.setWindowTitle("Academy 33-1B")
        self.resize(1200, 700)

        settings = load_settings()
        self.animation_mode = settings.get("animation", "slide_fade")

        apply_theme(settings.get("theme", "dark"))

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.sidebar = Sidebar(current_user)
        root.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        root.addWidget(self.stack, 1)

        self.students_page = StudentsPage(current_user)
        self.teachers_page = TeachersPage(current_user)
        self.settings_page = SettingsPage(current_user, main_window=self)

        self.stack.addWidget(self.students_page)
        self.stack.addWidget(self.teachers_page)
        self.stack.addWidget(self.settings_page)

        self.stack.setCurrentIndex(0)

        self.sidebar.page_changed.connect(self.change_page)

        self._anim_in = None
        self._anim_out = None

    def change_page(self, new_index: int):
        old_index = self.stack.currentIndex()
        if new_index == old_index:
            return

        if new_index < 0 or new_index >= self.stack.count():
            return

        if self.animation_mode == "fade":
            self._fade_transition(new_index)
        elif self.animation_mode == "slide":
            self._slide_transition(new_index)
        elif self.animation_mode == "slide_fade":
            self._slide_fade_transition(new_index)
        elif self.animation_mode == "flip":
            self._flip_transition(new_index)
        else:
            self.stack.setCurrentIndex(new_index)

    def _fade_transition(self, new_index):
        old = self.stack.currentWidget()
        new = self.stack.widget(new_index)

        eff_old = QGraphicsOpacityEffect()
        old.setGraphicsEffect(eff_old)

        eff_new = QGraphicsOpacityEffect()
        new.setGraphicsEffect(eff_new)
        eff_new.setOpacity(0)
        new.setVisible(True)

        anim_old = QPropertyAnimation(eff_old, b"opacity")
        anim_old.setDuration(200)
        anim_old.setStartValue(1)
        anim_old.setEndValue(0)

        anim_new = QPropertyAnimation(eff_new, b"opacity")
        anim_new.setDuration(200)
        anim_new.setStartValue(0)
        anim_new.setEndValue(1)

        def finish():
            self.stack.setCurrentIndex(new_index)
            old.setGraphicsEffect(None)
            new.setGraphicsEffect(None)

        anim_new.finished.connect(finish)

        anim_old.start()
        anim_new.start()

        self._anim_out = anim_old
        self._anim_in = anim_new

    def _slide_transition(self, new_index):
        old = self.stack.currentWidget()
        new = self.stack.widget(new_index)
        new.setVisible(True)

        w = self.stack.width()
        h = self.stack.height()

        new.setGeometry(w, 0, w, h)

        anim_old = QPropertyAnimation(old, b"geometry")
        anim_old.setDuration(250)
        anim_old.setStartValue(QRect(0, 0, w, h))
        anim_old.setEndValue(QRect(-w, 0, w, h))
        anim_old.setEasingCurve(QEasingCurve.Type.InOutCubic)

        anim_new = QPropertyAnimation(new, b"geometry")
        anim_new.setDuration(250)
        anim_new.setStartValue(QRect(w, 0, w, h))
        anim_new.setEndValue(QRect(0, 0, w, h))
        anim_new.setEasingCurve(QEasingCurve.Type.InOutCubic)

        def finish():
            self.stack.setCurrentIndex(new_index)
            new.setGeometry(0, 0, w, h)
            old.setGeometry(0, 0, w, h)

        anim_new.finished.connect(finish)

        anim_old.start()
        anim_new.start()

        self._anim_out = anim_old
        self._anim_in = anim_new

    def _slide_fade_transition(self, new_index):
        old = self.stack.currentWidget()
        new = self.stack.widget(new_index)
        new.setVisible(True)

        w = self.stack.width()
        h = self.stack.height()

        eff_old = QGraphicsOpacityEffect()
        eff_new = QGraphicsOpacityEffect()

        old.setGraphicsEffect(eff_old)
        new.setGraphicsEffect(eff_new)

        eff_old.setOpacity(1)
        eff_new.setOpacity(0)

        new.setGeometry(w // 2, 0, w, h)

        anim_old_pos = QPropertyAnimation(old, b"geometry")
        anim_old_pos.setDuration(250)
        anim_old_pos.setStartValue(QRect(0, 0, w, h))
        anim_old_pos.setEndValue(QRect(-w // 2, 0, w, h))
        anim_old_pos.setEasingCurve(QEasingCurve.Type.InOutCubic)

        anim_new_pos = QPropertyAnimation(new, b"geometry")
        anim_new_pos.setDuration(250)
        anim_new_pos.setStartValue(QRect(w // 2, 0, w, h))
        anim_new_pos.setEndValue(QRect(0, 0, w, h))
        anim_new_pos.setEasingCurve(QEasingCurve.Type.InOutCubic)

        anim_old_op = QPropertyAnimation(eff_old, b"opacity")
        anim_old_op.setDuration(250)
        anim_old_op.setStartValue(1)
        anim_old_op.setEndValue(0)

        anim_new_op = QPropertyAnimation(eff_new, b"opacity")
        anim_new_op.setDuration(250)
        anim_new_op.setStartValue(0)
        anim_new_op.setEndValue(1)

        def finish():
            self.stack.setCurrentIndex(new_index)
            new.setGeometry(0, 0, w, h)
            old.setGeometry(0, 0, w, h)
            old.setGraphicsEffect(None)
            new.setGraphicsEffect(None)

        anim_new_op.finished.connect(finish)

        for a in (anim_old_pos, anim_old_op, anim_new_pos, anim_new_op):
            a.start()

        self._anim_out = (anim_old_pos, anim_old_op)
        self._anim_in = (anim_new_pos, anim_new_op)

    def _flip_transition(self, new_index):
        old = self.stack.currentWidget()
        new = self.stack.widget(new_index)
        new.setVisible(True)

        w = self.stack.width()
        h = self.stack.height()

        anim_old = QPropertyAnimation(old, b"geometry")
        anim_old.setDuration(200)
        anim_old.setStartValue(QRect(0, 0, w, h))
        anim_old.setEndValue(QRect(w // 2, 0, 0, h))
        anim_old.setEasingCurve(QEasingCurve.Type.InOutCubic)

        def halfway():
            self.stack.setCurrentIndex(new_index)
            new.setGeometry(QRect(w // 2, 0, 0, h))

            anim_new = QPropertyAnimation(new, b"geometry")
            anim_new.setDuration(200)
            anim_new.setStartValue(QRect(w // 2, 0, 0, h))
            anim_new.setEndValue(QRect(0, 0, w, h))
            anim_new.setEasingCurve(QEasingCurve.Type.InOutCubic)
            anim_new.start()

            self._anim_in = anim_new

        anim_old.finished.connect(halfway)
        anim_old.start()

        self._anim_out = anim_old
