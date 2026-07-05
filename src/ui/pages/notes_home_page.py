from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem, QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt

from database.note_repository import get_all_notes
from ui.widgets.lottie_widget import LottieWidget


class NotesHomePage(QWidget):

    noteSelected = Signal(int)

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
        toolbar.addWidget(self.back_btn,1)
        toolbar.addStretch(8)
        layout.addLayout(toolbar)

        title = QLabel("Notes")
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
            "No notes yet.\n\nCreate a note to get started."
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
            self.open_note
        )

    # =====================================
    # Refresh
    # =====================================

    def refresh(self):
        self.list.clear()

        notes = get_all_notes()

        for note_id, title in notes:
            item = QListWidgetItem(title)

            item.setData(
                Qt.UserRole,
                note_id
            )

            self.list.addItem(item)

        has_notes = len(notes) > 0

        self.list.setVisible(has_notes)

        self.animation.setVisible(not has_notes)

        self.empty_label.setVisible(not has_notes)

    # =====================================
    # Open
    # =====================================

    def open_note(self, item):

        self.noteSelected.emit(
            item.data(Qt.UserRole)
        )