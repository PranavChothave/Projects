from pathlib import Path

from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QMovie
from PySide6.QtCore import Qt


class CharacterWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        gif_path = Path(__file__).parent.parent / "assets" / "water_drink.gif"

        self.movie = QMovie(str(gif_path))

        print("GIF Loaded:", self.movie.isValid())

        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.start()

        self.label.setMovie(self.movie)

        self.movie.frameChanged.connect(self.update_size)

    def update_size(self):
        size = self.movie.currentPixmap().size()

        self.label.resize(size)
        self.resize(size)