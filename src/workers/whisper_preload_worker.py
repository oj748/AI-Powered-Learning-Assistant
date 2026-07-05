from PySide6.QtCore import QThread
from services.speech import load_whisper

class WhisperPreloadWorker(QThread):

    def run(self):
        load_whisper()