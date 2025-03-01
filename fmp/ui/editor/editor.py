from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QRect, QEvent, Signal
from PySide6.QtGui import QShortcut
from fans.logger import get_logger
from fans.path import Path

from fmp.ui import cons
from fmp.ui import util

from .timeline import Timeline

logger = get_logger(__name__)


class Editor(QMainWindow):

    def __init__(
            self,
    ):
        super().__init__()

        self.setWindowTitle('fmp editor')

        self.setCentralWidget(CoreWidgets())


class CoreWidgets(QWidget):

    def __init__(self):
        super().__init__()

        self.timeline = Timeline()

        lt = QVBoxLayout(self)
        lt.setContentsMargins(0, 0, 0, 0)
        lt.addWidget(QLabel('main'))
        lt.addWidget(self.timeline)
