from enum import Enum
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication
from config import PROJECT_ROOT

THEME_DIR = (
    PROJECT_ROOT /
    "resources" /
    "themes"
)


class Theme(Enum):
    STORM = "dark"
    MORNING = "light"
    MIST = "mist"

THEME_COLORS = {

    Theme.STORM: {

        "background": "#071824",

        "surface": "#0C1C25",

        "card": "#10222C",

        "card_hover": "#162D38",

        "border": "#1C3642",

        "border_light": "#284552",

        "text": "#E7EDF2",

        "text_secondary": "#AEBCC4",

        "accent": "#325766",

        "accent_hover": "#406977",

        "selection": "#355B69",

        "success": "#4F8A6E",

        "error": "#A35656",
    },
Theme.MORNING: {
    "background": "#EEF2EE",      # Soft misty background
    "surface": "#E4EAE5",         # Panels / sidebar
    "card": "#F3F6F3",            # Paper-like card

    "card_hover": "#EDF2EE",

    "border": "#D2D9D3",
    "border_light": "#E3E8E4",

    "text": "#232623",            # Almost black
    "text_secondary": "#626A63",

    "accent": "#6E8D75",          # Muted sage
    "accent_hover": "#7C9A82",

    "selection": "#D6E2D7",

    "success": "#6F9A76",
    "error": "#B87474",
},
    Theme.MIST: {

        "background": "#D8DEE6",

        "surface": "#D0D8E2",

        "card": "#F4F7FA",

        "card_hover": "#E8EEF4",

        "border": "#B8C6D5",

        "border_light": "#CCD8E4",

        "text": "#31465A",

        "text_secondary": "#5D7286",

        "accent": "#88A9C9",

        "accent_hover": "#7398BE",

        "selection": "#CAD9E8",

        "success": "#7AA28B",

        "error": "#C07171",
    }

}

class ThemeManager(QObject):

    themeChanged = Signal(str)
    fontSizeChanged = Signal(int)

    def __init__(self):
        super().__init__()

        self.app = None
        self._current_theme = Theme.STORM
        self.font_size=18
    # -------------------------------------
    # Initialization
    # -------------------------------------

    def initialize(self, app: QApplication):

        self.app = app

    # -------------------------------------
    # Current Theme
    # -------------------------------------

    @property
    def current_theme(self):

        return self._current_theme

    def colors(self):
        return THEME_COLORS[
            self._current_theme
        ]

    # -------------------------------------
    # Theme Path
    # -------------------------------------

    def theme_path(self, theme: Theme):

        return (
            THEME_DIR /
            f"{theme.value}.qss"
        )

    # -------------------------------------
    # Apply Theme
    # -------------------------------------

    def set_theme(self, theme: Theme):

        if self.app is None:
            raise RuntimeError(
                "ThemeManager.initialize() "
                "must be called first."
            )

        qss_file = self.theme_path(theme)

        stylesheet = qss_file.read_text(
            encoding="utf-8"
        )

        self.app.setStyleSheet(stylesheet)

        self._current_theme = theme

        self.themeChanged.emit(
            theme.value
        )

    @staticmethod
    def from_name(name: str) -> Theme:
        return {
            "Storm": Theme.STORM,
            "Morning": Theme.MORNING,
            "Mist": Theme.MIST,
        }[name]

    def set_font_size(self, size):

        size = max(10, min(size, 32))

        if size == self.font_size:
            return

        self.font_size = size

        font = QApplication.font()
        font.setPointSize(size)

        QApplication.setFont(font)

        # Force stylesheet repolish
        self.app.setStyleSheet(self.app.styleSheet())

        self.fontSizeChanged.emit(size)

theme_manager = ThemeManager()