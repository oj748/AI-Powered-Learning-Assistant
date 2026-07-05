from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem, QHBoxLayout, QPushButton
)
from PySide6.QtCore import Qt

from database.flashcard_repository import get_all_decks
from ui.widgets.lottie_widget import LottieWidget


class DecksHomePage(QWidget):

    deckSelected = Signal(int)

    def __init__(self):
        super().__init__()

        self.setup_ui()

        self.refresh()

    # =====================================
    # UI
    # =====================================

    def setup_ui(self):

        layout = QVBoxLayout(self)

        toolbar = QHBoxLayout()
        self.back_btn = QPushButton("← Back")
        toolbar.addWidget(self.back_btn, 1)
        toolbar.addStretch(8)
        layout.addLayout(toolbar)

        title = QLabel("Flashcard Decks")
        title.setObjectName("pageTitle")

        font = title.font()
        font.setPointSize(22)
        font.setBold(True)

        title.setFont(font)
        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)

        self.list = QListWidget()
        self.list.setSpacing(4)
        self.list.setVerticalScrollMode(
            QListWidget.ScrollPerPixel
        )
        layout.addWidget(self.list)

        self.empty_label = QLabel(
            "No flashcard decks yet.\n\nCreate a deck to get started."
        )

        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setObjectName("emptyStateLabel")

        layout.addWidget(self.empty_label)



        self.animation = LottieWidget(
            "flashcard_review.json"
        )

        self.animation.setMinimumHeight(
            350
        )

        layout.addWidget(
            self.animation,
            stretch=1
        )


        self.list.itemClicked.connect(
            self.open_deck
        )

    # =====================================
    # Refresh
    # =====================================

    def refresh(self):

        self.list.clear()
        decks = get_all_decks()

        for deck_id, name in decks:

            item = QListWidgetItem(name)

            item.setData(
                Qt.UserRole,
                deck_id
            )

            self.list.addItem(item)

            has_decks = len(decks) > 0

            self.list.setVisible(has_decks)

            self.animation.setVisible(not has_decks)

            self.empty_label.setVisible(not has_decks)

    # =====================================
    # Open
    # =====================================

    def open_deck(self, item):

        self.deckSelected.emit(
            item.data(Qt.UserRole)
        )