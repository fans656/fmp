from PySide6.QtCore import Qt, QRect


class Drawers:

    def __init__(self):
        self.drawers = []

    def add(
            self,
            widget,
            placement: str,
            hover_width: int = None,
            hover_height: int = None,
            width: int = None,
            height: int = None,
    ):
        widget.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        widget.hide()
        rect_func = rect_func_from_placement(placement, hover_width, hover_height, width, height)
        self.drawers.append(Drawer(widget, rect_func))

    def on_mouse_move(self, pos, parent_rect):
        for drawer in self.drawers:
            hover_rect, drawer_rect = drawer.rect(parent_rect)
            if hover_rect.contains(pos):
                drawer.widget.setGeometry(drawer_rect)
                #drawer.widget.raise_()
                drawer.widget.setVisible(True)
            elif not drawer_rect.contains(pos):
                drawer.widget.hide()


class Drawer:

    def __init__(self, widget, rect_func):
        self.widget = widget
        self.rect = rect_func


def rect_func_from_placement(placement, hover_width, hover_height, width, height):
    width = width or hover_width
    height = height or hover_height
    def func(parent_rect):
        match placement:
            case 'top':
                hover_rect = QRect(0, 0, parent_rect.width(), hover_height)
                drawer_rect = QRect(0, 0, parent_rect.width(), height)
            case 'bottom':
                hover_rect = QRect(
                    0, parent_rect.height() - hover_height,
                    parent_rect.width(), hover_height,
                )
                drawer_rect = QRect(
                    0, parent_rect.height() - height,
                    parent_rect.width(), height,
                )
            case _:
                raise ValueError(f'unsupported placement "{placement}"')
        return hover_rect, drawer_rect
    return func
