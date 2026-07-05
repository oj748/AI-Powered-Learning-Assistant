from PySide6.QtCore import QThread, Signal

from services.ocr import preload_ocr


class OCRPreloadWorker(QThread):

    finished = Signal()

    def run(self):

        preload_ocr()

        self.finished.emit()