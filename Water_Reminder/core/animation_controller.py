from PySide6.QtCore import (
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QParallelAnimationGroup,
    QSequentialAnimationGroup,
)
from PySide6.QtWidgets import (
    QGraphicsOpacityEffect,
)


class AnimationController:

    def __init__(self, popup):

        self.popup = popup

        self.effects = {}

    ##########################################################

    def _opacity(self, widget):

        if widget not in self.effects:

            effect = QGraphicsOpacityEffect(widget)

            effect.setOpacity(1)

            widget.setGraphicsEffect(effect)

            self.effects[widget] = effect

        return self.effects[widget]

    ##########################################################

    def fade_in(self, widget, duration=350):

        effect = self._opacity(widget)

        effect.setOpacity(0)

        widget.show()

        anim = QPropertyAnimation(effect, b"opacity")

        anim.setDuration(duration)

        anim.setStartValue(0)

        anim.setEndValue(1)

        anim.setEasingCurve(QEasingCurve.OutCubic)

        return anim

    ##########################################################

    def fade_out(self, widget, duration=250):

        effect = self._opacity(widget)

        anim = QPropertyAnimation(effect, b"opacity")

        anim.setDuration(duration)

        anim.setStartValue(1)

        anim.setEndValue(0)

        anim.setEasingCurve(QEasingCurve.OutCubic)

        return anim

    ##########################################################

    def slide_in(self):

        end = self.popup.pos()

        start = QPoint(end.x(), end.y() + 70)

        self.popup.move(start)

        anim = QPropertyAnimation(self.popup, b"pos")

        anim.setDuration(450)

        anim.setStartValue(start)

        anim.setEndValue(end)

        anim.setEasingCurve(QEasingCurve.OutBack)

        return anim

    ##########################################################

    def bounce_character(self):

        label = self.popup.character

        pos = label.pos()

        up = QPoint(pos.x(), pos.y() - 10)

        down = QPoint(pos.x(), pos.y())

        a1 = QPropertyAnimation(label, b"pos")
        a1.setDuration(170)
        a1.setStartValue(down)
        a1.setEndValue(up)

        a2 = QPropertyAnimation(label, b"pos")
        a2.setDuration(170)
        a2.setStartValue(up)
        a2.setEndValue(down)

        group = QSequentialAnimationGroup()

        group.addAnimation(a1)
        group.addAnimation(a2)

        return group

    ##########################################################

    def play_intro(self):

        slide = self.slide_in()

        bounce = self.bounce_character()

        bubble = self.fade_in(self.popup.bubble)

        drink = self.fade_in(self.popup.drink_btn)

        snooze = self.fade_in(self.popup.snooze_btn)

        close = self.fade_in(self.popup.close_btn)

        buttons = QParallelAnimationGroup()

        buttons.addAnimation(drink)
        buttons.addAnimation(snooze)
        buttons.addAnimation(close)

        sequence = QSequentialAnimationGroup()

        sequence.addAnimation(slide)

        sequence.addAnimation(bounce)

        sequence.addAnimation(bubble)

        sequence.addAnimation(buttons)

        self.sequence = sequence

        self.sequence.start()

    ##########################################################

    def play_exit(self):

        fade = self.fade_out(self.popup.card, 220)

        fade.finished.connect(self.popup.hide)

        self.fade = fade

        self.fade.start()