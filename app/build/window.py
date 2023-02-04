from PyQt5.QtWidgets import (
    QWidget,
    QDesktopWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox
)
from PyQt5.QtCore import (
    Qt,
    QTimer,
    QThread,
    QUrl,
    QPoint
)
from PyQt5.QtGui import (
    QFontDatabase,
    QMouseEvent,
    QPixmap,
    QResizeEvent
)
from PyQt5.QtMultimedia import (
    QMediaPlayer,
    QMediaContent
)
from app.build.variables import *
from app.build.threads import (
    AudioFeedback,
    FileHandler
)


class Pomodoro(QWidget):
    """The Main Window of the Pomodoro Application."""

    def __init__(self):
        super().__init__()

        self.setObjectName("Pomodoro")
        self.InitSoundEffect()
        self.InitUI()
        self.InitStyle()
        self.InitWindow()
        self.InitTimer()


    def InitWindow(self):
        """Handles the window geometry and shows the window."""

        self.resize(WIN_WIDTH, WIN_HEIGHT)
        self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)
        self.goto_center()
        
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.show()

    
    def InitStyle(self):
        """Reads the qss file from the style folder"""

        QFontDatabase.addApplicationFont(OPEN_SANS_MEDIUM)
        QFontDatabase.addApplicationFont(OPEN_SANS_EXTRABOLD)
        with open(STYLESHEET_LOC, "r") as qss_file:
            self.setStyleSheet(qss_file.read())


    def InitSoundEffect(self):
        """Initialize Sound effect from file"""

        self.click_sound = QMediaPlayer(self)
        self.click_sound.setMedia(QMediaContent(QUrl.fromLocalFile(BUTTON_CLICK)))
        

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
        main_v_layout.setContentsMargins(0, 0, 0, 0)
        main_v_layout.setSpacing(0)
        # main_v_layout.setAlignment(Qt.AlignCenter)

        # Custom title bar
        self.title_bar = PomodoroTitleBar(self)
        main_v_layout.addWidget(self.title_bar)

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
        self.start_btn.clicked.connect(self.click_sound.play)
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setDisabled(True)
        self.stop_btn.clicked.connect(self.click_sound.play)
        self.stop_btn.clicked.connect(self.stop)

        row_2.addWidget(self.start_btn)
        row_2.addWidget(self.stop_btn)
        main_v_layout.addLayout(row_2)


        # --- 3rd row
        row_3 = QHBoxLayout()

        self.study_time_btn = QPushButton("Study Time")
        self.study_time_btn.clicked.connect(self.study_time_func)
        self.study_time_btn.clicked.connect(self.click_sound.play)
        self.short_break_btn = QPushButton("Short Break")
        self.short_break_btn.clicked.connect(self.short_break_time_func)
        self.short_break_btn.clicked.connect(self.click_sound.play)
        self.long_break_btn = QPushButton("Long Break")
        self.long_break_btn.clicked.connect(self.long_break_time_func)
        self.long_break_btn.clicked.connect(self.click_sound.play)

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
        self.study_time_btn.setDisabled(True)
        self.short_break_btn.setDisabled(True)
        self.long_break_btn.setDisabled(True)
        if self.isPaused != True:
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
        # self.run = False
        self.isPaused = False
        self.time_to_record = self.time_to_string()

        self.stop_dialog = StopDialog()
        user_resp = self.stop_dialog.exec()
        # Stop timer and save
        if user_resp == QMessageBox.Save:
            self.save_record()
            
        # Continue timer
        elif user_resp == QMessageBox.Cancel:
            self.click_sound.play()
            return self.start()

        # skip both if not saving (discard)
        self.click_sound.play()
        # If stopped then check timer state
        self.start_btn.setText("Start")
        if self.timer_state == STUDY_TIME_STATE:
            return self.study_time_func()
            # self.current_time = STUDY_TIME_SEC

        elif self.timer_state == SBREAK_TIME_STATE:
            # self.current_time = SBREAK_TIME_SEC
            return self.short_break_time_func()

        elif self.timer_state == LBREAK_TIME_STATE:
            # self.current_time = LBREAK_TIME_SEC
            return self.long_break_time_func()


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
        self.isPaused = False

        self.current_time = STUDY_TIME_SEC
        self.current_time_str = self.time_to_string()
        self.current_timer_label.setText(self.current_time_str)

        self.start_btn.setDisabled(False)
        self.start_btn.setText("Start")
        self.stop_btn.setDisabled(True)
        self.study_time_btn.setDisabled(True)
        self.short_break_btn.setDisabled(False)
        self.long_break_btn.setDisabled(False)
        

    def short_break_time_func(self):

        self.timer_state = SBREAK_TIME_STATE
        self.run = False
        self.isPaused = False

        self.current_time = SBREAK_TIME_SEC
        self.current_time_str = self.time_to_string()
        self.current_timer_label.setText(self.current_time_str)

        self.start_btn.setDisabled(False)
        self.start_btn.setText("Start")
        self.stop_btn.setDisabled(True)
        self.short_break_btn.setDisabled(True)
        self.study_time_btn.setDisabled(False)
        self.long_break_btn.setDisabled(False)


    def long_break_time_func(self):

        self.timer_state = LBREAK_TIME_STATE
        self.run = False
        self.isPaused = False

        self.current_time = LBREAK_TIME_SEC
        self.current_time_str = self.time_to_string()
        self.current_timer_label.setText(self.current_time_str)

        self.start_btn.setDisabled(False)
        self.start_btn.setText("Start")
        self.stop_btn.setDisabled(True)
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


    def closeEvent(self, event) -> None:
        return super().closeEvent(event)


