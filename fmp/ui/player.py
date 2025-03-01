from PySide6.QtWidgets import QMainWindow, QLineEdit, QTextEdit, QApplication, QDialog
from PySide6.QtCore import Qt, QRect, QEvent, Signal
from PySide6.QtGui import QShortcut
from fans.logger import get_logger
from fans.path import Path

from fmp.ui import cons
from fmp.ui import util
from fmp.data import Sidecar

from .common.drawers import Drawers
from .renderer import Renderer
from .title_bar import TitleBar
from .osc import OSC
from .preview_thumb import PreviewThumb
from .tag_dialog import TagDialog
from .side_panel import SidePanel
from .tags_panel import TagsPanel


logger = get_logger(__name__)


class Player(QMainWindow):

    on_property_path = Signal(str, str)

    def __init__(
            self,
            files: list[str],
            config_path: str,
    ):
        super().__init__()

        self.video_path = files[0]  # TODO: support multiple files as playlist
        self.conf = Path(config_path or 'conf.yaml').as_meta()

        self.on_property_path.connect(self.on_property_path_slot)

        self.renderer = Renderer(self, show_log=True)
        self.title_bar = TitleBar(self)
        self.osc = self.setup_osc()
        self.left_side_panel = self.setup_left_side_panel()
        self.right_side_panel = self.setup_right_side_panel()
        self.drawers = self.setup_drawers()

        self.preview_thumb = self.setup_preview_thumb()

        self.setup_mpv()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setCentralWidget(self.renderer)

        self.setup_shortcuts()

        # child widget might take focus, use event filter to handle global shortcuts
        QApplication.instance().installEventFilter(self)

        self.mpv.play(self.video_path)

    def setup_mpv(self):
        self.mpv = self.renderer.mpv
        self.mpv.observe_property('path', self.on_property_path.emit)
        self.mpv.observe_property('duration', self.on_property_duration)
        self.mpv.observe_property('time-pos', self.on_property_time_pos)

    def setup_preview_thumb(self):
        return PreviewThumb(self.video_path, self)

    def setup_osc(self):
        return OSC(
            self,
            seek_percent=self.seek_percent,
            seek_time=self.seek_time,
            preview_percent=self.preview_percent,
        )

    def setup_left_side_panel(self):
        panel = SidePanel(
            self,
        )

        self.tags_panel = TagsPanel(panel)
        self.tags_panel.tag_double_clicked.connect(self.seek_tag)
        self.tags_panel.edit_tag_clicked.connect(self.edit_tag)
        self.tags_panel.delete_tag_clicked.connect(self.delete_tag)

        panel.add_panel(self.tags_panel)
        return panel

    def seek_tag(self, tag):
        self.mpv.time_pos = tag['time_pos']

    def delete_tag(self, tag):
        with self.sidecar.tags as tags:
            tags.delete(tag)
        self.update_tags_panel()

    def edit_tag(self, tag: dict = None):
        if not tag:
            with self.sidecar.tags as tags:
                tag = tags.find_nearest_tag(self.mpv.time_pos)
        if tag:
            with self.sidecar.tags as tags:
                TagDialog(tag, tags).exec()
                tags.update(tag)
            self.update_tags_panel()
        else:
            self.osd('No tag near current position')

    def update_tags_panel(self):
        with self.sidecar.tags as tags:
            self.tags_panel.update(tags.sorted_tags)

    def goto_prev_tag(self):
        with self.sidecar.tags as tags:
            tag = tags.find_prev_tag(self.mpv.time_pos)
        if tag:
            self.seek_tag(tag)

    def goto_next_tag(self):
        with self.sidecar.tags as tags:
            tag = tags.find_next_tag(self.mpv.time_pos)
        if tag:
            self.seek_tag(tag)

    def setup_right_side_panel(self):
        return SidePanel(
            self,
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
        drawers.add(
            self.left_side_panel,
            'left',
            hover_width=cons.side_panel.hover_width,
            width=cons.side_panel.width,
        )
        drawers.add(
            self.right_side_panel,
            'right',
            hover_width=cons.side_panel.hover_width,
            width=cons.side_panel.width,
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

    def setup_shortcuts(self):
        self.shortcuts = []
        for key, func in [
                (Qt.Key_Return, self.toggle_fullscreen),
                (Qt.Key_Space, self.toggle_play),

                (Qt.Key_Left, lambda: self.seek(-5)),
                (CtrlLeft, lambda: self.seek(-30)),
                (ShiftLeft, lambda: self.seek(-60)),
                (Qt.Key_Right, lambda: self.seek(5)),
                (CtrlRight, lambda: self.seek(30)),
                (ShiftRight, lambda: self.seek(60)),

                (Qt.Key_T, self.tag),
                (Qt.Key_E, self.edit_tag),

                (Qt.Key_F, lambda: self.mpv.command('frame-step')),
                (Qt.Key_D, lambda: self.mpv.command('frame-back-step')),

                (Qt.Key_B, self.goto_prev_tag),
                (Qt.Key_W, self.goto_next_tag),
        ]:
            shortcut = QShortcut(key, self)
            shortcut.activated.connect(func)
            self.shortcuts.append(shortcut)

    def enable_shortcuts(self, enabled: bool = True):
        for shortcut in self.shortcuts:
            shortcut.setEnabled(enabled)

    def eventFilter(self, obj, event):
        if event.type() == event.Type.FocusIn:
            if isinstance(obj, (QLineEdit, QTextEdit, QDialog)):
                self.enable_shortcuts(False)
        elif event.type() == event.Type.FocusOut:
            if isinstance(obj, (QLineEdit, QTextEdit, QDialog)):
                self.enable_shortcuts(True)
        return super().eventFilter(obj, event)

    def update_cursor(self, pos):
        if self.isFullScreen():
            self.setCursor(Qt.ArrowCursor)
        else:
            self.setCursor(util.cursor_from_edges(util.calc_resize_edges(pos, self.rect())))

    def on_property_path_slot(self, _, path):
        self.sidecar = Sidecar(path, self.conf)
        self.osc.set_sidecar(self.sidecar)
        self.update_tags_panel()

    def on_property_time_pos(self, _, time_pos):
        self.osc.set_time_pos(time_pos)

    def on_property_duration(self, _, duration):
        self.osc.set_duration(duration)

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

    def seek_time(self, time):
        self.mpv.time_pos = time
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
        logger.info(f'[OSD] {message}')

    def tag(self):
        time_pos = self.mpv._get_property('time-pos/full')
        self.osd(f'Tagging {util.humanized_time(time_pos)}')

        with self.sidecar.tags as tags:
            tags.add({'time_pos': time_pos})
        self.update_tags_panel()


CtrlLeft = Qt.Key_Left | Qt.ControlModifier
ShiftLeft = Qt.Key_Left | Qt.ShiftModifier
CtrlRight = Qt.Key_Right | Qt.ControlModifier
ShiftRight = Qt.Key_Right | Qt.ShiftModifier
