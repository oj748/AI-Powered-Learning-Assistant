import time

start = time.time()
print("Imports started")

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
    QStatusBar,
    QFileDialog,
    QMessageBox
)
from PySide6.QtCore import Qt

from database.note_repository import (
    note_exists
)

from ui.dialogs.save_note_dialog import (
    SaveNoteDialog
)
from ui.dialogs.save_flashcard_dialog import SaveFlashcardDialog

from database.note_repository import (
    create_note,
    append_to_note
)

from database.flashcard_repository import (
    create_flashcard_if_missing,
    create_deck, get_due_flashcards_for_deck,
    get_all_decks, get_deck_id_by_name, update_flashcard_review
)

from database.note_repository import (
    get_all_notes
)

from workers.ocr_worker import OCRWorker

print("ocr worker import finished:", time.time() - start)

from ui.sidebar import Sidebar
from ui.pages.dashboard_page import DashboardPage
from ui.pages.flashcard_review import FlashcardReview
from ui.pages.settings_page import SettingsPage
from ui.pages.notes_page import NotesPage
from ui.pages.deck_page import DeckPage
from ui.pages.deck_cards_page import DeckCardsPage
from ui.pages.notes_home_page import NotesHomePage
from ui.pages.decks_home_page import DecksHomePage

from services.theme_manager import theme_manager
from services.theme_manager import Theme

from PySide6.QtCore import QTimer
from workers.model_preload_worker import ModelPreloadWorker
from workers.ocr_preload_worker import OCRPreloadWorker
from workers.summary_worker import SummaryWorker
from workers.quiz_worker import QuizWorker
from workers.flashcard_worker import FlashcardWorker
from workers.pdf_worker import PDFWorker

print("New imports started")
from workers.whisper_preload_worker import WhisperPreloadWorker
from workers.whisper_worker import WhisperWorker
from enum import Enum
print("Imports finished:", time.time() - start)

