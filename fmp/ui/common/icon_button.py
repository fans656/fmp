from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QSize
import qtawesome


class IconButton(QPushButton):

    def __init__(self, icon: str, clicked = None, size: int = 16):
        super().__init__()
        self.setIcon(qtawesome.icon(aliases.get(icon, icon)))
        self.setIconSize(QSize(size, size))
        self.setFixedSize(self.iconSize())
        if clicked:
            self.clicked.connect(clicked)


aliases = {
    'delete': 'ri.delete-bin-7-line',
    'edit': 'ri.edit-line',
}
