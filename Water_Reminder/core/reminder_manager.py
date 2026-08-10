import json
from pathlib import Path

from PySide6.QtCore import QObject, QTimer
from PySide6.QtWidgets import QMessageBox

from ui.reminder import ReminderPopup


class ReminderManager(QObject):

    def __init__(self):
        super().__init__()

        self.settings_file = (
            Path(__file__).parent.parent / "settings.json"
        )

        self.popup = ReminderPopup()

        self.popup.drank.connect(self.drank_water)
        self.popup.snooze.connect(self.snooze)
        self.popup.closed.connect(self.close_popup)

        #########################################################

        # Reminder timer
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.show_popup)

        # Auto hide timer
        self.auto_hide = QTimer(self)
        self.auto_hide.setSingleShot(True)
        self.auto_hide.timeout.connect(self.close_popup)

        #########################################################

        self.load_settings()

    #########################################################

    def load_settings(self):

        if not self.settings_file.exists():

            self.interval = 30

            self.save_settings()

            return

        with open(self.settings_file, "r") as file:

            data = json.load(file)

        self.interval = data.get("interval", 30)

    #########################################################

    def save_settings(self):

        with open(self.settings_file, "w") as file:

            json.dump(
                {"interval": self.interval},
                file,
                indent=4
            )

    #########################################################

    def start(self):

        # Uncomment this while testing
        self.show_popup()

        # Comment this while testing
        # self.start_timer(self.interval)

    #########################################################

    def start_timer(self, minutes):

        self.timer.stop()

        milliseconds = minutes * 60 * 1000

        # Testing
        # milliseconds = 5000

        self.timer.start(milliseconds)

        print(f"Next reminder in {minutes} minute(s)")

    #########################################################

    def show_popup(self):

        self.popup.play_intro()

        self.auto_hide.start(30000)

    #########################################################

    def drank_water(self):

        self.auto_hide.stop()

        self.popup.play_exit()

        msg = QMessageBox()

        msg.setWindowTitle("Great!")

        msg.setText(
            "When should I remind you again?"
        )

        btn30 = msg.addButton(
            "30 Minutes",
            QMessageBox.AcceptRole
        )

        btn60 = msg.addButton(
            "1 Hour",
            QMessageBox.AcceptRole
        )

        msg.exec()

        if msg.clickedButton() == btn30:

            self.interval = 30

        else:

            self.interval = 60

        self.save_settings()

        self.start_timer(self.interval)

    #########################################################

    def snooze(self):

        self.auto_hide.stop()

        self.popup.play_exit()

        print("Snoozed for 10 minutes")

        self.start_timer(10)

    #########################################################

    def close_popup(self):

        self.auto_hide.stop()

        self.popup.play_exit()

        self.start_timer(self.interval)