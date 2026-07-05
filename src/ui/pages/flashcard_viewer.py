from config import PROJECT_ROOT
import json

from PySide6.QtCore import (
    QUrl,
    Qt,
    Signal,
    QObject,
    Slot
)

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout
)

from PySide6.QtWebEngineWidgets import (
    QWebEngineView
)

from PySide6.QtWebChannel import (
    QWebChannel
)

from services.theme_manager import (
    theme_manager
)

HTML_FILE = (
    PROJECT_ROOT /
    "resources" /
    "markdown" /
    "flashcard.html"
)


# ======================================================
# Bridge between JavaScript and Python
# ======================================================

class FlashcardBridge(QObject):

    def __init__(self, viewer):
        super().__init__()

        self.viewer = viewer

    @Slot()
    def revealFinished(self):
        print("Reveal signal received!")

        self.viewer.revealed.emit()


# ======================================================
# Flashcard Viewer
# ======================================================

class FlashcardViewer(QWidget):

    revealed = Signal()

    def __init__(self):
        super().__init__()

        self.page_loaded = False

        self.current_progress = ""
        self.current_question = ""
        self.current_answer = ""

        self.can_previous = False
        self.can_next = False

        self.channel = None
        self.bridge = None

        self.setup_ui()

        theme_manager.themeChanged.connect(
            self.apply_theme
        )

        theme_manager.fontSizeChanged.connect(
            lambda _: self.apply_theme()
        )

        self.channel = QWebChannel()

        self.bridge = FlashcardBridge(self)

        self.channel.registerObject(
            "bridge",
            self.bridge
        )

        self.web.page().setWebChannel(
            self.channel
        )

        self.web.loadFinished.connect(
            self.on_page_loaded
        )

        self.web.load(
            QUrl.fromLocalFile(
                str(HTML_FILE)
            )
        )

    # ======================================================
    # UI
    # ======================================================

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        self.web = QWebEngineView()

        self.web.setContextMenuPolicy(
            Qt.NoContextMenu
        )

        self.web.setAttribute(Qt.WA_TranslucentBackground)
        self.web.page().setBackgroundColor(Qt.transparent)

        layout.addWidget(self.web)

    def apply_theme(self, theme_name=None):

        if not self.page_loaded:
            return

        colors = theme_manager.colors()

        js = (
            "".join(
                f"document.documentElement.style.setProperty('--{k.replace('_', '-')}','{v}');"
                for k, v in colors.items()
            )
        )

        js += (
            f"document.documentElement.style.setProperty("
            f"'--font-size','{theme_manager.font_size}px');"
        )

        self.web.page().runJavaScript(js)
    # ======================================================
    # Load Finished
    # ======================================================

    def on_page_loaded(self, ok):

        self.page_loaded = ok

        if not ok:
            return

        self.apply_theme()
        # ---------------------------------------
        # Create WebChannel
        # ---------------------------------------

        if self.current_question:

            self.load_card(
                self.current_question,
                self.current_answer
            )

    # ======================================================
    # Public API
    # ======================================================

    def load_card(
        self,
        question,
        answer
    ):

        self.current_question = question
        self.current_answer = answer

        if not self.page_loaded:
            return

        question = json.dumps(question)
        answer = json.dumps(answer)

        js = f"""
        loadFlashcard(
            {question},
            {answer}
        );
        """

        self.web.page().runJavaScript(js)

    # ======================================================
    # Reveal
    # ======================================================

    def reveal(self):

        self.web.page().runJavaScript(
            "revealAnswer();"
        )

    # ======================================================
    # Reset
    # ======================================================

    def reset(self):

        self.web.page().runJavaScript(
            "resetCard();"
        )

    # ======================================================
    # Query State
    # ======================================================

    def is_revealed(
        self,
        callback
    ):

        self.web.page().runJavaScript(
            "isRevealed();",
            callback
        )

    # ======================================================
    # Reload
    # ======================================================

    def reload(self):

        self.web.reload()

    def clear(self):

        self.current_question = ""
        self.current_answer = ""

        if self.page_loaded:

            self.load_card(
                "",
                ""
            )