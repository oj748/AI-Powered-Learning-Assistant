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

from database.note_repository import (
    get_note_titles
)


class SaveNoteDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Save Note")

        self.setMinimumWidth(430)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # --------------------------------------------------
        # Existing Note
        # --------------------------------------------------

        self.existing_radio = QRadioButton(
            "Save to Existing Note"
        )

        self.new_radio = QRadioButton(
            "Create New Note"
        )

        self.existing_radio.setChecked(True)

        layout.addWidget(self.existing_radio)

        layout.addWidget(QLabel("Note"))

        self.note_combo = QComboBox()

        notes = get_note_titles()

        self.note_combo.addItems(notes)

        layout.addWidget(self.note_combo)

        # --------------------------------------------------
        # New Note
        # --------------------------------------------------

        layout.addSpacing(8)

        layout.addWidget(self.new_radio)

        layout.addWidget(QLabel("Note Name"))

        self.note_name = QLineEdit()

        self.note_name.setPlaceholderText(
            "Enter note name..."
        )

        layout.addWidget(self.note_name)

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

        self.save_btn.setObjectName(
            "primaryButton"
        )
        self.save_btn.setDefault(True)
        self.save_btn.setAutoDefault(True)

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

        if not notes:

            self.existing_radio.setEnabled(False)

            self.new_radio.setChecked(True)

        self.update_state()

    # --------------------------------------------------
    # UI State
    # --------------------------------------------------

    def update_state(self):

        existing = self.existing_radio.isChecked()

        self.note_combo.setEnabled(existing)

        self.note_name.setEnabled(
            not existing
        )

    # --------------------------------------------------
    # Result
    # --------------------------------------------------

    def get_selected_note(self):

        if self.new_radio.isChecked():

            return (
                "new",
                self.note_name.text().strip()
            )

        return (
            "existing",
            self.note_combo.currentText()
        )