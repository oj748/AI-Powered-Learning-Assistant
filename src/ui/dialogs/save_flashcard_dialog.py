from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QComboBox,
)

from database.flashcard_repository import (
    get_all_decks
)


class SaveFlashcardDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Save Flashcard")

        self.setMinimumWidth(430)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # --------------------------------------------------
        # Existing Deck
        # --------------------------------------------------

        self.existing_radio = QRadioButton(
            "Save to Existing Deck"
        )

        self.new_radio = QRadioButton(
            "Create New Deck"
        )

        self.existing_radio.setChecked(True)

        layout.addWidget(self.existing_radio)

        layout.addWidget(QLabel("Deck"))

        self.deck_combo = QComboBox()

        decks = get_all_decks()

        self.deck_names = [
            deck[1]
            for deck in decks
        ]

        self.deck_combo.addItems(
            self.deck_names
        )

        layout.addWidget(self.deck_combo)

        # --------------------------------------------------
        # New Deck
        # --------------------------------------------------

        layout.addSpacing(8)

        layout.addWidget(self.new_radio)

        layout.addWidget(QLabel("Deck Name"))

        self.deck_name = QLineEdit()

        self.deck_name.setPlaceholderText(
            "Enter deck name..."
        )

        layout.addWidget(self.deck_name)

        # --------------------------------------------------
        # Buttons
        # --------------------------------------------------

        layout.addSpacing(10)

        buttons = QHBoxLayout()

        buttons.addStretch()

        self.cancel_btn = QPushButton(
            "Cancel"
        )

        self.save_btn = QPushButton(
            "Save"
        )

        self.cancel_btn.setObjectName(
            "secondaryButton"
        )
        self.save_btn.setDefault(True)
        self.save_btn.setAutoDefault(True)

        self.save_btn.setObjectName(
            "primaryButton"
        )

        buttons.addWidget(self.cancel_btn)
        buttons.addWidget(self.save_btn)

        layout.addLayout(buttons)

        # --------------------------------------------------
        # Connections
        # --------------------------------------------------

        self.cancel_btn.clicked.connect(
            self.reject
        )

        self.save_btn.clicked.connect(
            self.accept
        )

        self.existing_radio.toggled.connect(
            self.update_state
        )

        self.new_radio.toggled.connect(
            self.update_state
        )

        if not decks:

            self.existing_radio.setEnabled(False)

            self.new_radio.setChecked(True)

        self.update_state()

    # --------------------------------------------------
    # UI State
    # --------------------------------------------------

    def update_state(self):

        existing = self.existing_radio.isChecked()

        self.deck_combo.setEnabled(existing)

        self.deck_name.setEnabled(
            not existing
        )

    # --------------------------------------------------
    # Result
    # --------------------------------------------------

    def get_selected_deck(self):

        if self.new_radio.isChecked():

            return (
                "new",
                self.deck_name.text().strip()
            )

        return (
            "existing",
            self.deck_combo.currentText()
        )