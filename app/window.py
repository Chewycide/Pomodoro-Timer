from PyQt5.QtWidgets import (
    QWidget,
    QDesktopWidget,
)


class Pomodoro(QWidget):
    """The Main Window of the Pomodoro Application"""

    def __init__(self):
        super().__init__()

        self.InitUI()


    def InitUI(self):
        """Initializes the main UI of the Pomodoro app"""

        self.resize(500, 500)
        self.setMinimumSize(500, 500)
        self.goto_center()

        self.show()
        

    def goto_center(self):
        """Move the window to center upon initialization"""

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


