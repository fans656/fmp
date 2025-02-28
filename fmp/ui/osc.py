from PySide6.QtWidgets import (
    QWidget, QSlider, QPushButton, QLabel, QHBoxLayout, QVBoxLayout
)
from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QIcon

from fmp.ui import cons
from fmp.ui.util import humanized_time

from .renderer import Renderer
from .progress import Progress


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
        self.duration = None

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(10, 0, 10, 0)

        # Play progress slider
        self.progress = Progress(preview_percent=preview_percent)
        self.progress.percent_seek_requested.connect(self.seek_percent)
        main_layout.addWidget(self.progress)

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

    def set_sidecar(self, sidecar):
        with sidecar.tags as tags:
            self.progress.set_tags(tags)

    def set_duration(self, seconds: float):
        if seconds is not None:
            self.duration = seconds
            self.progress.set_duration(seconds)

    def set_time_pos(self, time_pos: float):
        if time_pos is not None:
            self.current_time_label.setText(humanized_time(time_pos))
            self.total_time_label.setText(humanized_time(self.duration))
            self.progress.set_time_pos(time_pos)

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
