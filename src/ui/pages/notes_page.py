from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QMessageBox
)
from PySide6.QtCore import Signal

from database.note_repository import (
    get_note,
    update_note, delete_note
)

from ui.pages.markdown_viewer import MarkdownViewer


class NotesPage(QWidget):
    noteDeleted = Signal(int)

    def __init__(self):
        super().__init__()

        self.current_note_id = None

        self.setup_ui()

    # =====================================
    # UI
    # =====================================

    def setup_ui(self):

        layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()

        self.back_btn = QPushButton("← Back")

        self.title_label = QLabel(
            "No Note Selected"
        )

        self.edit_btn = QPushButton(
            "Edit"
        )

        self.save_btn = QPushButton(
            "Save"
        )
        self.delete_btn = QPushButton(
            "Delete"
        )
        self.delete_btn.setObjectName("dangerButton")

        top_bar.addWidget(
            self.back_btn
        )

        top_bar.addWidget(
            self.title_label
        )

        top_bar.addStretch()

        top_bar.addWidget(
            self.edit_btn
        )

        top_bar.addWidget(
            self.save_btn
        )

        top_bar.addWidget(
            self.delete_btn
        )

        layout.addLayout(
            top_bar
        )

        self.viewer = MarkdownViewer(editable=True,auto_height=False)

        self.viewer.setPreviewMode()

        layout.addWidget(
            self.viewer
        )

        self.save_btn.clicked.connect(
            self.save_note
        )

        self.edit_btn.clicked.connect(
            self.toggle_edit
        )

        self.delete_btn.clicked.connect(
            self.delete_current_note
        )
    # =====================================
    # Load
    # =====================================

    def load_note(self, note_id):

        note = get_note(note_id)

        if not note:
            return

        self.current_note_id = note[0]

        title = note[1]

        content = note[2]

        self.title_label.setText(
            title
        )

        self.viewer.setMarkdown(
            content
        )

        self.viewer.setPreviewMode()

        self.edit_btn.setText(
            "Edit"
        )

    # =====================================
    # Save
    # =====================================

    def save_note(self):

        if self.current_note_id is None:
            return

        content = self.viewer.toMarkdown()

        update_note(
            self.current_note_id,
            content
        )

        self.viewer.setPreviewMode()

        self.edit_btn.setText(
            "Edit"
        )

    # =====================================
    # Edit / Preview
    # =====================================

    def toggle_edit(self):

        if self.viewer.isEditMode():

            self.viewer.setPreviewMode()

            self.edit_btn.setText(
                "Edit"
            )

        else:

            self.viewer.setEditMode()

            self.edit_btn.setText(
                "Preview"
            )

    def delete_current_note(self):

        if self.current_note_id is None:
            return

        reply = QMessageBox.question(
            self,
            "Delete Note",
            "Are you sure you want to permanently delete this note?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        deleted_id = self.current_note_id

        delete_note(deleted_id)

        self.current_note_id = None

        self.title_label.setText("No Note Selected")

        self.viewer.setMarkdown("")

        self.viewer.setPreviewMode()

        self.edit_btn.setText("Edit")

        self.noteDeleted.emit(deleted_id)

