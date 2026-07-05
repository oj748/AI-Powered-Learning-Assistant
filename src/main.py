import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from database.db import setup_database

from services.theme_manager import (
    theme_manager,
    Theme
)

def main():
    setup_database()
    app = QApplication(sys.argv)

    theme_manager.initialize(app)

    theme_manager.set_theme(
        Theme.STORM
    )
    theme_manager.set_font_size(14)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":  
    main()