class StopDialog(QMessageBox):
    """Dialog Popup when stopping timer."""

    def __init__(self):
        super().__init__()
        self.setObjectName("StopDialog")
        self.InitUI()
        self.InitStyle()
        self.setWindowFlags(Qt.FramelessWindowHint)

    
    def InitStyle(self):
        with open(STYLESHEET_LOC, "r") as qss_file:
            self.setStyleSheet(qss_file.read())


    def InitUI(self):
        icon = QPixmap(ICON_QUESION).scaled(80, 80)
        self.setIconPixmap(icon)

        self.setText("You stopped the timer.")
        self.setInformativeText("Do you want to save recorded time?")

        self.setStandardButtons(
            QMessageBox.Discard | QMessageBox.Cancel | QMessageBox.Save
        )
        self.setDefaultButton(QMessageBox.Save)

    
    def mousePressEvent(self, event: QMouseEvent):
        self.old_pos = event.globalPos()
        

    def mouseMoveEvent(self, event: QMouseEvent):
        delta = QPoint(event.globalPos() - self.old_pos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPos()


class PomodoroTitleBar(QWidget):
    """Custom Title bar for Pomodoro App"""

    def __init__(self, parent: Pomodoro):
        super().__init__()
        self.setObjectName("Titlebar")
        self.pomodoro_main = parent
        self.setFixedHeight(TITLE_HEIGHT)
        self.InitUI()


    def InitUI(self):

        btn_height = TITLE_HEIGHT
        btn_width = btn_height

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.title = QLabel("Pomodoro")
        self.title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title)


        self.minimize_btn = QPushButton("-")
        self.minimize_btn.setObjectName("MinimizeBtn")
        self.minimize_btn.clicked.connect(self.minimize_button_func)
        self.minimize_btn.setFixedSize(btn_width, btn_height)
        main_layout.addWidget(self.minimize_btn)


        self.close_btn = QPushButton("X")
        self.close_btn.setObjectName("CloseBtn")
        self.close_btn.clicked.connect(self.close_button_func)
        self.close_btn.setFixedSize(btn_width, btn_height)
        main_layout.addWidget(self.close_btn)


        self.setLayout(main_layout)


    def mousePressEvent(self, event: QMouseEvent):
        self.old_pos = event.globalPos()


    def mouseMoveEvent(self, event: QMouseEvent):
        delta = QPoint(event.globalPos() - self.old_pos)
        self.pomodoro_main.move(self.pomodoro_main.x() + delta.x(), self.pomodoro_main.y() + delta.y())
        self.old_pos = event.globalPos()

    
    # def ResizeEvent(self, event: QResizeEvent):
    #     super().resizeEvent(event)
    #     self.title.setFixedWidth(self.pomodoro_main.width)


    def minimize_button_func(self):
        self.pomodoro_main.showMinimized()


    def close_button_func(self):
        self.pomodoro_main.close()