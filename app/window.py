from PyQt5.QtWidgets import (
    QWidget,
    QDesktopWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from PyQt5.QtCore import (
    Qt,
    QTimer
)
from app.variables import *


class Pomodoro(QWidget):
    """The Main Window of the Pomodoro Application."""

    def __init__(self):
        super().__init__()

        self.InitUI()
        self.InitWindow()
        self.InitTimer()


    def InitWindow(self):
        """Handles the window geometry and shows the window."""

        self.resize(WIN_WIDTH, WIN_HEIGHT)
        self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)
        self.goto_center()
        
        self.setWindowTitle("Pomodoro")

        self.show()
        

    def goto_center(self):
        """Move the window to center upon initialization."""

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def InitUI(self):
        """Initializes all the layouts and components of the application."""

        # --- Main Layout of the window
        main_v_layout = QVBoxLayout()
        # main_v_layout.setAlignment(Qt.AlignCenter)
        

        # --- 1st row
        row_1 = QHBoxLayout()
        row_1.setAlignment(Qt.AlignCenter)

        self.current_timer_label = QLabel("25:00")

        row_1.addWidget(self.current_timer_label)
        main_v_layout.addLayout(row_1)


        # --- 2nd row
        row_2 = QHBoxLayout()

        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start)
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop)

        row_2.addWidget(self.start_btn)
        row_2.addWidget(self.stop_btn)
        main_v_layout.addLayout(row_2)


        # --- Set the layout of the window
        self.setLayout(main_v_layout)


    def InitTimer(self):
        """Initialize the Pomodoro's timer."""

        self.run = False
        self.current_time = 0
        self.current_timer = QTimer()
        self.current_timer.timeout.connect(self.display_time)
        self.current_timer.start(1000)


    def display_time(self):
        """Function to display the time."""

        self.current_time_min = self.current_time // 60
        self.current_time_sec = self.current_time % 60

        # when minutes and seconds reaches single-digit values it will 
        # not display a zero before the current digit therefore this 
        # statement will add zero before the digit.
        if self.current_time_sec < 10:
            self.current_time_sec = f"0{self.current_time_sec}"
        if self.current_time_min < 10:
            self.current_time_min = f"0{self.current_time_min}"

        # variable to be used to store time as a string
        self.current_time_str = f"{self.current_time_min}:{self.current_time_sec}"

        # must display time when user clicked the start button
        if self.run and self.current_time >= 0:
            self.current_time -=1
            self.current_timer_label.setText(self.current_time_str)

        # stop running upon displaying zero
        elif self.current_time < 0:
            self.run = False


    def start(self):
        """Handles starting of the pomodoro timer"""
        
        self.current_time = STUDY_TIME_SEC
        self.run = True


    def stop(self):
        """Handles stopping of the pomodoro timer"""

        self.current_time = STUDY_TIME_SEC
        self.run = False
