from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QIcon

from fmp.ui import cons
from fmp.ui import util
from fmp.ui.common import IconButton


class TagsPanel(QWidget):

    tag_double_clicked = Signal(dict)  # Emits the tag data when double-clicked
    edit_tag_clicked = Signal(dict)
    delete_tag_clicked = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)
        self.setLayout(self.layout)

        self.list_widget.itemDoubleClicked.connect(self._on_item_double_clicked)

    def update(self, tags: list[dict]):
        self.list_widget.clear()
        for tag_data in tags:
            self._add_tag_item(tag_data)

    def _add_tag_item(self, tag_data):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.addWidget(QLabel(util.humanized_time(tag_data.get('time_pos', 0))))
        layout.addWidget(QLabel(tag_data.get('tag', '')))
        layout.addWidget(IconButton('edit', lambda: self.edit_tag_clicked.emit(tag_data)))
        layout.addWidget(IconButton('delete', lambda: self.delete_tag_clicked.emit(tag_data)))
        widget.setLayout(layout)

        item = QListWidgetItem()
        item.setData(Qt.UserRole, tag_data)
        item.setSizeHint(widget.sizeHint())

        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, widget)

    def _on_item_double_clicked(self, item):
        """Handle double-click events on list items."""
        tag_data = item.data(Qt.UserRole)  # Retrieve the stored tag_data
        self.tag_double_clicked.emit(tag_data)
