from PyQt5.QtWidgets import QApplication
from app.build.window import Pomodoro
import sys


def run_app() -> None:
    """Will run the application"""

    pomodoro_app = QApplication(sys.argv)
    window = Pomodoro()
    sys.exit(pomodoro_app.exec())