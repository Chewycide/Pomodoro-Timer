from PyQt5.QtWidgets import (
    QWidget,
    QDesktopWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel
)
from PyQt5.QtCore import (
    Qt
)


WIN_WIDTH = 500
WIN_HEIGHT = WIN_WIDTH


class Pomodoro(QWidget):
    """The Main Window of the Pomodoro Application"""

    def __init__(self):
        super().__init__()

        self.InitUI()
        self.InitWindow()


    def InitWindow(self):
        """Handles the window geometry and shows the window"""

        self.resize(WIN_WIDTH, WIN_HEIGHT)
        self.setMinimumSize(500, 500)
        self.goto_center()

        self.show()
        

    def goto_center(self):
        """Move the window to center upon initialization"""

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def InitUI(self):
        """Initializes all the layouts and components of the application."""

        # --- Main Layout of the window
        main_v_layout = QVBoxLayout()
        main_v_layout.setAlignment(Qt.AlignCenter)
        

        # --- 1st row
        row_1 = QHBoxLayout()
        timer_placeholder = QLabel()
        timer_placeholder.setText("00:00")
        row_1.addWidget(timer_placeholder)
        main_v_layout.addLayout(row_1)


        # --- Set the layout of the window
        self.setLayout(main_v_layout)