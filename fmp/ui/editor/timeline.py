# NOTE: deepseek generated, re-write following kdenlive later
# see https://github.com/KDE/kdenlive/blob/master/src/timeline2/view/qml/timeline.qml
from fmp.ui.common.qt import *


class Timeline(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 100)
        self.setMouseTracking(True)

        # Timeline properties
        self.timeline_start = 0
        self.timeline_end = 100
        self.current_position = 0
        self.scale = 1.0
        self.offset = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the timeline background
        painter.fillRect(self.rect(), QColor(50, 50, 50))

        # Calculate the visible range
        visible_start = self.timeline_start + self.offset
        visible_end = visible_start + (self.timeline_end - self.timeline_start) / self.scale

        # Draw the timeline ticks
        painter.setPen(Qt.white)
        for i in range(int(visible_start), int(visible_end) + 1):
            x = self.time_to_pixel(i)
            painter.drawLine(x, 0, x, self.height())

        # Draw the current position indicator
        painter.setPen(Qt.red)
        current_x = self.time_to_pixel(self.current_position)
        painter.drawLine(current_x, 0, current_x, self.height())

    def time_to_pixel(self, time):
        visible_start = self.timeline_start + self.offset
        return int((time - visible_start) * self.scale * self.width() / (self.timeline_end - self.timeline_start))

    def pixel_to_time(self, x):
        visible_start = self.timeline_start + self.offset
        return visible_start + (x / self.width()) * (self.timeline_end - self.timeline_start) / self.scale

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() & Qt.ControlModifier:
            # Ctrl + Wheel: Scale in/out
            delta = event.angleDelta().y()
            if delta > 0:
                self.scale *= 1.1
            else:
                self.scale /= 1.1
            self.scale = max(0.1, min(self.scale, 10.0))
            self.update()
        else:
            # Wheel: Scroll horizontally
            delta = event.angleDelta().y()
            self.offset -= delta / 120.0
            self.offset = max(0, min(self.offset, self.timeline_end - self.timeline_start))
            self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            # Click: Change current play position
            self.current_position = self.pixel_to_time(event.x())
            self.update()
