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
    QTimer,
    QThread
)
from PyQt5.QtGui import QFontDatabase
from app.variables import *
from app.threads import (
    AudioFeedback,
    ButtonClickAudio,
    FileHandler
)


class Pomodoro(QWidget):
    """The Main Window of the Pomodoro Application."""

    def __init__(self):
        super().__init__()

        self.setObjectName("Pomodoro")
        self.InitUI()
        self.InitStyle()
        self.InitWindow()
        self.InitTimer()


    def InitWindow(self):
        """Handles the window geometry and shows the window."""

        self.resize(WIN_WIDTH, WIN_HEIGHT)
        self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)
        self.goto_center()
        
        self.setWindowTitle("Pomodoro")

        self.show()

    
    def InitStyle(self):
        """Reads the qss file from the style folder"""

        QFontDatabase.addApplicationFont(OPEN_SANS_MEDIUM)
        QFontDatabase.addApplicationFont(OPEN_SANS_EXTRABOLD)
        with open(STYLESHEET_LOC, "r") as qss_file:
            self.setStyleSheet(qss_file.read())
        

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
        self.current_timer_label.setObjectName("Timer")

        row_1.addWidget(self.current_timer_label)
        main_v_layout.addLayout(row_1)


        # --- 2nd row
        row_2 = QHBoxLayout()

        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start)
        self.start_btn.clicked.connect(self.feedback_audio)
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setDisabled(True)
        self.stop_btn.clicked.connect(self.stop)
        self.stop_btn.clicked.connect(self.feedback_audio)

        row_2.addWidget(self.start_btn)
        row_2.addWidget(self.stop_btn)
        main_v_layout.addLayout(row_2)


        # --- 3rd row
        row_3 = QHBoxLayout()

        self.study_time_btn = QPushButton("Study Time")
        self.study_time_btn.clicked.connect(self.study_time_func)
        self.study_time_btn.clicked.connect(self.feedback_audio)
        self.short_break_btn = QPushButton("Short Break")
        self.short_break_btn.clicked.connect(self.short_break_time_func)
        self.short_break_btn.clicked.connect(self.feedback_audio)
        self.long_break_btn = QPushButton("Long Break")
        self.long_break_btn.clicked.connect(self.long_break_time_func)
        self.long_break_btn.clicked.connect(self.feedback_audio)

        row_3.addWidget(self.study_time_btn)
        row_3.addWidget(self.short_break_btn)
        row_3.addWidget(self.long_break_btn)
        main_v_layout.addLayout(row_3)


        # --- Set the layout of the window
        self.setLayout(main_v_layout)


    def InitTimer(self):
        """Initialize the Pomodoro's timer."""

        self.isPaused = False
        self.timer_state = STUDY_TIME_STATE
        self.study_time_btn.setDisabled(True)
        self.run = False
        self.current_time = STUDY_TIME_SEC
        self.current_timer = QTimer()
        self.current_timer.timeout.connect(self.display_time)
        self.current_timer.start(NORMAL_INTERVAL)


    def display_time(self):
        """Function to display the time."""

        # variable to be used to store time as a string
        self.current_time_str = self.time_to_string()

        # must display time when user clicked the start button
        if self.run and self.current_time >= 0:
            self.current_time -= 1
            self.current_timer_label.setText(self.current_time_str)

        # stop running upon displaying zero
        elif self.current_time < 0:
            self.run = False
            # call alert function
            self.alert_audio()
            # will stop audio function from being called every second
            self.current_time = 0
            self.stop()


    def start(self):
        """Handles starting of the pomodoro timer"""
        
        self.stop_btn.setDisabled(False)
        if not self.isPaused == True:
            self.start_btn.setText("Pause")
            self.isPaused = True
            self.run = True

        elif self.isPaused == True:
            self.isPaused = False
            self.start_btn.setText("Resume")
            self.run = False


    def stop(self):
        """Handles stopping of the pomodoro timer"""

        self.start_btn.setDisabled(False)
        self.stop_btn.setDisabled(True)
        self.run = False
        self.time_to_record = self.time_to_string()
        self.save_record()


        if self.timer_state == STUDY_TIME_STATE:
            self.current_time = STUDY_TIME_SEC

        elif self.timer_state == SBREAK_TIME_STATE:
            self.current_time = SBREAK_TIME_SEC

        elif self.timer_state == LBREAK_TIME_STATE:
            self.current_time = LBREAK_TIME_SEC

        self.current_time_str = self.time_to_string()
        self.current_timer_label.setText(self.current_time_str)


    def time_to_string(self) -> str:
        """
            function that returns the full time in mins and return it as a 
            string with the format:

            mm:ss

            wherein mm is minutes and ss is seconds. e.g. 09:59
        """

        self.current_time_min = self.current_time // 60
        self.current_time_sec = self.current_time % 60

        # when minutes and seconds reaches single-digit values it will 
        # not display a zero before the current digit therefore this 
        # statement will add zero before the digit.
        if self.current_time_sec < 10:
            self.current_time_sec = f"0{self.current_time_sec}"
        if self.current_time_min < 10:
            self.current_time_min = f"0{self.current_time_min}"

        return f"{self.current_time_min}:{self.current_time_sec}"


    def study_time_func(self):

        self.timer_state = STUDY_TIME_STATE
        self.run = False

        self.current_time = STUDY_TIME_SEC
        self.current_time_str = self.time_to_string()
        self.current_timer_label.setText(self.current_time_str)

        self.start_btn.setDisabled(False)
        self.study_time_btn.setDisabled(True)
        self.short_break_btn.setDisabled(False)
        self.long_break_btn.setDisabled(False)
        

    def short_break_time_func(self):

        self.timer_state = SBREAK_TIME_STATE
        self.run = False

        self.current_time = SBREAK_TIME_SEC
        self.current_time_str = self.time_to_string()
        self.current_timer_label.setText(self.current_time_str)

        self.start_btn.setDisabled(False)
        self.short_break_btn.setDisabled(True)
        self.study_time_btn.setDisabled(False)
        self.long_break_btn.setDisabled(False)


    def long_break_time_func(self):
        
        self.timer_state = LBREAK_TIME_STATE
        self.run = False

        self.current_time = LBREAK_TIME_SEC
        self.current_time_str = self.time_to_string()
        self.current_timer_label.setText(self.current_time_str)

        self.start_btn.setDisabled(False)
        self.long_break_btn.setDisabled(True)
        self.study_time_btn.setDisabled(False)
        self.short_break_btn.setDisabled(False)


    def alert_audio(self):
        """Will alert user via audio."""

        self.alert_thread = QThread(self)
        self.alert_worker = AudioFeedback()
        self.alert_worker.moveToThread(self.alert_thread)

        # signals
        self.alert_thread.started.connect(self.alert_worker.play_audio)
        self.alert_worker.finished.connect(self.alert_thread.quit)
        self.alert_worker.finished.connect(self.alert_worker.deleteLater)
        self.alert_thread.finished.connect(self.alert_thread.deleteLater)
        self.alert_thread.start()


    def save_record(self):
        """Save record when timer stops."""
        
        self.file_thread = QThread(self)
        self.file_handler = FileHandler()
        self.file_handler.moveToThread(self.file_thread)

        #signals
        self.file_thread.started.connect(
            lambda: self.file_handler.create_record(
                self.timer_state,
                self.time_to_record
            )
        )
        self.file_handler.finished.connect(self.file_thread.quit)
        self.file_handler.finished.connect(self.file_handler.deleteLater)
        self.file_thread.finished.connect(self.file_thread.deleteLater)
        self.file_thread.start()


    def feedback_audio(self):
        """Button click audio feedback."""

        self.btnclk_thread = QThread(self)
        self.btnclk_audio = ButtonClickAudio()
        self.btnclk_audio.moveToThread(self.btnclk_thread)

        # signals
        self.btnclk_thread.started.connect(self.btnclk_audio.play_feedback)
        self.btnclk_audio.finished.connect(self.btnclk_thread.quit)
        self.btnclk_audio.finished.connect(self.btnclk_audio.deleteLater)
        self.btnclk_thread.finished.connect(self.btnclk_thread.deleteLater)
        self.btnclk_thread.start()


    def closeEvent(self, event) -> None:
        """
            Reimplements Pomodoro app close event to check and cleanup threads
            that are still running.
        """
        # TODO: create a way to quit all threads
        try:
            self.btnclk_thread.quit()
            self.btnclk_thread.wait()
        except RuntimeError:
            return super().closeEvent(event)
        return super().closeEvent(event)