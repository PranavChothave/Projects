import sys

from PySide6.QtWidgets import QApplication

from core.reminder_manager import ReminderManager

app = QApplication(sys.argv)

manager = ReminderManager()

manager.start()

sys.exit(app.exec())