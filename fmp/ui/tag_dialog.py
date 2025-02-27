from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit
from PySide6.QtCore import Qt


class TagDialog(QDialog):

    def __init__(self, tag):
        super().__init__()

        self.tag = tag

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.tag_name_edit = QLineEdit()
        self.tag_name_edit.setText(tag.get('tag', ''))
        self.tag_name_edit.returnPressed.connect(self.update_tag)

        layout = QVBoxLayout(self)
        layout.addWidget(self.tag_name_edit)

    def update_tag(self):
        self.tag['tag'] = self.tag_name_edit.text()
        self.close()
