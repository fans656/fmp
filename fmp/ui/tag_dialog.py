from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit
from PySide6.QtCore import Qt


class TagDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowFlags(Qt.FramelessWindowHint)

        layout = QVBoxLayout(self)
        layout.addWidget(QLineEdit())
