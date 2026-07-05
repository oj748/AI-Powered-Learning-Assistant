from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QComboBox, QApplication
)
from PySide6.QtCore import Qt

from services.theme_manager import theme_manager


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

        self.plus_btn.clicked.connect(self.increase_font)
        self.minus_btn.clicked.connect(self.decrease_font)

    def setup_ui(self):

        main_layout = QVBoxLayout(self)

        self.back_btn = QPushButton("← Back to Dashboard")
        main_layout.addWidget(self.back_btn)

        title = QLabel("Settings")
        title.setAlignment(Qt.AlignCenter)

        font = title.font()
        font.setPointSize(18)
        font.setBold(True)
        title.setFont(font)

        main_layout.addWidget(title)

        appearance_group = QGroupBox("Appearance")

        appearance_layout = QHBoxLayout()

        appearance_layout.addWidget(QLabel("Theme"))

        self.theme_combo = QComboBox()
        self.theme_combo.addItems([
            "Storm",
            "Morning",
            "Mist"
        ])

        appearance_layout.addWidget(self.theme_combo)

        appearance_group.setLayout(appearance_layout)

        main_layout.addWidget(appearance_group)

        main_layout.addStretch()

        font_layout = QHBoxLayout()

        font_layout.addWidget(QLabel("Font Size"))

        self.minus_btn = QPushButton("-")
        self.plus_btn = QPushButton("+")

        self.font_label = QLabel(
            str(theme_manager.font_size)
        )

        self.font_label.setAlignment(Qt.AlignCenter)

        font_layout.addWidget(self.minus_btn)
        font_layout.addWidget(self.font_label)
        font_layout.addWidget(self.plus_btn)

        appearance_layout.addLayout(font_layout)

    def increase_font(self):
        theme_manager.set_font_size(
            theme_manager.font_size + 1
        )

        print("App font:", QApplication.font().pointSize())

        self.font_label.setText(
            str(theme_manager.font_size)
        )

    def decrease_font(self):
        theme_manager.set_font_size(
            theme_manager.font_size - 1
        )

        print("App font:", QApplication.font().pointSize())
        
        self.font_label.setText(
            str(theme_manager.font_size)
        )