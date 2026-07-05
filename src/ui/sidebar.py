from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
    QPushButton
)
from PySide6.QtCore import Qt


class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # ==========================
        # Title
        # ==========================
        title = QLabel("Library")
        title.setAlignment(Qt.AlignCenter)

        font = title.font()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)

        layout.addWidget(title)

        # ==========================
        # Library Tree
        # ==========================
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)

        self.notes_root = QTreeWidgetItem(
            ["Notes"]
        )

        self.flashcards_root = QTreeWidgetItem(
            ["Flashcard Decks"]
        )

        self.tree.addTopLevelItem(
            self.notes_root
        )

        self.tree.addTopLevelItem(
            self.flashcards_root
        )

        self.tree.expandAll()

        layout.addWidget(self.tree)

        # ==========================
        # Settings Button
        # ==========================
        self.settings_btn = QPushButton("⚙ Settings")

        layout.addWidget(self.settings_btn)

        self.setMinimumWidth(220)
        self.setMaximumWidth(300)

    def clear_notes(self):
        self.notes_root.takeChildren()

    def add_note(self, note_id, title):
        item = QTreeWidgetItem([title])

        item.setData(
            0,
            Qt.UserRole,
            note_id
        )

        self.notes_root.addChild(item)

    def clear_decks(self):
        self.flashcards_root.takeChildren()

    def add_deck(self, deck_id, name):
        item = QTreeWidgetItem([name])

        item.setData(
            0,
            Qt.UserRole,
            deck_id
        )

        self.flashcards_root.addChild(item)