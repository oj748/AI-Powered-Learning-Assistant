from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel
)

from ui.pages.flashcard_viewer import FlashcardViewer


class FlashcardPage(QWidget):

    def __init__(self):
        super().__init__()

        self.flashcards = []
        self.current_card = 0

        self.setup_ui()
        self.setup_shortcuts()

    # ======================================================
    # UI
    # ======================================================

    def setup_ui(self):

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(25, 20, 25, 20)
        main_layout.setSpacing(18)

        # --------------------------------------------------
        # Progress
        # --------------------------------------------------

        self.progress_label = QLabel("No Flashcards")

        self.progress_label.setAlignment(
            Qt.AlignCenter
        )

        main_layout.addWidget(
            self.progress_label
        )

        # --------------------------------------------------
        # Viewer + Arrows
        # --------------------------------------------------

        viewer_layout = QHBoxLayout()

        self.prev_btn = QPushButton("◀")
        self.next_btn = QPushButton("▶")

        self.prev_btn.setFixedSize(54, 54)
        self.next_btn.setFixedSize(54, 54)

        self.viewer = FlashcardViewer()

        viewer_layout.addWidget(
            self.prev_btn,
            alignment=Qt.AlignCenter
        )

        viewer_layout.addWidget(
            self.viewer,
            stretch=1
        )

        viewer_layout.addWidget(
            self.next_btn,
            alignment=Qt.AlignCenter
        )

        main_layout.addLayout(
            viewer_layout,
            stretch=1
        )

        # --------------------------------------------------
        # Connections
        # --------------------------------------------------

        self.prev_btn.clicked.connect(
            self.prev_card
        )

        self.next_btn.clicked.connect(
            self.next_card
        )

    # ======================================================
    # Keyboard
    # ======================================================

    def setup_shortcuts(self):

        self.space_shortcut = QShortcut(
            QKeySequence(Qt.Key_Space),
            self
        )

        self.space_shortcut.activated.connect(
            self.reveal_card
        )

        self.left_shortcut = QShortcut(
            QKeySequence(Qt.Key_Left),
            self
        )

        self.left_shortcut.activated.connect(
            self.prev_card
        )

        self.right_shortcut = QShortcut(
            QKeySequence(Qt.Key_Right),
            self
        )

        self.right_shortcut.activated.connect(
            self.next_card
        )

    # ======================================================
    # Loading
    # ======================================================

    def load_flashcards(self, flashcards):

        self.flashcards = flashcards

        self.current_card = 0

        if not flashcards:

            self.progress_label.setText(
                "No Flashcards"
            )

            self.viewer.clear()

            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(False)

            return

        self.display_card()

    # ======================================================
    # Display
    # ======================================================

    def display_card(self):

        card = self.flashcards[
            self.current_card
        ]

        self.progress_label.setText(

            f"Card "

            f"{self.current_card + 1}"

            f" / "

            f"{len(self.flashcards)}"

        )

        self.viewer.load_card(

            card["question"],

            card["answer"]

        )

        self.prev_btn.setEnabled(
            self.current_card > 0
        )

        self.next_btn.setEnabled(
            self.current_card < len(self.flashcards)-1
        )

    # ======================================================
    # Reveal
    # ======================================================

    def reveal_card(self):

        self.viewer.is_revealed(
            self._handle_reveal
        )

    def _handle_reveal(self, revealed):

        if not revealed:

            self.viewer.reveal()

    # ======================================================
    # Navigation
    # ======================================================

    def next_card(self):

        if self.current_card >= len(self.flashcards)-1:
            return

        self.current_card += 1

        self.display_card()

    def prev_card(self):

        if self.current_card <= 0:
            return

        self.current_card -= 1

        self.display_card()

    def has_flashcards(self):
        return bool(self.flashcards)