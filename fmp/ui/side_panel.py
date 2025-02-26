from PySide6.QtWidgets import QWidget, QVBoxLayout

from fmp.ui import cons


class SidePanel(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.panels = []

    def add_panel(self, panel):
        self.panels.append(panel)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(panel)
        self.setLayout(layout)
