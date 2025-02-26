from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon

from fmp.ui import cons
from fmp.ui import util


class TagsPanel(QWidget):

    tag_double_clicked = Signal(dict)  # Emits the tag data when double-clicked
    edit_tag_clicked = Signal(dict)
    delete_tag_clicked = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)
        self.setLayout(self.layout)

        self.list_widget.itemDoubleClicked.connect(self._on_item_double_clicked)

    def update(self, tags):
        """Update the list of tags displayed in the panel."""
        self.list_widget.clear()
        for tag_data in tags:
            self._add_tag_item(tag_data)

    def _add_tag_item(self, tag_data):
        """Add a single tag item to the list widget."""
        item = QListWidgetItem()
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # Time position label
        time_pos = tag_data.get('time_pos', 0)
        time_label = QLabel(util.humanized_time(time_pos))
        layout.addWidget(time_label)

        # Tag name label
        tag_name = tag_data.get('tag', '')
        tag_label = QLabel(tag_name)
        layout.addWidget(tag_label)

        # Edit icon button
        edit_button = QPushButton('E')
        edit_button.clicked.connect(lambda: self.edit_tag_clicked.emit(tag_data))
        layout.addWidget(edit_button)

        delete_button = QPushButton('D')
        delete_button.clicked.connect(lambda: self.delete_tag_clicked.emit(tag_data))
        layout.addWidget(delete_button)

        widget.setLayout(layout)
        item.setSizeHint(widget.sizeHint())
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, widget)

        item.setData(Qt.UserRole, tag_data)

    def _on_item_double_clicked(self, item):
        """Handle double-click events on list items."""
        tag_data = item.data(Qt.UserRole)  # Retrieve the stored tag_data
        self.tag_double_clicked.emit(tag_data)
