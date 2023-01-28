from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from app.variables import DEFAULT_ALERT
import datetime as dt
import playsound
import csv


class AudioFeedback(QObject):
    """
        Worker thread for giving audio feedback to the user. This 
        thread is required to play the audio without blocking the
        main thread.
    """
    finished = pyqtSignal()

    @pyqtSlot()
    def play_audio(self):
        """Play audio"""
        playsound.playsound(DEFAULT_ALERT)
        self.finished.emit()


class FileHandler(QObject):

    finished = pyqtSignal()

    @pyqtSlot()
    def create_record(self, t_state: int, c_time: str):
        """
            Creates a record to be saved as an external file.

            params:

            t_state: timer state
            c_time: current_time
        """
        if t_state == 0:
            self.save_to_csv("STUDY TIME", c_time)
        elif t_state == 1:
            self.save_to_csv("SHORT BREAK", c_time)
        elif t_state == 2:
            self.save_to_csv("LONG BREAK", c_time)

        self.finished.emit()
    
    
    def save_to_csv(self, c_type, c_time):
        """
            Handles file creation and saving.
        """
        c_date = dt.date.today()
        c_month = c_date.strftime("%B")
        c_day = c_date.strftime("%d")
        c_year = c_date.strftime("%Y")


        with open("userdata.csv", "a", newline='') as csv_file:
            record_writer = csv.writer(csv_file)
            record_writer.writerow([c_type, c_time, c_month, c_day, c_year])