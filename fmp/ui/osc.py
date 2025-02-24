from PySide6.QtWidgets import (
    QWidget, QSlider, QPushButton, QLabel, QHBoxLayout, QVBoxLayout
)
from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QIcon

from fmp.ui import cons
from fmp.ui.util import humanized_time

from .renderer import Renderer


class ProgressBar(QSlider):

    def __init__(self, *args, preview_percent=None, **kwargs):
        super().__init__(*args, **kwargs)

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


class OSC(QWidget):

    def __init__(
            self,
            *args,
            seek_percent=None,
            preview_percent=None,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.seek_percent = seek_percent

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(10, 0, 10, 0)

        # Play progress slider
        self.progress_slider = ProgressBar(Qt.Horizontal, preview_percent=preview_percent)
        self.progress_slider.setRange(0, progress_range)
        self.progress_slider.setValue(0)
        self.progress_slider.setFixedHeight(10)
        self.progress_slider.sliderPressed.connect(self.on_progress_slider_press)
        main_layout.addWidget(self.progress_slider)

        # Control buttons and time display
        control_layout = QHBoxLayout()
        control_layout.setSpacing(0)

        # Play/Pause button
        self.play_pause_button = QPushButton()
        self.play_pause_button.setIcon(QIcon.fromTheme("media-playback-start"))
        self.play_pause_button.setIconSize(QSize(cons.icon_size, cons.icon_size))
        self.play_pause_button.setFixedSize(cons.button_size, cons.button_size)
        self.play_pause_button.setStyleSheet("QPushButton { border: none; }")
        control_layout.addWidget(self.play_pause_button)

        # Current time label
        self.current_time_label = QLabel("00:00")
        control_layout.addWidget(self.current_time_label)

        control_layout.addWidget(QLabel("/"))

        # Total time label
        self.total_time_label = QLabel("00:00")
        control_layout.addWidget(self.total_time_label)

        # Spacer
        control_layout.addStretch()

        # Mute button
        self.mute_button = QPushButton()
        self.mute_button.setIcon(QIcon.fromTheme("audio-volume-high"))
        self.mute_button.setIconSize(QSize(cons.icon_size, cons.icon_size))
        self.mute_button.setFixedSize(cons.button_size, cons.button_size)
        self.mute_button.setStyleSheet("QPushButton { border: none; }")
        control_layout.addWidget(self.mute_button)

        # Volume control slider
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setFixedWidth(100)
        control_layout.addWidget(self.volume_slider)

        # Add control layout to main layout
        main_layout.addLayout(control_layout)

        # Set the main layout to the widget
        self.setLayout(main_layout)

    def update_progress(self, current_time, total_time):
        if current_time is None or total_time is None:
            return
        self.current_time_label.setText(humanized_time(current_time))
        self.total_time_label.setText(humanized_time(total_time))
        self.progress_slider.setValue(current_time / total_time * progress_range)

    def toggle_play_pause(self, is_playing):
        if is_playing:
            self.play_pause_button.setIcon(QIcon.fromTheme("media-playback-pause"))
        else:
            self.play_pause_button.setIcon(QIcon.fromTheme("media-playback-start"))

    def toggle_mute(self, is_muted):
        if is_muted:
            self.mute_button.setIcon(QIcon.fromTheme("audio-volume-muted"))
        else:
            self.mute_button.setIcon(QIcon.fromTheme("audio-volume-high"))

    def on_progress_slider_press(self):
        self.seek_percent(float(self.progress_slider.value()) / progress_range * 100.0)


progress_range = 10000
