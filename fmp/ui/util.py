from PySide6.QtCore import Qt, QTimer

from fmp.ui import cons


def dispatch(func):
    QTimer.singleShot(0, func)
    print('hi')


def cursor_from_edges(edge):
    if edge == (Qt.TopEdge | Qt.LeftEdge):
        return Qt.SizeFDiagCursor
    elif edge == (Qt.TopEdge | Qt.RightEdge):
        return Qt.SizeBDiagCursor
    elif edge == (Qt.BottomEdge | Qt.LeftEdge):
        return Qt.SizeBDiagCursor
    elif edge == (Qt.BottomEdge | Qt.RightEdge):
        return Qt.SizeFDiagCursor
    elif edge & Qt.LeftEdge or edge & Qt.RightEdge:
        return Qt.SizeHorCursor
    elif edge & Qt.TopEdge or edge & Qt.BottomEdge:
        return Qt.SizeVerCursor
    else:
        return Qt.ArrowCursor


def calc_resize_edges(pos, rect):
    ret = Qt.Edges()

    if pos.y() <= cons.resize_margin:
        ret |= Qt.TopEdge
    elif pos.y() >= rect.height() - cons.resize_margin:
        ret |= Qt.BottomEdge

    if pos.x() <= cons.resize_margin:
        ret |= Qt.LeftEdge
    elif pos.x() >= rect.width() - cons.resize_margin:
        ret |= Qt.RightEdge

    return ret


def seek_time_from_modifiers(event):
    modifiers = event.modifiers()
    time = 5
    if modifiers == Qt.ControlModifier:
        time = 30
    elif modifiers == Qt.ShiftModifier:
        time = 60
    return time if event.key() == Qt.Key_Right else -time


def humanized_time(seconds):
    seconds = int(seconds)
    hours = 0
    minutes = 0
    if seconds >= 60:
        minutes = seconds // 60
        seconds %= 60
    if minutes >= 60:
        hours = minutes // 60
        minutes %= 60
    return f'{hours}:{minutes:02}:{seconds:02}'


def calc_preview_thumb_xy(rect, percent):
    x_max = rect.width() - cons.preview_thumb.width
    x = x_max * percent / 100.0
    y = rect.height() - cons.preview_thumb.height - cons.osc.height
    return x, y
