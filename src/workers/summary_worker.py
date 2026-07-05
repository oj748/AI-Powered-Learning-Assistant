from PySide6.QtCore import QThread, Signal

from services.summarize import summarize_text
from services.summarize_online import summarize_online


class SummaryWorker(QThread):

    finished = Signal(str)
    progress = Signal(str)

    def __init__(self, transcript, online=False):
        super().__init__()

        self.transcript = transcript
        self.online = online

    def run(self):

        if self.online:

            self.progress.emit(
                "Using Gemini..."
            )

            try:

                summary = summarize_online(
                    self.transcript
                )

            except Exception as e:

                print("Gemini failed:", e)

                self.progress.emit(
                    "Gemini unavailable. Falling back to local model..."
                )

                summary = self._offline_summary()

        else:

            self.progress.emit(
                "Offline mode selected."
            )

            summary = self._offline_summary()

        self.finished.emit(summary)

    def _offline_summary(self):

        self.progress.emit(
            "Running Phi locally..."
        )

        return summarize_text(
            self.transcript
        )