import os
import sys
import argparse

from PySide6.QtWidgets import QApplication

from .ui import Player


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Configuration file to use')
    parser.add_argument('--width', type=int, default=800, help='Window width')
    parser.add_argument('--height', type=int, default=600, help='Window height')
    parser.add_argument('--x', type=int, default=None, help='Window x position')
    parser.add_argument('--y', type=int, default=None, help='Window y position')
    parser.add_argument('file', nargs='+', help='File(s) to play')
    args = parser.parse_args()

    if args.file[0] == 'script' and len(args.file) > 1:
        script = args.file[1]
        os.system(f'uv run -m fmp.scripts.{script}')
        exit()

    app = QApplication(sys.argv)

    desktop_rect = app.primaryScreen().availableGeometry()

    width = args.width
    height = args.height

    x = args.x
    if x is None:
        x = desktop_rect.left() + (desktop_rect.width() - width) // 2
    y = args.y
    if y is None:
        y = desktop_rect.top() + (desktop_rect.height() - height) // 2

    player = Player(
        files=args.file,
        config_path=args.config,
    )
    player.resize(width, height)
    player.move(x, y)
    player.show()

    sys.exit(app.exec())
