from PySide6.QtWidgets import QMainWindow, QLineEdit, QTextEdit, QApplication
from PySide6.QtCore import Qt, QRect, QEvent

from fmp.ui import cons
from fmp.ui import util

from .common.drawers import Drawers
from .renderer import Renderer
from .title_bar import TitleBar
from .osc import OSC
from .preview_thumb import PreviewThumb


class Player(QMainWindow):

    def __init__(
            self,
            files: list[str],
    ):
        super().__init__()

        self.video_path = files[0]  # TODO: support multiple files as playlist

        self.renderer = Renderer(self, show_log=True)
        self.title_bar = TitleBar(self)
        self.osc = self.setup_osc()
        self.drawers = self.setup_drawers()

        self.preview_thumb = self.setup_preview_thumb()

        self.setup_mpv()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setCentralWidget(self.renderer)

        # child widget might take focus, use event filter to handle global shortcuts
        QApplication.instance().installEventFilter(self)

    def setup_mpv(self):
        self.mpv = self.renderer.mpv
        self.mpv.observe_property('time-pos', self.update_progress)
        self.mpv.play(self.video_path)

    def setup_preview_thumb(self):
        return PreviewThumb(self.video_path, self)

    def setup_osc(self):
        return OSC(
            self,
            seek_percent=self.seek_percent,
            preview_percent=self.preview_percent,
        )

    def setup_drawers(self):
        drawers = Drawers()
        drawers.add(
            self.title_bar,
            'top',
            hover_height=cons.title_bar.height,
        )
        drawers.add(
            self.osc,
            'bottom',
            hover_height=cons.osc.hover_height,
            height=cons.osc.height,
        )
        return drawers

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            edges = util.calc_resize_edges(event.pos(), self.rect())
            if edges:
                self.windowHandle().startSystemResize(edges)
            else:
                self.windowHandle().startSystemMove()

    def mouseMoveEvent(self, event):
        self.update_cursor(event.pos())
        self.drawers.on_mouse_move(event.pos(), self.rect())

    def keyPressEvent(self, event):
        match event.key():
            case Qt.Key_Return | Qt.Key_Enter:
                self.toggle_fullscreen()
            case Qt.Key_Space:
                self.toggle_play()
            case Qt.Key_Left | Qt.Key_Right:
                self.seek(util.seek_time_from_modifiers(event))
            case Qt.Key_T:
                pos = self.mpv._get_property('time-pos/full')
                self.osd(f'Tagging {util.humanized_time(pos)}')
            case Qt.Key_E:
                print('edit tag')
            case _:
                super().keyPressEvent(event)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if isinstance(obj, (QLineEdit, QTextEdit)):
                return False
            else:
                self.keyPressEvent(event)
                return True
        return super().eventFilter(obj, event)

    def update_cursor(self, pos):
        if self.isFullScreen():
            self.setCursor(Qt.ArrowCursor)
        else:
            self.setCursor(util.cursor_from_edges(util.calc_resize_edges(pos, self.rect())))

    def update_progress(self, _, time):
        self.osc.update_progress(time, self.mpv.duration)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.renderer.set_fullscreen(False)
            self.showNormal()
        else:
            self.renderer.set_fullscreen(True)
            self.showFullScreen()

    def toggle_play(self):
        self.mpv.pause = not self.mpv.pause

    def seek(self, time):
        self.mpv.seek(time)

        now = self.mpv.time_pos
        self.osd(f'Seek {"+" if time > 0 else ""}{time}s ({util.humanized_time(now)})', 200)

    def seek_percent(self, percent):
        self.mpv.percent_pos = percent
        self.osd(f'Seek to {percent:.2f}%')

    def preview_percent(self, percent):
        if percent is None:
            self.preview_thumb.hide()
        else:
            self.preview_thumb.mpv.percent_pos = percent
            self.preview_thumb.move(*util.calc_preview_thumb_xy(self.rect(), percent))
            self.preview_thumb.show()

    def osd(self, message: str, duration: int = 1000):
        self.mpv.command('show-text', message, 3000)
