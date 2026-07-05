from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QRadioButton,
    QSizePolicy
)

from PySide6.QtCore import (
    Qt,
    Signal
)

from ui.pages.markdown_viewer import MarkdownViewer


class QuizOptionWidget(QFrame):

    clicked = Signal(object)

    def __init__(self):
        super().__init__()

        self.selected = False

        self.setup_ui()
        self.apply_style()

    # ===================================
    # UI
    # ===================================

    def setup_ui(self):

        self.setCursor(Qt.PointingHandCursor)

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Minimum
        )

        self.setMinimumHeight(70)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(15)

        self.radio = QRadioButton()

        self.viewer = MarkdownViewer(
            style="option",
            auto_height=True, scrollable= False
        )
        self.viewer.setPreviewMode()


        layout.addWidget(
            self.radio,
            alignment=Qt.AlignVCenter
        )

        layout.addWidget(
            self.viewer,
            stretch=1
        )

    # ===================================
    # API
    # ===================================

    def setMarkdown(self, text):

        self.viewer.setMarkdown(text)

    def isChecked(self):

        return self.selected

    def setChecked(self, checked):

        self.selected = checked
        self.radio.setChecked(checked)

        self.apply_style()

    # ===================================
    # Styling
    # ===================================

    def apply_style(self):

        if self.selected:

            self.setStyleSheet("""
            QuizOptionWidget{
                background:#e8f1ff;
                border:2px solid #4c8bf5;
                border-radius:12px;
            }
            """)

        else:

            self.setStyleSheet("""
            QuizOptionWidget{
                background:white;
                border:1px solid #d9d9d9;
                border-radius:12px;
            }

            QuizOptionWidget:hover{
                border:2px solid #8ab4ff;
                background:#f8fbff;
            }
            """)

    # ===================================
    # Mouse
    # ===================================

    def mousePressEvent(self, event):

        self.clicked.emit(self)

        super().mousePressEvent(event)