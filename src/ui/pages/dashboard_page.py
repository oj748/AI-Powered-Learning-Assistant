from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTabBar, QStackedWidget,
    QSizePolicy
)

from PySide6.QtWidgets import QProgressBar

from ui.pages.markdown_viewer import MarkdownViewer
from ui.pages.flashcard_page import FlashcardPage
from ui.pages.quiz_page import QuizPage

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_ui()


    def setup_ui(self):

        self.flashcard_page = FlashcardPage()
        self.quiz_page = QuizPage()

        main_layout = QVBoxLayout(self)


        # ==========================
        # Transcript Area
        # ==========================
        self.transcript_area = MarkdownViewer(editable = True, auto_height=False)

        self.transcript_area.setMarkdown(
            "# Transcript\n\n"
            "*Upload an image or audio file to generate a transcript...*"
        )

        self.transcript_area.setPreviewMode()

        # ==========================
        # Generated Summary
        # ==========================
        self.summary_area = MarkdownViewer(editable = True,auto_height=False)
        self.summary_area.set_read_only(True)
        self.summary_area.set_placeholder_markdown(
            "# Summary\n\n*Click Generate Summary...*"
        )

        # ==========================
        # Header Section
        # ==========================

        self.action_status = QLabel("")

        self.edit_btn = QPushButton("Edit")
        self.save_btn = QPushButton("Save")
        self.save_card_btn = QPushButton("💾 Save Card")
        self.save_deck_btn = QPushButton("💾 Save Deck")
        self.save_flashcard_btn = QPushButton("💾 Save as Flashcard")

        self.edit_btn.setObjectName("secondaryButton")
        self.edit_btn.setObjectName("primaryButton")
        self.save_card_btn.setObjectName("primaryButton")
        self.save_deck_btn.setObjectName("primaryButton")
        self.save_flashcard_btn.setObjectName("primaryButton")

        self.save_btn.hide()
        self.save_card_btn.hide()
        self.save_deck_btn.hide()
        self.save_flashcard_btn.hide()

        self.tab_bar = QTabBar()
        self.tab_bar.setExpanding(False)
        self.tab_bar.setDrawBase(False)

        self.tab_bar.addTab("Transcript")
        self.tab_bar.addTab("Summary")
        self.tab_bar.addTab("Flashcards")
        self.tab_bar.addTab("Quiz")

        header_layout = QHBoxLayout()

        header_layout.addWidget(self.tab_bar)
        header_layout.addWidget(self.action_status)
        header_layout.addStretch()
        header_layout.addWidget(self.edit_btn)
        header_layout.addWidget(self.save_btn)

        header_layout.addWidget(self.save_card_btn)
        header_layout.addWidget(self.save_deck_btn)
        header_layout.addWidget(self.save_flashcard_btn)

        #==========================
        #Stacked widgets
        #==========================
        self.viewer_stack = QStackedWidget()

        self.viewer_stack.addWidget(self.transcript_area)  # 0
        self.viewer_stack.addWidget(self.summary_area)  # 1
        self.viewer_stack.addWidget(self.flashcard_page)  # 2
        self.viewer_stack.addWidget(self.quiz_page)  # 3


        # ==========================
        # Upload Section
        # ==========================

        upload_layout = QHBoxLayout()

        self.upload_image_btn = QPushButton("Upload Image")
        self.upload_audio_btn = QPushButton("Upload Audio")
        self.upload_pdf_btn = QPushButton("Upload PDF")
       # self.upload_video_btn = QPushButton("Upload Video")

        upload_layout.addWidget(self.upload_image_btn)
        upload_layout.addWidget(self.upload_audio_btn)
        upload_layout.addWidget(self.upload_pdf_btn)

        upload_layout.addStretch()

        self.mode_btn = QPushButton("🌐 Online")

        self.mode_btn.setObjectName("primaryButton")
        self.mode_btn.setCheckable(True)
        self.mode_btn.setChecked(True)

        upload_layout.addWidget(self.mode_btn)

        # ==========================
        # Action Buttons
        # ==========================

        self.summary_btn = QPushButton("Generate Summary")
        self.summary_btn.setFixedHeight(50)

        self.flashcards_btn = QPushButton("Generate Flashcards")
        self.quiz_btn = QPushButton("Generate Quiz")

        self.summary_btn.setObjectName("primaryButton")
        self.flashcards_btn.setObjectName("primaryButton")
        self.quiz_btn.setObjectName("primaryButton")

        summary_layout = QHBoxLayout()
        #summary_layout.addStretch()
        summary_layout.addWidget(self.summary_btn,stretch=1)
        #summary_layout.addStretch()

        self.flashcards_btn.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        self.quiz_btn.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.flashcards_btn)
        bottom_layout.addWidget(self.quiz_btn)

        progress_layout = QHBoxLayout()
        self.action_progress = QProgressBar()
        self.action_progress.setRange(0, 0)
        self.action_progress.hide()

        progress_layout.addWidget(self.action_progress)

        self.edit_btn.clicked.connect(
            self.toggle_current_view_edit
        )

        main_layout.setSpacing(12)
        main_layout.setContentsMargins(12, 12, 12, 12)

        main_layout.addLayout(upload_layout)

        main_layout.addLayout(header_layout)

        main_layout.addWidget(self.viewer_stack, stretch=10)

        main_layout.addLayout(bottom_layout)

        main_layout.addLayout(summary_layout)

        main_layout.addLayout(progress_layout)

        self.summary_btn.setEnabled(False)
        self.flashcards_btn.setEnabled(False)
        self.quiz_btn.setEnabled(False)
        self.edit_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        self.action_status.hide()
        self.save_btn.hide()

    def current_viewer(self):
        return self.viewer_stack.currentWidget()

    def update_save_button(self):
        viewer = self.current_viewer()

        if not hasattr(viewer, "toMarkdown"):
            self.save_btn.hide()
            return

        has_text = bool(viewer.toMarkdown().strip())

        self.save_btn.setVisible(has_text)

    def toggle_current_view_edit(self):
        viewer = self.viewer_stack.currentWidget()

        if not hasattr(viewer, "toggleMode"):
            return

        viewer.toggleMode()

        self.edit_btn.setText(
            "Preview" if viewer.isEditMode() else "Edit"
        )

    def on_tab_changed(self, index):

        self.viewer_stack.setCurrentIndex(index)

        self.update_header_controls(index)

    def current_document(self):
        index = self.tab_bar.currentIndex()

        if index == 0:
            return "transcript"

        elif index == 1:
            return "summary"

        return None

    def update_header_controls(self, index):

        self.viewer_stack.setCurrentIndex(index)