from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame, QHBoxLayout, QApplication, QStyle, QMessageBox, QGridLayout
)
from PySide6.QtCore import Qt, Signal
from database.flashcard_repository import (
    get_flashcards_for_deck, delete_deck, get_deck_statistics
)


class DeckPage(QWidget):

    deckDeleted = Signal(int)

    def __init__(self):
        super().__init__()

        self.deck_id = None

        self.setup_ui()

    def setup_ui(self):

        main_layout = QVBoxLayout(self)

        # ==========================
        # Back Button
        # ==========================

        self.back_btn = QPushButton(
            "← Back"
        )

        self.delete_deck_btn = QPushButton("Delete Deck")
        self.delete_deck_btn.setObjectName("dangerButton")
        self.delete_deck_btn.setIcon(
            QApplication.style().standardIcon(QStyle.SP_TrashIcon)
        )

      # ==========================
        # Deck Title
        # ==========================

        self.title_label = QLabel(
            "No Deck Selected"
        )

        self.title_label.setAlignment(
            Qt.AlignCenter
        )

        toolbar = QHBoxLayout()

        toolbar.addWidget(self.back_btn)

        toolbar.addStretch()

        toolbar.addWidget(self.title_label)

        toolbar.addStretch()

        toolbar.addWidget(self.delete_deck_btn)

        main_layout.addLayout(toolbar)


        self.stats_frame = QFrame()
        self.stats_frame.setObjectName("statsCard")

        stats_layout = QGridLayout(self.stats_frame)

        stats_layout.setHorizontalSpacing(40)
        stats_layout.setVerticalSpacing(20)

        cards_layout, self.total_value = self.create_stat(
            "📚 Total Cards",
            "0"
        )

        due_layout, self.due_value = self.create_stat(
            "⏰ Due Today",
            "0"
        )

        ease_layout, self.ease_value = self.create_stat(
            "⭐ Average Ease",
            "0"
        )

        reviews_layout, self.review_value = self.create_stat(
            "🔥 Reviews",
            "0"
        )

        stats_layout.addLayout(cards_layout, 0, 0)
        stats_layout.addLayout(due_layout, 0, 1)
        stats_layout.addLayout(ease_layout, 1, 0)
        stats_layout.addLayout(reviews_layout, 1, 1)

        main_layout.addWidget(
            self.stats_frame,
            alignment=Qt.AlignCenter
        )

        line = QFrame()
        line.setFrameShape(QFrame.HLine)

        stats_layout.addWidget(
            line,
            2,
            0,
            1,
            2
        )

        self.ease_info = QLabel(
            "Average Ease determines how quickly\n"
            "flashcards are scheduled.\n\n"
            "Higher values mean cards you've\n"
            "consistently remembered and will\n"
            "appear less often.\n\n"
            "Lower values indicate difficult\n"
            "cards that are reviewed more\n"
            "frequently."
        )

        self.ease_info.setWordWrap(True)
        self.ease_info.setAlignment(Qt.AlignCenter)

        stats_layout.addWidget(
            self.ease_info,
            3,
            0,
            1,
            2
        )

        self.ease_info.setObjectName("statDescription")

        # ==========================
        # Start Review
        # ==========================

        self.review_btn = QPushButton(
            "Start Review"
        )

        self.review_btn.setMinimumHeight(
            50
        )

        self.review_btn.setObjectName("primaryButton")

        # ==========================
        # View All Cards
        # ==========================

        self.view_cards_btn = QPushButton(
            "View All Cards"
        )

        self.view_cards_btn.setMinimumHeight(
            50
        )

        self.view_cards_btn.setObjectName("secondaryButton")

        buttons = QHBoxLayout()

        buttons.addWidget(self.review_btn)
        buttons.addWidget(self.view_cards_btn)

        main_layout.addLayout(buttons)

        self.delete_deck_btn.clicked.connect(
            self.delete_current_deck
        )

    def load_deck(
            self,
            deck_id,
            deck_name
    ):

        self.deck_id = deck_id

        cards = get_flashcards_for_deck(deck_id)

        total, due, ease = get_deck_statistics(deck_id)
        self.title_label.setText(
            deck_name
        )

        self.total_value.setText(str(total))

        self.due_value.setText(str(due))

        self.ease_value.setText(f"{ease:.2f}")

    def delete_current_deck(self):
        reply = QMessageBox.question(
            self,
            "Delete Deck",
            f"Delete '{self.title_label.text()}'?\n\n"
            "All flashcards in this deck will also be permanently deleted.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        delete_deck(self.deck_id)

        # Notify the main window that the deck was deleted
        self.deckDeleted.emit(self.deck_id)

        self.deck_id = None

        self.title_label.setText("No Deck Selected")

        self.total_value.setText("0")
        self.due_value.setText("0")
        self.ease_value.setText("0.00")
        self.review_value.setText("0")

        self.review_btn.setEnabled(False)

        self.view_cards_btn.setEnabled(False)

    def create_stat(self,title, value):

        title_lbl = QLabel(title)
        title_lbl.setAlignment(Qt.AlignCenter)

        value_lbl = QLabel(value)
        value_lbl.setObjectName("statValue")
        value_lbl.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()

        layout.addWidget(title_lbl)
        layout.addWidget(value_lbl)

        return layout, value_lbl