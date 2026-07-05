from PySide6.QtCore import QThread, Signal

from services.quiz_generator import create_quiz
from services.quiz_generator_online import create_quiz_online

class QuizWorker(QThread):

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

                quiz = create_quiz_online(
                    self.text
                )

                self.progress.emit(
                    "Parsing quiz..."
                )


            except Exception as e:

                print("Gemini failed:", e)

                self.progress.emit(
                    "Gemini unavailable. Falling back to local model..."
                )

                quiz = self._offline_quiz()

        else:

            self.progress.emit(
                "Offline mode selected."
            )

            quiz = self._offline_quiz()

        self.finished.emit(
            quiz
        )

    def _offline_quiz(self):

        self.progress.emit(
            "Running Phi locally..."
        )

        return create_quiz(
            self.text
        )