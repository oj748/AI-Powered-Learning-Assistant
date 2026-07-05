from PySide6.QtCore import QThread, Signal

from services.flashcards import create_flashcard
from services.flashcards_online import create_flashcard_online


class FlashcardWorker(QThread):

    finished = Signal(object)
    progress = Signal(str)

    def __init__(self, text, online=False):
        super().__init__()

        self.text = text
        self.online = online

    def run(self):

        if self.online:

            self.progress.emit(
                "Using Gemini..."
            )

            try:

                flashcards = create_flashcard_online(
                    self.text
                )

            except Exception as e:

                print("Gemini failed:", e)

                self.progress.emit(
                    "Gemini unavailable. Falling back to local model..."
                )

                flashcards = self._offline_flashcards()

        else:

            self.progress.emit(
                "Offline mode selected."
            )

            flashcards = self._offline_flashcards()

        self.finished.emit(
            flashcards
        )

    def _offline_flashcards(self):

        self.progress.emit(
            "Running Phi locally..."
        )

        return create_flashcard(
            self.text
        )