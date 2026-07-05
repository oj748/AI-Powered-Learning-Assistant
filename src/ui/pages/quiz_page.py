from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton
)

from ui.pages.quiz_viewer import QuizViewer


class QuizPage(QWidget):

    def __init__(self):
        super().__init__()

        self.quiz_data = []
        self.current_question = 0
        self.score = 0
        self.answered = 0

        self.setup_ui()

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(20, 20, 20, 20)

        layout.setSpacing(15)

        # -----------------------------------------
        # Quiz Viewer
        # -----------------------------------------

        self.viewer = QuizViewer()

        layout.addWidget(self.viewer)

        # -----------------------------------------
        # Bottom
        # -----------------------------------------

        self.next_btn = QPushButton("Submit Answer")
        self.next_btn.setObjectName("primaryButton")

        layout.addWidget(self.next_btn)
        self.next_btn.hide()

        self.next_btn.clicked.connect(
            self.next_clicked
        )

    # ==================================================
    # Loading
    # ==================================================

    def load_quiz(self, quiz):
        self.score = 0
        self.answered = 0

        self.quiz_data = quiz

        self.current_question = 0
        self.next_btn.setEnabled(True)

        self.load_current_question()

    def load_current_question(self):

        question = self.quiz_data[
            self.current_question
        ]

        progress = (
            f"Question "
            f"{self.current_question + 1}"
            f" / "
            f"{len(self.quiz_data)}"
        )

        self.viewer.load_question(

            progress,

            question["question"],

            question["options"]

        )

        self.next_btn.setText(
            "Submit Answer"
        )

    # ==================================================
    # Button
    # ==================================================

    def next_clicked(self):

        if self.next_btn.text() == "Retry Quiz":
            self.load_quiz(self.quiz_data)
            return

        if self.next_btn.text() == "Submit Answer":

            self.viewer.selected_option(

                self.answer_selected

            )

            return

        self.current_question += 1

        if self.current_question >= len(
                self.quiz_data
        ):

            self.display_results()

            return

        self.load_current_question()

    # ==================================================
    # Answer
    # ==================================================

    def answer_selected(self, selected):

        if selected is None:

            return

        question = self.quiz_data[
            self.current_question
        ]

        if selected == question["correct"]:
            self.score += 1

        self.answered += 1

        self.viewer.show_feedback(

            selected,

            question["correct"],

            question["explanation"]

        )

        if self.current_question + 1 >= len(self.quiz_data):
            self.next_btn.setText(
                "End Quiz"
            )
        else :
            self.next_btn.setText(
                "Next Question"
            )

    def display_results(self):

        self.viewer.show_results(
            self.score,
            len(self.quiz_data)
        )

        self.next_btn.setText("Retry Quiz")

        return

