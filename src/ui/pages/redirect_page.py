from PySide6.QtWebEngineCore import (
    QWebEnginePage
)
from PySide6.QtGui import QDesktopServices


class MarkdownPage(QWebEnginePage):

    def acceptNavigationRequest(
        self,
        url,
        nav_type,
        isMainFrame
    ):

        if nav_type == QWebEnginePage.NavigationTypeLinkClicked:

            QDesktopServices.openUrl(url)

            return False

        return super().acceptNavigationRequest(
            url,
            nav_type,
            isMainFrame
        )