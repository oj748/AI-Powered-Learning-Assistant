from PySide6.QtCore import QUrl
from PySide6.QtWidgets import (
    QWidget,
    QTextEdit,
    QStackedLayout,
)

from PySide6.QtWebEngineWidgets import (
    QWebEngineView
)
from PySide6.QtCore import Signal
from PySide6.QtGui import QTextCursor, QColor
import json

from config import PROJECT_ROOT
from services.theme_manager import theme_manager

from ui.pages.redirect_page import MarkdownPage

HTML_FILE = (
    PROJECT_ROOT /
    "resources" /
    "markdown" /
    "viewer.html"
)

class MarkdownViewer(QWidget):

    textChanged = Signal()

    def __init__(
            self,
            editable=False,
            style="document",
            auto_height=False,
            scrollable=True
    ):
        super().__init__()
        self.editable = editable
        self.page_loaded = False
        self._markdown=""
        self.style = style
        self.auto_height = auto_height
        self.scrollable = scrollable

        self.setup_ui()

        theme_manager.themeChanged.connect(
            self.apply_theme
        )

        theme_manager.fontSizeChanged.connect(
            lambda _: self.apply_theme()
        )

        self.preview.loadFinished.connect(
            self.on_page_loaded
        )

        self.preview.load(
            QUrl.fromLocalFile(
                str(HTML_FILE)
            )
        )
    # ==========================
    # UI
    # ==========================

    def setup_ui(self):

        self.layout = QStackedLayout(self)

        if self.editable:

            self.editor = QTextEdit()

            self.layout.addWidget(self.editor)

            self.editor.textChanged.connect(
                self.refresh_preview
            )

            self.editor.textChanged.connect(
                self.textChanged.emit
            )

        else:

            self.editor = None

        self.preview = QWebEngineView()
        self.preview.setPage(
            MarkdownPage(self.preview)
        )
        self.layout.addWidget(self.preview)

        self.layout.setCurrentWidget(
            self.preview
        )

    def apply_theme(self, theme_name=None):

        if not self.page_loaded:
            return

        colors = theme_manager.colors()

        self.preview.page().setBackgroundColor(
            QColor(colors["surface"])
        )

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

        self.preview.page().runJavaScript(
            js,
            lambda _: self.refresh_preview()
        )

    def on_page_loaded(self, ok):
        print("Page loaded:", ok)
        print("URL:", self.preview.url().toString())

        self.page_loaded = ok

        if not ok:
            return

        self.apply_theme()

    # ==========================
    # Public API
    # ==========================

    def setMarkdown(self, markdown):

        if self.editable:

            self.editor.setPlainText(markdown)

        else:

            self._markdown = markdown

        self.refresh_preview()

    def toMarkdown(self):

        if self.editable:
            return self.editor.toPlainText()

        return self._markdown

    def clear(self):

        if self.editable:

            self.editor.clear()

        else:

            self._markdown = ""

        self.refresh_preview()

    # ==========================
    # Modes
    # ==========================

    def setEditMode(self):

        if not self.editable:
            return

        self.layout.setCurrentWidget(
            self.editor
        )

    def setPreviewMode(self):

        self.refresh_preview()

        self.layout.setCurrentWidget(
            self.preview
        )

    def isEditMode(self):

        if not self.editable:
            return False

        return (
                self.layout.currentWidget()
                == self.editor
        )
    # ==========================
    # Preview
    # ==========================

    def refresh_preview(self):

        if not self.page_loaded:
            return

        markdown = self.toMarkdown()

        escaped = json.dumps(markdown)

        style = json.dumps(self.style)
        scrollable = "true" if self.scrollable else "false"

        self.preview.page().runJavaScript(
            f"renderMarkdown({escaped}, {style}, {scrollable});",
            self._after_render
        )

    def _after_render(self, result):

        if not self.auto_height:
            return

        self.preview.page().runJavaScript(
            "document.getElementById('content').scrollHeight",
            self._set_height
        )

    def _set_height(self, height):
        print(self.style, height)
        if height:
            self.preview.setFixedHeight(height + 4)

    def set_read_only(self, read_only):
        if read_only:
            self.setPreviewMode()
        else:
            self.setEditMode()

    def set_placeholder_markdown(self, text):
        if not self.toMarkdown().strip():
            self.setMarkdown(text)

    def textCursor(self):

        if self.editable:
            return self.editor.textCursor()

        return QTextCursor()

    def setTextCursor(self, cursor):

        if self.editable:
            self.editor.setTextCursor(cursor)

    def scrollToBottom(self):

        self.preview.page().runJavaScript(
            """
            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: "smooth"
            });
            """
        )

    def toggleMode(self):

        if not self.editable:
            return

        if self.isEditMode():
            self.setPreviewMode()
        else:
            self.setEditMode()
