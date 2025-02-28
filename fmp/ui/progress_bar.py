from PySide6.QtWidgets import QWidget, QSlider, QPushButton, QLabel, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, QSize, QRect, Signal
from PySide6.QtGui import QIcon


class ProgressBar(QWidget):

    percent_seek_requested = Signal(float)

    def __init__(
            self,
            preview_percent,
    ):
        super().__init__()

        self.slider = Slider(preview_percent=preview_percent)
        self.slider.setFixedHeight(10)
        self.slider.setValue(0)
        self.slider.setRange(0, PROGRESS_RANGE)
        self.slider.sliderPressed.connect(self.on_slider_pressed)

        lt = QVBoxLayout(self)
        lt.addWidget(self.slider)

    def on_slider_pressed(self):
        percent = float(self.slider.value()) / PROGRESS_RANGE * 100.0
        self.percent_seek_requested.emit(percent)

    def set_ratio_pos(self, ratio):
        self.slider.setValue(ratio * PROGRESS_RANGE)


class Slider(QSlider):

    def __init__(self, *, preview_percent):
        super().__init__(Qt.Horizontal)

        self.preview_percent = preview_percent

        self.setMouseTracking(True)

        self.setStyleSheet('QSlider { margin: 0px; padding: 0px; }')

    def leaveEvent(self, event):
        self.preview_percent(None)

    def mouseMoveEvent(self, event):
        pos = event.pos().x()

        slider_range = self.maximum() - self.minimum()
        slider_width = self.width()
        value = self.minimum() + (pos / slider_width) * slider_range

        self.preview_percent(value / slider_range * 100.0)


PROGRESS_RANGE = 10000
