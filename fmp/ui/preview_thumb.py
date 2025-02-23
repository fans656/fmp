from PySide6.QtCore import Qt

from fmp.ui.renderer import Renderer
from fmp.ui import cons


class PreviewThumb(Renderer):

    def __init__(self, file: str, parent):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.resize(cons.preview_thumb.width, cons.preview_thumb.height)
        self.hide()

        self.mpv.play(file)
        self.mpv.pause = True
