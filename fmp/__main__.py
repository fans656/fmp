import sys
import argparse

from PySide6.QtWidgets import QApplication

from .ui import Player


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()

    app = QApplication(sys.argv)

    player = Player(
        files=args.files,
    )
    player.resize(800, 600)
    player.show()

    sys.exit(app.exec())
