from pathlib import Path

from PySide6.QtCore import (
    Qt,
    QSize,
    Signal,
    QPropertyAnimation,
    QEasingCurve,
    QPoint,
    QTimer,
)

from PySide6.QtGui import (
    QMovie,
    QGuiApplication,
)

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect,
)


class ReminderPopup(QWidget):

    drank = Signal()
    snooze = Signal()
    closed = Signal()

    def __init__(self):
        super().__init__()

        ##################################################
        # Window
        ##################################################

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setFixedSize(390, 360)

        ##################################################
        # Root Layout
        ##################################################

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)

        ##################################################
        # Main Card
        ##################################################

        self.card = QFrame()

        self.card.setObjectName("card")

        self.card.setStyleSheet("""
        QFrame#card{
            background:white;
            border-radius:22px;
            border:1px solid #DDEEFF;
        }
        """)

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(35)
        shadow.setOffset(0, 8)

        self.card.setGraphicsEffect(shadow)

        root.addWidget(self.card)

        ##################################################

        layout = QVBoxLayout(self.card)

        layout.setContentsMargins(25, 20, 25, 20)

        layout.setSpacing(15)

        ##################################################
        # Title
        ##################################################

        self.title = QLabel("💧 Water Reminder")

        self.title.setAlignment(Qt.AlignCenter)

        self.title.setStyleSheet("""
        QLabel{
            font-size:20px;
            font-weight:700;
            color:#1E88E5;
            border:none;
        }
        """)

        layout.addWidget(self.title)

        ##################################################
        # Character
        ##################################################

        self.character = QLabel()

        self.character.setAlignment(Qt.AlignCenter)

        gif_path = (
            Path(__file__).parent.parent
            / "assets"
            / "water_drink.gif"
        )

        self.movie = QMovie(str(gif_path))

        self.movie.setCacheMode(QMovie.CacheAll)

        self.movie.setScaledSize(QSize(180, 180))

        self.character.setFixedSize(180, 180)

        self.character.setMovie(self.movie)

        self.movie.start()

        layout.addWidget(
            self.character,
            alignment=Qt.AlignCenter
        )

        ##################################################
        # Bubble
        ##################################################

        self.bubble = QLabel(
            "💧\nTime to drink some water!"
        )

        self.bubble.setWordWrap(True)

        self.bubble.setAlignment(Qt.AlignCenter)

        self.bubble.setStyleSheet("""
        QLabel{
            background:#F5FBFF;
            border:2px solid #90CAF9;
            border-radius:16px;
            padding:14px;
            font-size:15px;
            color:#333333;
        }
        """)

        self.bubble_effect = QGraphicsOpacityEffect()

        self.bubble.setGraphicsEffect(
            self.bubble_effect
        )

        self.bubble_effect.setOpacity(1)

        layout.addWidget(self.bubble)

        ##################################################
        # Button Row
        ##################################################

        self.button_row = QHBoxLayout()

        self.button_row.setSpacing(10)

        self.drink_btn = QPushButton("✓ I Drank")

        self.snooze_btn = QPushButton("😴 Snooze")

        self.close_btn = QPushButton("✕")

        self.close_btn.setFixedWidth(45)

        ##################################################
        # Buttons Styling
        ##################################################

        self.drink_btn.setCursor(Qt.PointingHandCursor)
        self.snooze_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.setCursor(Qt.PointingHandCursor)

        self.drink_btn.setStyleSheet("""
        QPushButton{
            background:#4CAF50;
            color:white;
            border:none;
            border-radius:10px;
            padding:10px 14px;
            font-size:13px;
            font-weight:600;
        }

        QPushButton:hover{
            background:#43A047;
        }
        """)

        self.snooze_btn.setStyleSheet("""
        QPushButton{
            background:#FF9800;
            color:white;
            border:none;
            border-radius:10px;
            padding:10px 14px;
            font-size:13px;
            font-weight:600;
        }

        QPushButton:hover{
            background:#FB8C00;
        }
        """)

        self.close_btn.setStyleSheet("""
        QPushButton{
            background:#BDBDBD;
            color:white;
            border:none;
            border-radius:10px;
            font-size:16px;
            font-weight:bold;
        }

        QPushButton:hover{
            background:#9E9E9E;
        }
        """)

        self.button_row.addWidget(self.drink_btn)
        self.button_row.addWidget(self.snooze_btn)
        self.button_row.addWidget(self.close_btn)

        layout.addLayout(self.button_row)

        ##################################################
        # Signals
        ##################################################

        self.drink_btn.clicked.connect(self.drank.emit)
        self.snooze_btn.clicked.connect(self.snooze.emit)
        self.close_btn.clicked.connect(self.closed.emit)

        ##################################################
        # Popup opacity (used later)
        ##################################################

        self.popup_effect = QGraphicsOpacityEffect(self)

        self.popup_effect.setOpacity(1)

        self.setGraphicsEffect(self.popup_effect)

        ##################################################

        self.move_bottom_right()

    ########################################################
    # Position
    ########################################################

    def move_bottom_right(self):

        screen = QGuiApplication.primaryScreen().availableGeometry()

        margin = 20

        x = screen.right() - self.width() - margin

        y = screen.bottom() - self.height() - margin

        self.move(x, y)

    ########################################################
    # Show popup
    ########################################################

    def show_popup(self):

        self.move_bottom_right()

        self.show()

        self.raise_()

        self.activateWindow()

    ########################################################
    # Hide popup
    ########################################################

    def hide_popup(self):

        self.hide()

    ########################################################
    # Slide In
    ########################################################

    def slide_in(self):

        end_pos = self.pos()

        start_pos = QPoint(end_pos.x() + 250, end_pos.y())

        self.move(start_pos)

        self.slide_anim = QPropertyAnimation(self, b"pos")

        self.slide_anim.setDuration(500)

        self.slide_anim.setStartValue(start_pos)

        self.slide_anim.setEndValue(end_pos)

        self.slide_anim.setEasingCurve(QEasingCurve.OutCubic)

        self.slide_anim.start()

    ########################################################
    # Slide Out
    ########################################################

    def slide_out(self):

        start_pos = self.pos()

        end_pos = QPoint(start_pos.x() + 250, start_pos.y())

        self.slide_anim = QPropertyAnimation(self, b"pos")

        self.slide_anim.setDuration(350)

        self.slide_anim.setStartValue(start_pos)

        self.slide_anim.setEndValue(end_pos)

        self.slide_anim.setEasingCurve(QEasingCurve.InCubic)

        self.slide_anim.finished.connect(self.hide)

        self.slide_anim.start()

    ########################################################
    # Fade Bubble
    ########################################################

    def show_bubble(self):

        self.bubble_effect.setOpacity(0)

        self.fade_anim = QPropertyAnimation(
            self.bubble_effect,
            b"opacity"
        )

        self.fade_anim.setDuration(350)

        self.fade_anim.setStartValue(0)

        self.fade_anim.setEndValue(1)

        self.fade_anim.start()

    ########################################################
    # Play Intro
    ########################################################

    def play_intro(self):

        self.show_popup()

        self.slide_in()

        QTimer.singleShot(
            700,
            self.show_bubble
        )

    ########################################################
    # Play Exit
    ########################################################

    def play_exit(self):

        self.slide_out()