class AIMode(Enum):
    ONLINE = "online"
    OFFLINE = "offline"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Learning Assistant")
        self.resize(1400, 900)

        self.setup_ui()
        self.connect_signals()
        self.refresh_notes_tree()
        self.refresh_decks_tree()

        self.ai_mode = AIMode.ONLINE

        QTimer.singleShot(1000,self.preload_ocr)

        QTimer.singleShot(3000,self.preload_models)

        QTimer.singleShot(2000, self.preload_whisper)

        self.quiz_generated = False
        self.quiz_data = []

        self.current_transcript = ""
        self.current_summary = ""
        self.previous_transcript = ""
        self.flashcards_generated = False
        self.summary_generated = False
        self.is_generating = False
        self.models_ready = {
            "ocr": False,
            "whisper": False,
        }

        self.dashboard_page.quiz_btn.setEnabled(False)
        self.dashboard_page.flashcards_btn.setEnabled(False)
        self.dashboard_page.summary_btn.setEnabled(False)
        self.dashboard_page.upload_image_btn.setEnabled(False)
        self.dashboard_page.upload_audio_btn.setEnabled(False)
        self.dashboard_page.upload_pdf_btn.setEnabled(False)

    def setup_ui(self):
        # ==========================
        # Central Widget
        # ==========================
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # ==========================
        # Sidebar
        # ==========================
        self.sidebar = Sidebar()
        self.sidebar.setObjectName("sidebar")
        # ==========================
        # Pages
        # ==========================
        self.pages = QStackedWidget()

        self.dashboard_page = DashboardPage()
     #   self.flashcard_page = FlashcardPage()
        self.flashcard_review = FlashcardReview()
        self.deck_cards_page = DeckCardsPage()
      #  self.quiz_page = QuizPage()
        self.settings_page = SettingsPage()
        self.notes_page = NotesPage()
        self.deck_page = DeckPage()
        self.notes_home_page = NotesHomePage()
        self.decks_home_page = DecksHomePage()

        self.pages.addWidget(self.dashboard_page)   # index 0
   #     self.pages.addWidget(self.flashcard_page)   # index 1
   #     self.pages.addWidget(self.quiz_page)        # index 2
        self.pages.addWidget(self.settings_page)    # index 3
        self.pages.addWidget(self.notes_page)       # index 4
        self.pages.addWidget(self.deck_page)        # index 5
        self.pages.addWidget(self.flashcard_review)  # index 6
        self.pages.addWidget(self.deck_cards_page)
        self.pages.addWidget(self.notes_home_page)
        self.pages.addWidget(self.decks_home_page)

        # Dashboard should open first
        self.pages.setCurrentWidget(self.dashboard_page)

        # ==========================
        # Layout
        # ==========================
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.pages)

        # ==========================
        # Status Bar
        # ==========================
        self.status_bar = QStatusBar()

        self.status_bar.showMessage("Ready")

        self.setStatusBar(self.status_bar)

    def connect_signals(self):
        """
        Temporary navigation signals.
        These will be replaced with real logic later.
        """
        # Online offline toggle
        self.dashboard_page.mode_btn.clicked.connect(
            self.toggle_online_mode
        )

        # Settings button in sidebar
        self.sidebar.settings_btn.clicked.connect(
            self.show_settings_page
        )

        self.settings_page.theme_combo.currentTextChanged.connect(
            self.change_theme
        )

        # Back button from settings
        self.settings_page.back_btn.clicked.connect(
            self.show_dashboard_page
        )

        # Back button from flashcards
       # self.flashcard_page.back_btn.clicked.connect(self.show_dashboard_page)

        self.flashcard_review.back_btn.clicked.connect(
            self.show_dashboard_page
        )

        # Exit button from quiz
        #self.quiz_page.exit_btn.clicked.connect(self.show_dashboard_page)

        # Show flashcards page
        self.dashboard_page.flashcards_btn.clicked.connect(
            self.handle_flashcard_button
        )

        # Show quiz page
        self.dashboard_page.quiz_btn.clicked.connect(
            self.handle_quiz_button
        )

        # Upload image to generate transcripts
        self.dashboard_page.upload_image_btn.clicked.connect(
            self.upload_image
        )

        #Upload audios to generate transcripts
        self.dashboard_page.upload_audio_btn.clicked.connect(
            self.upload_audio
        )

        #Upload pdfs
        self.dashboard_page.upload_pdf_btn.clicked.connect(
            self.upload_pdf
        )

        #Enable stuff if transcript area text changed
        self.dashboard_page.transcript_area.textChanged.connect(
            self.transcript_changed
        )

        self.dashboard_page.summary_area.textChanged.connect(
            self.summary_changed
        )

        # Generate summaries
        self.dashboard_page.summary_btn.clicked.connect(
            self.generate_summary
        )

        # Save buttons
        self.dashboard_page.save_btn.clicked.connect(
            self.save_current_document
        )

        self.dashboard_page.save_card_btn.clicked.connect(
            self.save_current_flashcard
        )

        self.dashboard_page.save_deck_btn.clicked.connect(
            self.save_all_flashcards
        )

        self.dashboard_page.save_flashcard_btn.clicked.connect(
            self.save_question_as_flashcard
        )

        # Back button from notes_page and deck_page
        self.notes_page.back_btn.clicked.connect(
            self.show_dashboard_page
        )
        self.deck_page.back_btn.clicked.connect(
            self.show_dashboard_page
        )


        #OPen notes from tree
        #self.sidebar.tree.itemClicked.connect(self.open_library_item)
        self.sidebar.tree.itemClicked.connect(self.on_library_item_clicked)

        #Review deck
        self.deck_page.review_btn.clicked.connect(
            self.start_deck_review
        )

        # show all flashcards from a deck
        self.deck_page.view_cards_btn.clicked.connect(
            self.show_deck_cards
        )
        #back button from cards table page
        self.deck_cards_page.back_btn.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.deck_page)
        )


        # FLASHCARD REVIEW BUTTONS
        self.flashcard_review.reviewed.connect(
            self.handle_review
        )

        # Refresh Sidebar after deleting note or deck
        self.notes_page.noteDeleted.connect(self.on_note_deleted)
        self.deck_page.deckDeleted.connect(self.on_deck_deleted)

        # Open note and flashcard deck when selected form the list on the home page
        self.notes_home_page.noteSelected.connect(
            self.open_note
        )

        self.decks_home_page.deckSelected.connect(
            self.open_deck
        )

        # Back buttonss from notes and decks home
        self.notes_home_page.back_btn.clicked.connect(
            self.show_dashboard_page
        )

        self.decks_home_page.back_btn.clicked.connect(
            self.show_dashboard_page
        )

        self.dashboard_page.tab_bar.currentChanged.connect(
            self.dashboard_page.viewer_stack.setCurrentIndex
        )

        self.dashboard_page.tab_bar.currentChanged.connect(
            lambda _: self.refresh_dashboard_state()
        )

    def transcript_changed(self):

        if self.is_generating:
            return

        self.current_transcript = (
            self.dashboard_page.transcript_area
            .toMarkdown()
            .strip()
        )

        self.dashboard_page.update_save_button()

        # Transcript changed -> invalidate generated content
        self.summary_generated = False
        self.flashcards_generated = False
        self.quiz_generated = False

        self.dashboard_page.summary_btn.setText(
            "Generate Summary"
        )

        self.refresh_dashboard_state()

    def summary_changed(self):
        if self.is_generating:
            return

        self.current_summary = (
            self.dashboard_page.summary_area
            .toMarkdown()
            .strip()
        )

        self.dashboard_page.update_save_button()

        self.refresh_dashboard_state()

    def preload_models(self):

        self.preload_worker = ModelPreloadWorker()

        self.preload_worker.finished.connect(
            lambda: self.status_bar.showMessage(
                "Phi Ready"
            )
        )

        self.preload_worker.start()

    def show_dashboard_page(self):
        self.pages.setCurrentWidget(self.dashboard_page)
        self.status_bar.showMessage("Dashboard")

    def show_settings_page(self):
        self.settings_page.theme_combo.setCurrentText(
            {
                Theme.STORM: "Storm",
                Theme.MORNING: "Morning",
                Theme.MIST: "Mist",
            }[theme_manager.current_theme]
        )
        self.pages.setCurrentWidget(self.settings_page)
        self.status_bar.showMessage("Settings")

    def transcript_progress(self, message):
        self.dashboard_page.action_status.setText(message)

    def upload_image(self):
        self.dashboard_page.action_status.setText(
            "Preparing transcription..."
        )

        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )

        if not files:
            return

        self.previous_transcript = self.current_transcript

        self.current_transcript = ""

        self.status_bar.showMessage(
            "Generating Transcript..."
        )

        self.dashboard_page.action_status.show()

        self.is_generating = True
        self.refresh_dashboard_state()

        self.ocr_worker = OCRWorker(
            files,
            online=self.ai_mode == AIMode.ONLINE
        )

        self.ocr_worker.progress.connect(
            self.transcript_progress
        )

        self.ocr_worker.finished.connect(
            self.ocr_finished
        )
        self.ocr_worker.partial_transcript.connect(
            self.update_live_transcript
        )

        self.ocr_worker.start()

    def ocr_finished(self, transcript):

        if self.previous_transcript:

            final = (
                    self.previous_transcript
                    + "\n\n"
                    + transcript
            )

        else:

            final = transcript

        self.current_transcript = final

        self.dashboard_page.transcript_area.setMarkdown(
            final
        )

        self.dashboard_page.action_status.hide()

        self.is_generating = False
        self.refresh_dashboard_state()

        #self.dashboard_page.save_btn.show()

        self.status_bar.showMessage(
            "Transcript Ready"
        )

    def generate_summary(self):

        self.is_generating = True
        self.refresh_dashboard_state()

       # self.dashboard_page.summary_progress.show()

        transcript = self.current_transcript

        self.summary_worker = SummaryWorker(
            transcript,
            online=self.ai_mode == AIMode.ONLINE
        )

        self.summary_worker.progress.connect(
            self.summary_progress
        )

        self.summary_worker.finished.connect(
            self.summary_finished
        )

        self.summary_worker.start()

    def summary_progress(self, message):
        self.dashboard_page.action_status.setText(
            message
        )

    def summary_finished(self, summary):

       # self.current_summary_markdown = summary
        self.summary_generated = True

        self.current_summary = summary

        self.dashboard_page.summary_area.setMarkdown(summary)
        self.dashboard_page.tab_bar.setCurrentIndex(1)

        self.dashboard_page.summary_btn.setText(
            "Summary Generated"
        )

        self.is_generating = False
        self.refresh_dashboard_state()

    def generate_quiz(self):

        self.is_generating = True
        self.refresh_dashboard_state()

        #self.dashboard_page.action_progress.show()

        document = self.dashboard_page.current_document()

        if document == "summary":
            source_text = self.current_summary or self.current_transcript
        else:
            source_text = self.current_transcript or self.current_summary

        self.quiz_worker = QuizWorker(
            source_text,
            online=self.ai_mode == AIMode.ONLINE
        )

        self.quiz_worker.progress.connect(
            self.quiz_progress
        )

        self.quiz_worker.finished.connect(
            self.quiz_created
        )

        self.quiz_worker.start()

    def quiz_created(self, quiz_data):

        self.dashboard_page.quiz_page.load_quiz(quiz_data)

        self.dashboard_page.tab_bar.setCurrentIndex(3)

        self.quiz_generated = True

        self.dashboard_page.quiz_btn.setText("Generate Quiz")

        self.is_generating = False
        self.refresh_dashboard_state()

    def quiz_progress(self, message):
        self.dashboard_page.quiz_btn.setText(message)

    def handle_quiz_button(self):
        self.generate_quiz()

    def generate_flashcard(self):

        self.is_generating = True
        self.refresh_dashboard_state()

        #self.dashboard_page.action_progress.show()

        document = self.dashboard_page.current_document()

        if document == "summary":
            source_text = self.current_summary or self.current_transcript
        else:
            source_text = self.current_transcript or self.current_summary

        self.flash_worker = FlashcardWorker(
            source_text,
            online=self.ai_mode == AIMode.ONLINE
        )

        self.flash_worker.progress.connect(
            self.flashcard_progress
        )

        self.flash_worker.finished.connect(
            self.flash_created
        )

        self.flash_worker.start()

    def flash_created(self, flash_data):

        self.dashboard_page.flashcard_page.load_flashcards(
            flash_data
        )

        self.dashboard_page.tab_bar.setCurrentIndex(2)

        self.flashcards_generated = True

        self.dashboard_page.action_progress.hide()

        self.dashboard_page.flashcards_btn.setText("Generate Flashcards")

        self.is_generating = False
        self.refresh_dashboard_state()

    def flashcard_progress(self, message):
        self.dashboard_page.flashcards_btn.setText(message)

    def handle_flashcard_button(self):
        self.generate_flashcard()

    def preload_ocr(self):
      #  self.dashboard_page.upload_image_btn.setEnabled(False)
        self.dashboard_page.upload_image_btn.setText("Loading OCR")
       # self.dashboard_page.upload_pdf_btn.setEnabled(False)
        self.dashboard_page.upload_pdf_btn.setText("Loading OCR")
        self.ocr_preload_worker = OCRPreloadWorker()

        self.ocr_preload_worker.finished.connect(
            self.ocr_models_ready
        )

        self.ocr_preload_worker.start()

    def ocr_models_ready(self):
       # self.dashboard_page.upload_image_btn.setEnabled(True)
        self.dashboard_page.upload_image_btn.setText("Upload Image")
       # self.dashboard_page.upload_pdf_btn.setEnabled(True)
        self.dashboard_page.upload_pdf_btn.setText("Upload PDF")
        self.models_ready["ocr"] = True
        self.refresh_dashboard_state()
        print("OCR Ready")

    def preload_whisper(self):

      #  self.dashboard_page.upload_audio_btn.setEnabled(False)
        self.dashboard_page.upload_audio_btn.setText(
            "Loading Whisper"
        )

        self.whisper_preload_worker = WhisperPreloadWorker()

        self.whisper_preload_worker.finished.connect(
            self.whisper_ready
        )

        self.whisper_preload_worker.start()

    def whisper_ready(self):

       # self.dashboard_page.upload_audio_btn.setEnabled(True)
        self.models_ready["whisper"] = True
        self.refresh_dashboard_state()
        self.dashboard_page.upload_audio_btn.setText(
            "Upload Audio"
        )

        print("Whisper Ready")

    def upload_audio(self):

        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Audio Files",
            "",
            "Audio (*.mp3 *.wav *.m4a *.flac)"
        )

        if not files:
            return

        self.dashboard_page.action_status.setText(
            "Preparing transcription..."
        )

        self.previous_transcript = self.current_transcript

        self.current_transcript = ""

        self.status_bar.showMessage(
            "Generating Transcript..."
        )

        self.dashboard_page.action_status.show()

        self.is_generating = True
        self.refresh_dashboard_state()

        self.whisper_worker = WhisperWorker(files)

        self.whisper_worker.partial_transcript.connect(
            self.update_live_transcript
        )

        self.whisper_worker.progress.connect(
            self.transcript_progress
        )

        self.whisper_worker.finished.connect(
            self.audio_finished
        )

        self.whisper_worker.start()

    def update_live_transcript(self, segment):

        self.current_transcript += segment

        if self.previous_transcript:
            display = (
                    self.previous_transcript
                    + "\n\n"
                    + self.current_transcript
            )
        else:
            display = self.current_transcript

        self.dashboard_page.transcript_area.setMarkdown(display)
        self.dashboard_page.transcript_area.scrollToBottom()

    def audio_finished(self, transcript):

        self.current_transcript = transcript

        if self.previous_transcript:
            final = (
                    self.previous_transcript
                    + "\n\n"
                    + transcript
            )
        else:
            final = transcript

        self.current_transcript = final

        self.dashboard_page.transcript_area.setMarkdown(final)

        self.dashboard_page.action_status.hide()

        self.status_bar.showMessage("Transcript Ready")

        self.is_generating = False
        self.refresh_dashboard_state()

    def save_current_document(self):

        document = self.dashboard_page.current_document()

        if document == "transcript":
            self._save_transcript_note()

        elif document == "summary":
            self._save_summary_note()

    def _save_transcript_note(self):

        dialog = SaveNoteDialog()

        if not dialog.exec():
            return

        mode, note_name = (
            dialog.get_selected_note()
        )

        transcript = (
            self.dashboard_page.transcript_area
            .toMarkdown()
            .strip()
        )

        markdown = f"""# Transcript\n\n{transcript}
    """

        if mode == "new":

            if not note_name:
                QMessageBox.warning(
                    self,
                    "Invalid Name",
                    "Please enter a note name."
                )

                return

            if note_exists(note_name):
                QMessageBox.warning(
                    self,
                    "Note Exists",
                    "A note with that name already exists."
                )

                return

            create_note(
                note_name,
                markdown
            )

        else:
            print(repr(markdown))
            append_to_note(
                note_name,
                markdown
            )

        self.refresh_notes_tree()

        self.status_bar.showMessage(
            "Note Saved"
        )

    def _save_summary_note(self):

        dialog = SaveNoteDialog()

        if not dialog.exec():
            return

        mode, note_name = (
            dialog.get_selected_note()
        )

        summary = (
            self.dashboard_page.summary_area
            .toMarkdown()
            .strip()
        )

        markdown = f"""# Summary\n\n{summary}
    """

        if mode == "new":

            if not note_name:
                QMessageBox.warning(
                    self,
                    "Invalid Name",
                    "Please enter a note name."
                )

                return

            if note_exists(note_name):
                QMessageBox.warning(
                    self,
                    "Note Exists",
                    "A note with that name already exists."
                )

                return
            print(summary)
            create_note(
                note_name,
                markdown
            )

        else:
            print(repr(markdown))
            append_to_note(
                note_name,
                markdown
            )

        self.refresh_notes_tree()

        self.status_bar.showMessage(
            "Note Saved"
        )

    def refresh_notes_tree(self):

        self.sidebar.clear_notes()

        notes = get_all_notes()

        for note_id, title in notes:
            self.sidebar.add_note(
                note_id,
                title
            )

        self.sidebar.tree.expandAll()

        # Refresh Notes Home
        self.notes_home_page.refresh()

    def open_note(self, note_id):
        self.notes_page.load_note(
            note_id
        )

        self.pages.setCurrentWidget(
            self.notes_page
        )

        self.status_bar.showMessage("Note")

    def on_note_deleted(self):

        self.refresh_notes_tree()

        self.show_notes_home()

    def show_notes_home(self):

        self.notes_home_page.refresh()

        self.pages.setCurrentWidget(
            self.notes_home_page
        )

        self.status_bar.showMessage("Notes")

    def open_library_item(self, item):

        parent = item.parent()

        if not parent:
            return

        if parent == self.sidebar.notes_root:

            note_id = item.data(
                0,
                Qt.UserRole
            )

            self.notes_page.load_note(
                note_id
            )

            self.pages.setCurrentWidget(
                self.notes_page
            )

        elif parent == self.sidebar.flashcards_root:

            deck_id = item.data(
                0,
                Qt.UserRole
            )

            self.open_deck(deck_id)

    def on_library_item_clicked(self, item, column):

        # Notes root
        if item == self.sidebar.notes_root:
            self.show_notes_home()
            return

        # Flashcards root
        if item == self.sidebar.flashcards_root:
            self.show_decks_home()
            return

        parent = item.parent()

        if parent == self.sidebar.notes_root:

            note_id = item.data(0, Qt.UserRole)

            self.open_note(note_id)

        elif parent == self.sidebar.flashcards_root:

            deck_id = item.data(0, Qt.UserRole)

            self.open_deck(deck_id)

    def save_current_flashcard(self):

        card = (
            self.dashboard_page.flashcard_page.flashcards[
                self.dashboard_page.flashcard_page.current_card
            ]
        )

        dialog = SaveFlashcardDialog()

        if not dialog.exec():
            return

        mode, deck_name = (
            dialog.get_selected_deck()
        )

        if mode == "new":
            if not deck_name:
                QMessageBox.warning(
                    self,
                    "Invalid Name",
                    "Please enter a deck name."
                )
                return
            create_deck(deck_name)

            self.refresh_decks_tree()

            decks = get_all_decks()

            deck_id = next(
                deck[0]
                for deck in decks
                if deck[1] == deck_name
            )

        else:

            deck_id = get_deck_id_by_name(
                deck_name
            )

        create_flashcard_if_missing(
            deck_id,
            card["question"],
            card["answer"]
        )
        self.refresh_decks_tree()
        self.status_bar.showMessage(
            "Flashcard Saved"
        )

    def save_all_flashcards(self):

        dialog = SaveFlashcardDialog()

        if not dialog.exec():
            return

        mode, deck_name = (
            dialog.get_selected_deck()
        )

        if mode == "new":
            if not deck_name:
                QMessageBox.warning(
                    self,
                    "Invalid Name",
                    "Please enter a deck name."
                )
                return
            create_deck(deck_name)

            self.refresh_decks_tree()

        deck_id = get_deck_id_by_name(
            deck_name
        )

        for card in (
                self.dashboard_page.flashcard_page.flashcards
        ):
            create_flashcard_if_missing(
                deck_id,
                card["question"],
                card["answer"]
            )
        self.status_bar.showMessage(
            "Flashcards Saved"
        )

    def open_deck(self,deck_id):

        decks = get_all_decks()

        for d_id, name in decks:

            if d_id == deck_id:
                self.deck_page.load_deck(
                    d_id,
                    name
                )

                break

        self.pages.setCurrentWidget(
            self.deck_page
        )
        self.status_bar.showMessage(
            "Flashcard Deck"
        )

    def on_deck_deleted(self):

        self.refresh_decks_tree()

        self.decks_home_page.refresh()

        self.show_decks_home()

    def show_decks_home(self):

        self.decks_home_page.refresh()

        self.pages.setCurrentWidget(
            self.decks_home_page
        )

        self.status_bar.showMessage("Flashcard Decks")

    def start_deck_review(self):

        deck_id = (
            self.deck_page.deck_id
        )

        cards = get_due_flashcards_for_deck(
            deck_id
        )

        flashcards = []

        for card in cards:
            flashcards.append({
                "id": card[0],
                "question": card[2],
                "answer": card[3]
            })

        self.flashcard_review.deck_title.setText(
            self.deck_page.title_label.text()
        )

        self.flashcard_review.load_flashcards(
            flashcards
        )

        self.pages.setCurrentWidget(
            self.flashcard_review
        )

    def refresh_decks_tree(self):

        self.sidebar.clear_decks()

        decks = get_all_decks()

        for deck_id, name in decks:
            self.sidebar.add_deck(
                deck_id,
                name
            )

        self.sidebar.tree.expandAll()

        # Refresh Decks Home
        self.decks_home_page.refresh()

    def handle_review(self,flashcard_id,rating):
        update_flashcard_review(
            flashcard_id,
            rating
        )

    def show_deck_cards(self):

        self.deck_cards_page.load_deck(
            self.deck_page.deck_id,
            self.deck_page.title_label.text()
        )

        self.pages.setCurrentWidget(
            self.deck_cards_page
        )

    def toggle_online_mode(self):

        if self.dashboard_page.mode_btn.isChecked():
            self.ai_mode = AIMode.ONLINE
            self.dashboard_page.mode_btn.setText("🌐 Online")
        else:
            self.ai_mode = AIMode.OFFLINE
            self.dashboard_page.mode_btn.setText("💻 Offline")

    def save_question_as_flashcard(self):

        if not self.dashboard_page.quiz_page.quiz_data:
            return

        question = (
            self.dashboard_page.quiz_page.quiz_data[
                self.dashboard_page.quiz_page.current_question
            ]
        )
        correct = question["correct"]
        index = ord(correct.upper()) - ord("A")
        correct_text = question["options"][index]

        answer = (
            f"{correct_text}\n"
        )

        dialog = SaveFlashcardDialog()

        if not dialog.exec():
            return

        mode, deck_name = dialog.get_selected_deck()

        if mode == "new":

            if not deck_name:
                QMessageBox.warning(
                    self,
                    "Invalid Name",
                    "Please enter a deck name."
                )
                return

            create_deck(deck_name)

            self.refresh_decks_tree()

            deck_id = get_deck_id_by_name(deck_name)

        else:

            deck_id = get_deck_id_by_name(deck_name)

        create_flashcard_if_missing(
            deck_id,
            question["question"],
            answer
        )

        self.refresh_decks_tree()

        self.status_bar.showMessage(
            "Question Saved as Flashcard"
        )

    def upload_pdf(self):

        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select PDF",
            "",
            "PDF Files (*.pdf)"
        )

        if not file:
            return


        self.dashboard_page.action_status.setText(
            "Preparing transcription..."
        )

        self.previous_transcript = self.current_transcript
        self.current_transcript = ""

        self.status_bar.showMessage(
            "Generating Transcript..."
        )

        self.dashboard_page.action_status.show()

        self.is_generating = True
        self.refresh_dashboard_state()

        self.pdf_worker = PDFWorker(
            file,
            online=self.ai_mode == AIMode.ONLINE
        )

        self.pdf_worker.progress.connect(
            self.transcript_progress
        )

        self.pdf_worker.partial_transcript.connect(
            self.update_live_transcript
        )

        self.pdf_worker.finished.connect(
            self.pdf_finished
        )

        self.pdf_worker.start()

    def pdf_finished(self, transcript):

        self.current_transcript = transcript

        if self.previous_transcript:

            final = (
                    self.previous_transcript
                    + "\n\n"
                    + transcript
            )

        else:

            final = transcript

        self.current_transcript = final

        self.dashboard_page.transcript_area.setMarkdown(
            final
        )

        self.dashboard_page.action_status.hide()

        self.is_generating = False
        self.refresh_dashboard_state()

        self.status_bar.showMessage(
            "Transcript Ready"
        )

    def change_theme(self, name):

        theme_manager.set_theme(
            theme_manager.from_name(name)
        )

    def refresh_dashboard_state(self):

        d = self.dashboard_page

        # -----------------------------
        # Current state
        # -----------------------------
        tab = d.tab_bar.currentIndex()

        has_transcript = bool(self.current_transcript.strip())
        has_summary = bool(self.current_summary.strip())
        has_content = has_transcript or has_summary

        has_flashcards = bool(
            d.flashcard_page.flashcards
        )

        has_quiz = bool(
            d.quiz_page.quiz_data
        )

        generating = self.is_generating

        # -----------------------------
        # Upload buttons
        # -----------------------------

        d.upload_image_btn.setEnabled(
            self.models_ready["ocr"] and not generating
        )

        d.upload_pdf_btn.setEnabled(
            self.models_ready["ocr"] and not generating
        )

        d.upload_audio_btn.setEnabled(
            self.models_ready["whisper"] and not generating
        )
        # -----------------------------
        # Progress
        # -----------------------------
        d.action_progress.setVisible(generating)

        # -----------------------------
        # Edit / Save
        # -----------------------------
        d.edit_btn.hide()
        d.save_btn.hide()

        if tab <= 1:

            d.edit_btn.show()

            viewer = d.current_viewer()

            if hasattr(viewer, "isEditMode"):
                d.edit_btn.setText(
                    "Preview"
                    if viewer.isEditMode()
                    else "Edit"
                )

            if hasattr(viewer, "toMarkdown"):
                d.save_btn.setVisible(
                    bool(viewer.toMarkdown().strip())
                )

        # -----------------------------
        # Header buttons
        # -----------------------------
        d.save_card_btn.hide()
        d.save_deck_btn.hide()
        d.save_flashcard_btn.hide()

        d.summary_btn.show()
        d.flashcards_btn.show()
        d.quiz_btn.show()

       #if tab == 1:
            # d.summary_btn.hide()

        if tab == 2:

            d.summary_btn.hide()
            d.quiz_btn.hide()

            d.flashcards_btn.setVisible(
                not self.flashcards_generated
            )

            d.save_card_btn.setVisible(
                has_flashcards
            )

            d.save_deck_btn.setVisible(
                has_flashcards
            )

        elif tab == 3:

            d.summary_btn.hide()
            d.flashcards_btn.hide()

            d.quiz_btn.setVisible(
                not self.quiz_generated
            )

            d.save_flashcard_btn.setVisible(
                has_quiz
            )

            d.quiz_page.next_btn.setVisible(
                self.quiz_generated
            )

        # -----------------------------
        # Generation buttons
        # -----------------------------
        d.summary_btn.setEnabled(

            has_transcript

            and not self.summary_generated

            and not generating
        )

        d.flashcards_btn.setEnabled(

            has_content

            and not self.flashcards_generated

            and not generating
        )

        d.quiz_btn.setEnabled(

            has_content

            and not self.quiz_generated

            and not generating
        )
