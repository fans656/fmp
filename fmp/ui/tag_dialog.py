from PySide6.QtWidgets import (
    QWidget, QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton,
    QGridLayout,
)
from PySide6.QtCore import Qt, Signal

from fmp.ui import util


class TagDialog(QDialog):

    def __init__(self, tag, tags):
        super().__init__()

        self.tag = tag
        self.tags = tags

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.tag_name_edit = Edit()
        self.tag_name_edit.quick_select.connect(self.on_quick_select)
        self.tag_name_edit.setText(tag.get('tag', ''))
        self.tag_name_edit.returnPressed.connect(self.update_tag)

        self.tag_selector = TagsSelector(tags)
        self.tag_selector.tag_selected.connect(self.on_tag_selected)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(util.humanized_time(tag['time_pos'])))
        layout.addWidget(self.tag_name_edit)
        layout.addWidget(self.tag_selector)

    def update_tag(self):
        self.tag['tag'] = self.tag_name_edit.text()
        self.close()

    def on_tag_selected(self, tag):
        self.toggle_tag(tag)

    def toggle_tag(self, tag):
        text = self.tag_name_edit.text()
        tags = set(text.split())
        if tag['tag'] in tags:
            tags.remove(tag['tag'])
        else:
            tags.add(tag['tag'])
        text = ' '.join(sorted(tags))
        self.tag_name_edit.setText(text)
        self.tag['tag'] = self.tag_name_edit.text()

    def on_quick_select(self, key: str):
        for tag in self.tags.template_tags:
            if tag.get('key') == key:
                self.toggle_tag(tag)
                break


class Edit(QLineEdit):

    quick_select = Signal(str)

    def __init__(self):
        super().__init__()

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.AltModifier:
            self.quick_select.emit(event.text().lower())
        else:
            return super().keyPressEvent(event)


class TagsSelector(QWidget):

    tag_selected = Signal(dict)

    def __init__(self, tags):
        super().__init__()

        self.tags = tags

        lt = QGridLayout(self)

        n_col = 5
        for i, tag in enumerate((d for d in self.tags.template_tags)):
            row = i // n_col
            col = i % n_col

            label = tag['tag']
            if tag.get('key'):
                label = f'{tag["key"]}: {label}'
            button = QPushButton(label)
            emit = lambda tag: (lambda: self.tag_selected.emit(tag))
            button.clicked.connect(emit(tag))
            lt.addWidget(button, row, col)
