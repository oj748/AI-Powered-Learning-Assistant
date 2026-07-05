
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QColor

from PySide6.QtWebEngineWidgets import QWebEngineView

from config import PROJECT_ROOT

ANIMATION_DIR = (
    PROJECT_ROOT
    / "resources"
    / "animations"
)


class LottieWidget(QWebEngineView):

    def __init__(self, animation_file):

        super().__init__()

        self.setStyleSheet(
            "background:transparent;"
        )


        self.page().setBackgroundColor(
            QColor(0, 0, 0, 0)
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

        self.setAutoFillBackground(False)

        self.setStyleSheet("""
        QWebEngineView{
            background: transparent;
            border:none;
        }
        """)

        html = ANIMATION_DIR / "player.html"

        url = QUrl.fromLocalFile(
            str(html)
        )

        url.setQuery(
            f"file={animation_file}"
        )

        self.load(url)