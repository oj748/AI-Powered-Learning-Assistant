from PySide6.QtCore import QThread, Signal
from services.phi4 import get_phi

class ModelPreloadWorker(QThread):

    finished = Signal()

    def run(self):
        get_phi()
        self.finished.emit()