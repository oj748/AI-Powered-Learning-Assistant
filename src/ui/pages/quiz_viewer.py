import json

from PySide6.QtCore import (
    QUrl,
    Signal, Qt
)

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout
)

from PySide6.QtWebEngineWidgets import (
    QWebEngineView
)

from config import PROJECT_ROOT
from services.theme_manager import theme_manager

HTML_FILE = (
    PROJECT_ROOT /
    "resources" /
    "markdown" /
    "quiz.html"
)


class QuizViewer(QWidget):

    optionChanged = Signal(str)

    def __init__(self):
        super().__init__()

        self.page_loaded = False

        self.current_question = ""
        self.current_options = []
        self.current_progress = ""

        self.setup_ui()
        theme_manager.themeChanged.connect(
            self.apply_theme
        )

        theme_manager.fontSizeChanged.connect(
            lambda _: self.apply_theme()
        )

        self.web.loadFinished.connect(
            self.on_page_loaded
        )

        self.web.load(
            QUrl.fromLocalFile(
                str(HTML_FILE)
            )
        )

    # ==========================================
    # UI
    # ==========================================

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        self.web = QWebEngineView()

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
    # ==========================================
    # Loading
    # ==========================================

    def on_page_loaded(self, ok):

        self.page_loaded = ok

        if ok and self.current_question:

            self.load_question(
                self.current_progress,
                self.current_question,
                self.current_options
            )

        self.apply_theme()

    # ==========================================
    # Public API
    # ==========================================

    def load_question(
            self,
            progress,
            question,
            options
    ):

        self.current_progress = progress
        self.current_question = question
        self.current_options = options

        if not self.page_loaded:
            return

        progress = json.dumps(progress)
        question = json.dumps(question)
        options = json.dumps(options)

        js = f"""

        renderQuiz(
            {progress},
            {question},
            {options}
        );

        """

        self.web.page().runJavaScript(js)

    # ==========================================
    # Selected Option
    # ==========================================

    def selected_option(self, callback):

        self.web.page().runJavaScript(

            "getSelectedOption();",

            callback

        )

    # ==========================================
    # Feedback
    # ==========================================

    def show_feedback(

            self,
            selected_letter,
            correct_letter,

            explanation

    ):
        selected = json.dumps(selected_letter)

        correct = json.dumps(correct_letter)

        explanation = json.dumps(explanation)

        js = f"""

        showFeedback(

            {selected},

            {correct},

            {explanation}

        );

        """

        self.web.page().runJavaScript(js)

    # ==========================================
    # Helpers
    # ==========================================

    def clear(self):

        self.load_question(

            "",

            "",

            []

        )

    def reload(self):

        self.web.reload()

    def show_results(self, score, total):

        if not self.page_loaded:
            return

        js = f"""
        showResults({score}, {total});
        """

        self.web.page().runJavaScript(js)