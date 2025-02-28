from PySide6.QtWidgets import QWidget, QSlider, QPushButton, QLabel, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, QSize, QRect, Signal
from PySide6.QtGui import QIcon, QPainter, QFont, QFontMetrics, QTextOption


class Progress(QWidget):

    percent_seek_requested = Signal(float)

    def __init__(
            self,
            preview_percent,
    ):
        super().__init__()

        self.duration = None

        self.slider = Slider(preview_percent=preview_percent)
        self.slider.setFixedHeight(10)
        self.slider.setValue(0)
        self.slider.setRange(0, PROGRESS_RANGE)
        self.slider.sliderPressed.connect(self.on_slider_pressed)

        self.indicator = Indicator(self.slider, progress=self)

        lt = QVBoxLayout(self)
        lt.setSpacing(0)
        lt.addWidget(self.indicator)
        lt.addWidget(self.slider)

    def set_duration(self, duration):
        self.duration = duration

    def set_tags(self, tags):
        self.indicator.tags = tags or {'tags': []}

    def on_slider_pressed(self):
        percent = float(self.slider.value()) / PROGRESS_RANGE * 100.0
        self.percent_seek_requested.emit(percent)

    def set_time_pos(self, time_pos):
        if self.duration is not None:
            self.set_ratio_pos(time_pos / self.duration)

    def set_ratio_pos(self, ratio):
        self.slider.setValue(ratio * PROGRESS_RANGE)


class Indicator(QWidget):

    def __init__(self, slider, progress):
        super().__init__()

        self.slider = slider
        self.progress = progress

        self.tags = []

    def paintEvent(self, event):
        super().paintEvent(event)

        if not self.tags:
            return

        duration = self.progress.duration
        if duration is None:
            return

        slider_width = self.slider.width()

        painter = QPainter(self)
        painter.setPen(Qt.black)

        font = QFont()
        font.setPixelSize(9)
        painter.setFont(font)

        fm = QFontMetrics(font)

        last_tag_ending_x = 0
        for tag in self.tags.sorted_tags:
            ratio = tag['time_pos'] / duration
            x = ratio * slider_width
            painter.drawLine(x, 0, x, self.height())

            text = tag.get('tag')
            if text:
                if x >= last_tag_ending_x:
                    width = 20
                    text_rect = QRect(x, 0, width, 12)
                    painter.drawText(text_rect, text)
                    last_tag_ending_x = x + width


class Slider(QSlider):

    def __init__(self, *, preview_percent):
        super().__init__(Qt.Horizontal)

        self.preview_percent = preview_percent

        self.setMouseTracking(True)

        self.setStyleSheet('''
            QSlider::groove:horizontal {
                background: #ddd;
                height: 4px;
                margin: 0px;
                padding: 0px;
            }

            QSlider::handle:horizontal {
                background: #555;
                width: 1px;
                height: 16px;
            }

            QSlider::sub-page:horizontal {
                background: #555;
            }
                           ''')

    def leaveEvent(self, event):
        self.preview_percent(None)

    def mouseMoveEvent(self, event):
        pos = event.pos().x()

        slider_range = self.maximum() - self.minimum()
        slider_width = self.width()
        value = max(0, self.minimum() + (pos / slider_width) * slider_range)

        self.preview_percent(value / slider_range * 100.0)


PROGRESS_RANGE = 10000
