from PyQt5.QtWidgets import (
    QWidget,
    QDesktopWidget,
    QVBoxLayout,
    QHBoxLayout
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
        """Initializes all the layouts and components of the application"""
        pass

        
        

