from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import playsound


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
        playsound.playsound("assets/default_alert.wav")
        self.finished.emit()