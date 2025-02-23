from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QIcon, QColor
from PySide6.QtCore import Qt, QSize

from fmp.ui import cons


class TitleBar(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #palette = self.palette()
        #palette.setColor(self.backgroundRole(), QColor('#eee'))
        #self.setPalette(palette)
        #self.setAutoFillBackground(True)

        close_button = QPushButton(self)
        close_button.setIcon(QIcon.fromTheme("window-close"))
        close_button.setIconSize(QSize(8, 8))
        close_button.setFixedSize(cons.title_bar.height, cons.title_bar.height)
        close_button.setStyleSheet("QPushButton { border: none; }")
        close_button.clicked.connect(self.on_close)

        close_button.clicked.connect(self.on_close)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(QLabel('fmp', self))
        layout.addWidget(close_button)

        self.setLayout(layout)

    def on_close(self):
        self.window().close()
