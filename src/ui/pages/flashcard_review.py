from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
)
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtCore import (Qt, Signal)
from ui.pages.flashcard_viewer import FlashcardViewer

class FlashcardReview(QWidget):
    reviewed = Signal(int,int)

    def __init__(self):
        super().__init__()
        self.review_queue = []
        self.current_card = 0
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # ==========================
        # Header
        # ==========================
        self.back_btn = QPushButton("← Back to Dashboard")
        main_layout.addWidget(self.back_btn)

        # ==========================
        # Deck Title
        # ==========================
        self.deck_title = QLabel("Flashcards")
        self.deck_title.setAlignment(Qt.AlignCenter)

        font = self.deck_title.font()
        font.setPointSize(18)
        font.setBold(True)
        self.deck_title.setFont(font)

        main_layout.addWidget(self.deck_title)

        # ==========================
        # Progress
        # ==========================
        self.card_progress = QLabel("No Flashcards Loaded")
        self.card_progress.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(self.card_progress)

        # ==========================
        # Flashcard Viewer
        # ==========================

        self.viewer = FlashcardViewer()

        self.viewer.setMinimumHeight(520)
        self.viewer.setMaximumHeight(650)
        main_layout.addWidget(
            self.viewer,
            stretch=1
        )

        #==========================
        # REVIEW BUTTONS
        #==========================

        review_layout = QHBoxLayout()

        self.again_btn = QPushButton("Again")
        self.hard_btn = QPushButton("Hard")
        self.good_btn = QPushButton("Good")
        self.easy_btn = QPushButton("Easy")

        review_layout.addWidget(self.again_btn)
        review_layout.addWidget(self.hard_btn)
        review_layout.addWidget(self.good_btn)
        review_layout.addWidget(self.easy_btn)

        main_layout.addLayout(review_layout)

        self.again_btn.hide()
        self.hard_btn.hide()
        self.good_btn.hide()
        self.easy_btn.hide()

        main_layout.addStretch()

        self.space_shortcut = QShortcut(
            QKeySequence(Qt.Key_Space),
            self
        )

        self.space_shortcut.activated.connect(
            self.reveal_card
        )

        self.viewer.revealed.connect(
            self.show_review_buttons
        )

        self.again_btn.clicked.connect(
            lambda:
            self.review_current_card(0)
        )

        self.hard_btn.clicked.connect(
            lambda:
            self.review_current_card(1)
        )

        self.good_btn.clicked.connect(
            lambda:
            self.review_current_card(2)
        )

        self.easy_btn.clicked.connect(
            lambda:
            self.review_current_card(3)
        )

    def load_flashcards(self, flashcards):

        self.review_queue = flashcards.copy()

        self.current_card = 0

        if not self.review_queue:
            self.viewer.load_card("Nothing Due Today 🎉",
                                  "")


            self.card_progress.setText("0 Cards")

            return

        self.display_card()

    def display_card(self):

        card = self.review_queue[self.current_card]

        self.card_progress.setText(
            f"{len(self.review_queue)} cards remaining"
        )

        self.viewer.load_card(
            card["question"],
            card["answer"]
        )

        self.again_btn.hide()
        self.hard_btn.hide()
        self.good_btn.hide()
        self.easy_btn.hide()

    def reveal_card(self):
        if not self.review_queue:
            return

        self.viewer.reveal()

    def show_review_buttons(self):
        if not self.review_queue:
            return
        self.again_btn.show()
        self.hard_btn.show()
        self.good_btn.show()
        self.easy_btn.show()


    def review_current_card(self,rating):

        card = self.review_queue.pop(
            self.current_card
        )

        self.reviewed.emit(
            card["id"],
            rating
        )

        if rating == 0:
            self.review_queue.append(card)

        if not self.review_queue:
            self.viewer.load_card(
                "🎉 Review Complete!",
                "No cards remaining."
            )

            self.again_btn.hide()
            self.hard_btn.hide()
            self.good_btn.hide()
            self.easy_btn.hide()

            self.card_progress.setText(
                "0 Cards Remaining"
            )

            return

        self.current_card = 0

        self.display_card()