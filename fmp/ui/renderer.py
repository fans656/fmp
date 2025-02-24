import os
from pathlib import Path

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

os.environ['PATH'] = f"{os.environ['PATH']}{os.pathsep}{str(Path('./lib'))}"; import mpv


class Renderer(QWidget):

    def __init__(
            self,
            parent,
            show_log: bool = False,
            mpv_kwargs: dict = {},
    ):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.setAttribute(Qt.WA_NativeWindow)
        self.setMouseTracking(True)

        self.mpv = mpv.MPV(
            wid=str(int(self.winId())),
            vo='gpu',
            log_handler=self.mpv_log_handler if show_log else None,
        )

    def mouseMoveEvent(self, event):
        self.parent().mouseMoveEvent(event)

    def set_fullscreen(self, fullscreen: bool):
        if fullscreen:
            self.normal_geometry = self.geometry()
            self.mpv.fullscreen = True
            self.setGeometry(self.screen().geometry())
        else:
            self.mpv.fullscreen = False
            self.setGeometry(self.normal_geometry)

    def mpv_log_handler(self, log_level, log_type, log_message):
        print(f'[mpv][{log_level}][{log_type}] {log_message.strip()}')
